# FondrAI — Your AI Co-Founder

FondrAI is an agentic AI startup co-founder developed for the **MASQUERADE '26** AI Chatbot Challenge. It is designed to help founders turn vague, early-stage ideas into structured, clear, and actionable startup plans through natural, challenging, and context-aware dialogue.

Rather than acting as a simple questionnaire or template filler, FondrAI thinks along with the founder—listening, validating pain points, and constructively stress-testing assumptions.

---

## What FondrAI Does

FondrAI is equipped with conversational capability to help generate, refine, and structure the following:

* **Startup Idea Discovery**: Refines vague, early-stage sentences into defined value propositions.
* **Problem & Customer Clarification**: Pinpoints specific target segments and distinguishes between users and buyers.
* **Constructive Idea Challenging**: Stress-tests assumptions and calls out contradictions.
* **Business Model Canvas**: Populates all nine standard segments based on dialogue context.
* **SWOT Analysis**: Creates context-specific Strengths, Weaknesses, Opportunities, and Threats.
* **MVP Builder**: Separates features into *MUST HAVE*, *NICE TO HAVE*, and *NOT YET* lists.
* **MVP Roadmap**: Creates step-by-step validation-oriented pathways (Validate, Prototype, Build, Test, Launch).
* **Pitch Generation**: Drafts concise elevator and investor pitches without fabricating metrics.
* **Validation Strategy**: Recommends concrete real-world experiments instead of generic advice.
* **Startup Snapshot**: Generates structured summaries of the startup's current state.
* **Founder Next Steps**: Highlights top 3 high-impact sequential actions.
* **Multi-Turn Conversational Memory**: Tracks pivots and updates assumptions dynamically.

---

## Why FondrAI Is Different

FondrAI is designed to behave like a sharp, practical co-founder rather than a generic template filler:
* **Constructive Skepticism**: It does not blindly agree or praise weak concepts; it questions assumptions to build stronger businesses.
* **Active Discovery**: It avoids interrogation lists, choosing instead to ask exactly one high-value question per turn to guide thinking naturally.
* **Context-Aware Pivots**: If you change your target customer, pricing, or product, it immediately updates its context and builds on the newest criteria.
* **Honest Reasoning**: It distinguishes between established facts and estimates/assumptions, and avoids fabricating details you haven't provided.
* **Playful Persona**: It stays focused on business but responds naturally to casual topics (like coffee) without corporate canned responses.

---

## Architecture

```text
User 
 └── React Frontend (Vercel)
      └── FastAPI Backend (Render)
           ├── Primary AI Model: Llama-3.3-70B-Versatile (Groq API)
           └── Fallback AI Model: Llama-3.1-8B-Instant (Groq API) [Triggers on 429/5xx/Timeouts]
```

* **Frontend**: React, Vite, Tailwind CSS, Lucide icons. Hosted on **Vercel**.
* **Backend**: Python 3.13, FastAPI, Pydantic data validation, Uvicorn, HTTPX client. Hosted on **Render**.
* **AI Provider**: OpenAI-compatible API via **Groq**. 

---

## Live Application

* **Frontend Live Application**: [https://foundr-ai-v2-delta.vercel.app](https://foundr-ai-v2-delta.vercel.app)

---

## API Endpoint

FondrAI implements a standard OpenAI-compatible completions endpoint for judges and external client integrations:

* **Endpoint**: `POST https://foundrai-v2.onrender.com/chat/completions`

### Example Request

```json
{
  "model": "fondrai",
  "messages": [
    {
      "role": "user",
      "content": "I want to build an app for tracking class attendance."
    }
  ],
  "stream": false
}
```

### Example Response

```json
{
  "id": "chatcmpl-fondrai-b75725be",
  "object": "chat.completion",
  "created": 1785517825,
  "model": "fondrai",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "An app for tracking student attendance could be useful. But before we dive into features, let's understand the specific pain. What is the current way students track their classes today, and why is it failing?"
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

---

## Multi-Turn Conversation

To maintain state in a stateless API layout, clients must resend the complete conversation history array in the `messages` parameter:

```json
{
  "model": "fondrai",
  "messages": [
    { "role": "user", "content": "I want to build an app for tracking student attendance." },
    { "role": "assistant", "content": "What is the current way students track their classes today, and why is it failing?" },
    { "role": "user", "content": "They use paper syllabus lists and calendars, but keep forgetting to update it." }
  ],
  "stream": false
}
```

---

## Local Development

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Set up virtual environment and activate:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   ```bash
   cp .env.example .env
   ```
   Add your `AI_API_KEY` to `backend/.env`.
5. Start server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Configure environment:
   ```bash
   cp .env.example .env
   ```
   *Note: Ensure VITE_API_BASE_URL is set to http://localhost:8000.*
4. Start dev server:
   ```bash
   npm run dev
   ```

---

## Environment Variables

### Backend Configuration (`backend/.env`)

Configure the following variables in the backend:
* `AI_API_KEY`: API access key for the upstream model provider. (Must never be committed or exposed to the client side).
* `AI_BASE_URL`: Completion endpoint URL of the upstream provider (e.g. `https://api.groq.com/openai/v1`).
* `AI_MODEL`: Target primary model (defaults to `llama-3.3-70b-versatile`).
* `FRONTEND_ORIGIN`: Allowed origins for CORS separation (e.g. `https://foundr-ai-v2-delta.vercel.app`).

### Frontend Configuration (`frontend/.env`)

* `VITE_API_BASE_URL`: Target endpoint url for backend requests (e.g. `http://localhost:8000`).

---

## Reliability & Fault Tolerance

* **Automatic Failover**: If the primary upstream model (`llama-3.3-70b-versatile`) triggers an HTTP 429 rate limit error, HTTP 5xx server failure, or times out, the backend automatically retries the exact same query against `llama-3.1-8b-instant`.
* **Sanitized Diagnostics**: Stack traces, API keys, and raw upstream error bodies (containing organization IDs, limits, or tokens) are intercepted server-side.
* **Fallback Response**: If both models fail, the API gracefully returns a capacity-limit response within the standard OpenAI structure: `"FondrAI hit a temporary capacity limit. Give me a moment and try that again."`

---

## Health Check

* **Endpoint**: `GET /health`
* **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

---

## Project Structure

```text
fondrai/
├── backend/
│   ├── app/
│   │   ├── api/          # chat router endpoints
│   │   ├── models/       # chat request/response schemas
│   │   ├── prompts/      # compressed system prompts
│   │   ├── services/     # client client with automatic failover
│   │   └── main.py       # FastAPI application entrypoint
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # ChatMessage, ChatInput, WelcomeScreen
│   │   └── App.jsx       # layout and messages management
│   ├── .env.example
│   └── package.json
└── README.md
```

---

## MASQUERADE '26

FondrAI was engineered from the ground up for the **MASQUERADE '26** AI Chatbot Challenge. It conforms to strict requirements regarding CORS separation, multi-turn history parsing, response schema formatting, and offline capacity fallbacks.

---

## Security

* **Secrets Isolation**: API credentials reside exclusively on the backend server.
* **Identity Safeguards**: Incoming system instructions submitted to the API are safely filtered out, preventing system prompt overrides.
* **Opaque Client API**: The frontend and judges only see model `"fondrai"` in the JSON response, masking upstream provider details.
