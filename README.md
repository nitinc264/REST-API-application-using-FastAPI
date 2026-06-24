# IR INFOTECH API Assignment

A production-ready REST API built using **FastAPI** and **Google Gemini AI** that provides intelligent text processing capabilities including text summarization, language translation, and professional email generation.

## Features

* FastAPI-based REST API
* Google Gemini AI integration
* Request validation using Pydantic v2
* Structured error handling
* Centralized logging
* Environment variable configuration
* Request ID tracing
* CORS support
* Interactive Swagger Documentation
* Unit Testing with Pytest
* Clean modular architecture

---

## Tech Stack

* Python 3.10+
* FastAPI
* Google Gemini API
* Pydantic v2
* Pydantic Settings
* Uvicorn
* Pytest
* HTTPX
* Python Dotenv

---

## Project Structure

```text
project/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   └── test_summarize.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
```

---

## API Endpoints

### Health Check

**GET /**

Returns application status and version information.

#### Response

```json
{
  "app": "IR INFOTECH API Assignment",
  "version": "1.0.0",
  "status": "healthy"
}
```

---

### Summarize Text

**POST /summarize**

Generate a concise AI-powered summary of a text block.

#### Request

```json
{
  "text": "Artificial Intelligence is transforming industries worldwide by automating repetitive tasks and improving decision making.",
  "max_length": 100
}
```

#### Response

```json
{
  "summary": "Artificial Intelligence is fundamentally changing industries worldwide.",
  "original_length": 14,
  "summary_length": 8,
  "request_id": "uuid"
}
```

---

### Translate Text

**POST /translate**

Translate text into any supported language.

#### Request

```json
{
  "text": "Hello, how are you?",
  "target_language": "Hindi",
  "source_language": "English"
}
```

#### Response

```json
{
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "source_language": "English",
  "target_language": "Hindi",
  "request_id": "uuid"
}
```

---

### Generate Professional Email

**POST /generate-email**

Generate a complete professional email from a context description.

#### Request

```json
{
  "context": "Requesting an internship opportunity at a technology company.",
  "tone": "professional",
  "recipient_name": "Hiring Manager",
  "sender_name": "Nitin Chauhan"
}
```

#### Response

```json
{
  "subject": "Internship Opportunity Inquiry",
  "body": "Generated email content...",
  "tone": "professional",
  "request_id": "uuid"
}
```

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd project
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-flash

APP_NAME=IR INFOTECH API Assignment
APP_VERSION=1.0.0
APP_ENV=development
APP_PORT=8000

LOG_LEVEL=INFO
CORS_ORIGINS=*
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Running Tests

Execute all tests:

```bash
python -m pytest
```

Sample Result:

```text
14 passed in 1.64s
```

---

## Validation & Error Handling

The API validates all incoming requests using Pydantic models.

Example validation error:

```json
{
  "error": true,
  "message": "Request validation failed. Please check your input.",
  "detail": "Field required",
  "request_id": "uuid"
}
```

---

## Logging

The application logs:

* Incoming requests
* Outgoing responses
* Request IDs
* Errors and exceptions
* Application startup/shutdown events

---

## Key Features Implemented

* Request Validation
* Exception Handling
* Centralized Logging
* Environment Variable Management
* Swagger Documentation
* ReDoc Documentation
* Request ID Middleware
* CORS Middleware
* AI-Powered NLP Features
* Unit Testing

---

## Author

**Nitin Chauhan**

B.Tech – Artificial Intelligence & Data Science

IR INFOTECH – AI/ML Intern Assignment
