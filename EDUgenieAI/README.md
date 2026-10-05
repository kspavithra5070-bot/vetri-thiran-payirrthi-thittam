# EduGenie

EduGenie is an AI-powered educational assistant.

It provides:

- Question and Answer
- Topic Explanation
- Quiz Generation
- Text Summarization
- Personalized Learning Recommendations

The backend is built with FastAPI.

The frontend uses HTML, CSS and JavaScript.

Gemini is used for generative AI features.

An optional LaMini-Flan-T5 model can be used locally
for concept explanations.

---

# PROJECT STRUCTURE

EduGenie/

├── app/

│   ├── __init__.py

│   ├── main.py

│   ├── config.py

│   ├── schemas.py

│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py
│   │   ├── local_explainer.py
│   │   ├── explanation_service.py
│   │   └── quiz_service.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── app.js
│
├── tests/
│   └── test_api.py
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md

---

# REQUIREMENTS

Install:

Python 3.10 or newer.

VS Code is recommended.

---

# CREATE VIRTUAL ENVIRONMENT

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate

---

# INSTALL PACKAGES

python -m pip install --upgrade pip

pip install -r requirements.txt

---

# CONFIGURE GEMINI

Create:

.env

using:

.env.example

Then add your Gemini API key:

GEMINI_API_KEY=your_actual_api_key

Example:

GEMINI_API_KEY=YOUR_KEY_HERE

---

# RUN APPLICATION

Run:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

---

# FASTAPI DOCUMENTATION

Open:

http://127.0.0.1:8000/docs

This displays the Swagger API interface.

---

# HEALTH CHECK

Open:

http://127.0.0.1:8000/health

Expected response:

{
    "status": "ok",
    "gemini_configured": true,
    "local_model_enabled": false
}

---

# API ENDPOINTS

GET /

Web application.

GET /health

Application health.

POST /qa

Question answering.

POST /explain

Explain an educational topic.

POST /quiz

Generate exactly three MCQs.

POST /summarize

Summarize educational text.

POST /learn/recommendations

Generate a structured learning path.

---

# TESTING

Activate the virtual environment.

Run:

pytest -q

The tests check:

1. Home page
2. Health endpoint

---

# LOCAL EXPLANATION MODEL

The project supports:

MBZUAI/LaMini-Flan-T5-783M

To enable it, change:

USE_LOCAL_MODEL=false

to:

USE_LOCAL_MODEL=true

The model will be downloaded when the explanation
feature is first used.

This can require additional disk space and memory.

---

# GEMINI MODE

For normal development, use:

USE_LOCAL_MODEL=false

Gemini will handle:

- Q&A
- Explanation
- Quiz generation
- Summarization
- Learning recommendations

---

# TROUBLESHOOTING

## Gemini API key error

If you see:

GEMINI_API_KEY is not configured.

Check that:

1. .env exists
2. GEMINI_API_KEY is filled
3. Uvicorn was restarted

---

## Port already in use

Use:

uvicorn app.main:app --reload --port 8001

Then open:

http://127.0.0.1:8001

---

## Package installation error

Run:

python -m pip install --upgrade pip

Then:

pip install -r requirements.txt

---

# APPLICATION WORKFLOW

User

↓

HTML/CSS/JavaScript Frontend

↓

FastAPI Backend

↓

Selected API Endpoint

↓

AI Service

↓

Gemini / Local LaMini Model

↓

Generated Result

↓

Frontend

↓

Student

---

# FEATURES

## 1. Ask Questions

Students can enter an academic question.

EduGenie sends it to the Gemini model.

The generated answer is displayed on the page.

---

## 2. Explain Topic

Students enter a difficult concept.

EduGenie explains the concept in simpler language.

---

## 3. Generate Quiz

Students paste study material.

EduGenie creates:

3 questions

4 options per question

1 correct answer

---

## 4. Summarize

Students paste a long educational passage.

EduGenie creates a shorter revision-friendly summary.

---

## 5. Learning Recommendations

Students provide:

Topic

Learning level

EduGenie creates a structured learning path.

---

# SECURITY

Never put the Gemini API key in:

HTML

CSS

JavaScript

The key must remain in:

.env

The .gitignore file prevents .env from being committed.

---

# DEVELOPMENT

Start server:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Run tests:

pytest -q