from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import requests

app = Flask(__name__)

app.secret_key = 'your-secret-key'
app.template_folder = 'templates'
app.static_folder = 'public'

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"

# Home page - question generation
@app.route('/')
def index():
    return render_template('generate.html')

# Test page - answering questions
@app.route('/test')
def test_page():
    questions = session.get('questions', [])
    company = session.get('company', '')
    role = session.get('role', '')
    level = session.get('level', '')
    return render_template('test.html', questions=questions, company=company, role=role, level=level)

# API to generate interview questions
@app.route('/chat', methods=['POST'])
def generate_questions():
    data = request.get_json()
    prompt = data.get('prompt')
    company = data.get('company')
    role = data.get('role')
    level = data.get('level')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        })

        if response.status_code != 200:
            return jsonify({'error': 'AI generation failed'}), 500

        result = response.json()
        text = result.get('response', '').strip()
        lines = text.split('\n')
        questions = [line.strip() for line in lines if line.strip() and (line.endswith('?') or line.strip().startswith(tuple('0123456789')))]
        # Limit to 7
        all_questions = questions  # full list
        test_questions = questions[:7]
        # Store data in session
        session['questions'] = test_questions
        session['company'] = company
        session['role'] = role
        session['level'] = level

        return jsonify({
            'success': True,
            'questions': all_questions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to evaluate user answers
@app.route('/evaluate', methods=['POST'])
def evaluate_answers():
    data = request.get_json()
    answers = data.get('answers')

    if not answers:
        return jsonify({'error': 'Answers are required'}), 400

    company = session.get('company', '')
    role = session.get('role', '')
    level = session.get('level', '')
    questions = session.get('questions', [])

    qa_prompt = ""
    for i, question in enumerate(questions):
        user_answer = answers.get(str(i), "").strip()  # Removing any surrounding whitespace

        # Check for blank input more explicitly
        if not user_answer:  # This now considers empty or whitespace-only strings
            qa_prompt += f"Q{i + 1}: {question}\nAnswer: (empty)\nScore: 0/5\n\n"
        else:
            qa_prompt += f"Q{i + 1}: {question}\nAnswer: {user_answer}\n\n"

    full_prompt = f"""You are a rigorous technical interviewer evaluating a candidate for a {level} level {role} role at {company}.
Below are the candidate's answers. Evaluate them strictly. Deduct points for incomplete or incorrect explanations, vague answers, and lack of technical depth.

For each question, provide:
- A strict evaluation (1-2 sentences)
- A score out of 5 (1-5 scale, where 5 is perfect and 1 is poor)
- If the answer is blank, give 0/5 and say "Answer was blank."

Format your response as:
Q1: [evaluation] Score: x/5
Q2: [evaluation] Score: x/5
...

Evaluate these answers:

{qa_prompt}
"""

    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llama3:latest",
            "prompt": full_prompt,
            "stream": False
        })

        result = response.json()
        feedback = result.get('response', '').strip()

        # Check if feedback is empty or contains "Answer was blank" or other key responses
        if 'Answer was blank' in feedback:
            feedback += "\nNote: One or more answers were left blank. Please review them."

        return jsonify({'feedback': feedback})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)