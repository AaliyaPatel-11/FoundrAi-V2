# FondrAI - AI Startup Co-founder

FondrAI is an AI startup co-founder app that helps you turn a vague idea into a real, actionable startup plan through a natural, guided conversation.

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, JavaScript
- **Backend**: Python, FastAPI, Pydantic, httpx
- **APIs**: OpenAI-compatible MASQUERADE '26 chat completions standard

---

## Project Structure

```text
fondrai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── chat.py
│   │   ├── models/
│   │   │   └── chat.py
│   │   ├── prompts/
│   │   │   └── system_prompt.py
│   │   ├── services/
│   │   │   └── ai_service.py
│   │   ├── config.py
│   │   └── main.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInput.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── TypingIndicator.jsx
│   │   │   └── WelcomeScreen.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── package.json
├── .gitignore
└── README.md
```

---

## Getting Started

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Customize `.env` with your API keys if needed (or leave empty to use the offline fallback).
5. Start the backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
4. Start the frontend:
   ```bash
   npm run dev
   ```
   The application will be running on `http://localhost:5173`.

---

## API Documentation

### Health Check

- **Endpoint**: `GET /health`
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

### Chat Completion (MASQUERADE '26 Compatible)

- **Endpoint**: `POST /chat/completions`
- **Request Format**:
  ```json
  {
    "model": "fondrai",
    "messages": [
      {
        "role": "user",
        "content": "Hello"
      }
    ],
    "stream": false
  }
  ```
- **Response Format**:
  ```json
  {
    "id": "chatcmpl-fondrai-1722442477",
    "object": "chat.completion",
    "created": 1722442477,
    "model": "fondrai",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "FondrAI is online. Tell me what you're thinking of building."
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 0,
      "completion_tokens": 0,
      "total_tokens": 0
    }
  }
  ```

#### cURL Verification Example

```bash
curl http://localhost:8000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "fondrai", "messages": [{"role": "user", "content": "Hello"}], "stream": false}'
```
