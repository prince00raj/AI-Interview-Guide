AI-Powered Company-Specific Interview Guide

An intelligent web application that generates company-specific,
role-based interview questions and evaluates candidate responses using
AI. The system offers adaptive difficulty, instant feedback, and a
seamless practice experience without requiring user login.

Project Overview

This project is designed to help candidates prepare for technical
interviews by generating dynamic questions tailored to specific
companies and job roles. The system uses a locally hosted LLaMA 3 model
via Ollama for both question generation and answer evaluation.

Features

-   Company-Specific Questions
-   Role-Based Question Sets
-   AI-Powered Evaluation
-   Adaptive Difficulty Levels
-   Responsive UI
-   No Login Required

Technology Stack

Backend: Python, Flask, Ollama
Frontend: HTML

Installation & Setup

1.  Install Ollama
2.  Set up Python environment
3.  Install dependencies
4.  Run main.py
5.  Open browser at http://localhost:5000

Usage

Generate questions → Take test → Submit answers → Get AI feedback

Project Structure

ai-interview-guide/ - main.py - requirements.txt - templates/ -
generate.html - hi.html - README.md

API Endpoints

POST /chat – generate questions
POST /evaluate – evaluate answers

Supported Companies & Roles

10+ IT companies and 8 major engineering roles

Troubleshooting

-   Ensure Ollama is running
-   Free system RAM
-   Resolve port conflicts

Author

Aadishakti Murlidhar Muley
Final Year Project
