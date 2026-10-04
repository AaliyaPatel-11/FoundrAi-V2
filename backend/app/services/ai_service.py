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
        if response.status_code != 200:
            logger.error(
                f"Upstream AI provider error: status_code={response.status_code} "
                f"url={url} model={model} body={response.text}"
            )
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
    Attempts configured model first, and gracefully falls back to available Groq models if 404/429 occurs.
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

    # Candidate models to try in order
    candidate_models: List[str] = []
    if AI_MODEL and AI_MODEL.strip():
        candidate_models.append(AI_MODEL.strip())
    
    # Standard reliable Groq fallback models
    default_fallbacks = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "deepseek-r1-distill-llama-70b",
        "qwen-2.5-32b"
    ]
    for fallback in default_fallbacks:
        if fallback not in candidate_models:
            candidate_models.append(fallback)

    last_error = None
    for model in candidate_models:
        try:
            logger.info(f"Attempting completion request with model: {model}")
            return _call_upstream_provider(formatted_messages, model)
        except httpx.HTTPStatusError as http_err:
            logger.warning(
                f"Model '{model}' failed with HTTP {http_err.response.status_code}. "
                f"Trying next model candidate..."
            )
            last_error = http_err
            continue
        except Exception as e:
            logger.warning(f"Model '{model}' failed with error: {str(e)}. Trying next candidate...")
            last_error = e
            continue

    logger.error(f"All candidate models failed. Last error: {last_error}")
    return "FondrAI is currently unable to reach the AI model. Please check the API key and provider configuration."
