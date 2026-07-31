import httpx
import logging
from typing import List
from app.models.chat import ChatMessage
from app.config import AI_API_KEY, AI_BASE_URL, AI_MODEL
from app.prompts.system_prompt import FONDRAI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def _call_upstream_provider(messages: List[dict], model: str) -> str:
    """
    Helper function to call the upstream OpenAI-compatible chat completion provider.
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800,
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    base_url = AI_BASE_URL or "https://api.openai.com/v1"
    url = f"{base_url.rstrip('/')}/chat/completions"

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data and "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"]
                
        raise ValueError("Invalid response structure from upstream AI provider")


def generate_response(messages: List[ChatMessage]) -> str:
    """
    Generate a response based on the complete conversation history.
    Uses FONDRAI_SYSTEM_PROMPT as the primary system instruction.
    Attempts primary model first, fallback to llama-3.1-8b-instant on 429, 5xx, or timeouts.
    If no AI API key is configured, uses the offline development fallback.
    """
    if not AI_API_KEY:
        logger.info("AI_API_KEY is not configured. Using offline development fallback.")
        return "FondrAI is online, but its AI provider isn't configured yet."

    # Prepare conversation history payload
    formatted_messages = [
        {"role": "system", "content": FONDRAI_SYSTEM_PROMPT}
    ]

    for msg in messages:
        if msg.role in ("user", "assistant"):
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        elif msg.role == "system":
            logger.warning("Ignoring external system message in request history to preserve prompt integrity.")

    primary_model = AI_MODEL or "llama-3.3-70b-versatile"
    fallback_model = "llama-3.1-8b-instant"

    # Attempt 1: Call primary model
    try:
        logger.info(f"Attempting completion request with primary model: {primary_model}")
        return _call_upstream_provider(formatted_messages, primary_model)

    except (httpx.HTTPStatusError, httpx.TimeoutException, ValueError) as e:
        should_fallback = False
        error_details = ""

        if isinstance(e, httpx.HTTPStatusError):
            status_code = e.response.status_code
            if status_code == 429:
                error_details = "HTTP 429 (Rate Limited)"
                should_fallback = True
            elif 500 <= status_code < 600:
                error_details = f"HTTP {status_code} (Server Error)"
                should_fallback = True
            else:
                error_details = f"HTTP {status_code}"
        elif isinstance(e, httpx.TimeoutException):
            error_details = "Connection Timeout"
            should_fallback = True
        elif isinstance(e, ValueError):
            error_details = "Value parsing error"
            should_fallback = True

        if not should_fallback:
            # Re-raise authentication (e.g. 401/403) or malformed query (400) errors immediately
            logger.error(f"Unrecoverable error with primary model: {error_details}. Skipping fallback.")
            raise e

        # Attempt 2: Call fallback model
        logger.warning(f"Primary AI model unavailable ({error_details}); attempting fallback model ({fallback_model}).")
        
        try:
            return _call_upstream_provider(formatted_messages, fallback_model)
        except httpx.HTTPStatusError as fallback_http_err:
            logger.error(f"Fallback model request failed with HTTP status {fallback_http_err.response.status_code}")
            return "FondrAI hit a temporary capacity limit. Give me a moment and try that again."
        except Exception as fallback_err:
            logger.error("Fallback model request failed with an unexpected error")
            return "FondrAI hit a temporary capacity limit. Give me a moment and try that again."

    except Exception as e:
        logger.error("General error encountered in AI service")
        return "FondrAI is experiencing issues connecting to the AI provider. Please check backend server logs."
