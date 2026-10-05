import httpx
import logging
from typing import List
from app.models.chat import ChatMessage
from app.config import AI_API_KEY, AI_BASE_URL, AI_MODEL
from app.prompts.system_prompt import FONDRAI_SYSTEM_PROMPT
from app.prompts.cfo_prompt import CFO_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def _fetch_available_models() -> List[str]:
    """
    Fetch all currently active models from Groq / OpenAI compatible provider dynamically.
    """
    if not AI_API_KEY:
        return []
        
    base_url = AI_BASE_URL or "https://api.groq.com/openai/v1"
    url = f"{base_url.rstrip('/')}/models"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if "data" in data and isinstance(data["data"], list):
                    models = [m["id"] for m in data["data"] if "id" in m]
                    # Filter out non-chat models
                    chat_models = [
                        m for m in models 
                        if not any(x in m.lower() for x in ("whisper", "guard", "safeguard", "embed", "tts", "moderation"))
                    ]
                    logger.info(f"Dynamically discovered active models from provider: {chat_models}")
                    return chat_models
            else:
                logger.warning(f"Failed to fetch models from {url}: status={resp.status_code}, body={resp.text}")
    except Exception as e:
        logger.warning(f"Could not dynamically query active models: {str(e)}")
    return []


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

    base_url = AI_BASE_URL or "https://api.groq.com/openai/v1"
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


def generate_response(messages: List[ChatMessage], role: str = None) -> str:
    """
    Generate a response based on the complete conversation history.
    Uses FONDRAI_SYSTEM_PROMPT as the primary system instruction.
    Dynamically auto-discovers and uses active models from the provider.
    """
    if not AI_API_KEY:
        logger.info("AI_API_KEY is not configured. Using offline development fallback.")
        return "FondrAI is online, but its AI provider isn't configured yet."

    # Prepare conversation history payload
    system_prompt = CFO_SYSTEM_PROMPT if role == "cfo" else FONDRAI_SYSTEM_PROMPT

    formatted_messages = [
        {"role": "system", "content": system_prompt}
    ]

    for msg in messages:
        if msg.role in ("user", "assistant"):
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        elif msg.role == "system":
            logger.warning("Ignoring external system message in request history to preserve prompt integrity.")

    # 1. Candidate models: start with configured AI_MODEL
    candidate_models: List[str] = []
    if AI_MODEL and AI_MODEL.strip():
        candidate_models.append(AI_MODEL.strip())
    
    # 2. Dynamically fetch currently active models from Groq / provider
    active_discovered_models = _fetch_available_models()
    for m in active_discovered_models:
        if m not in candidate_models:
            candidate_models.append(m)

    # 3. Known modern models as last-resort static fallback
    static_fallbacks = [
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview",
        "llama-3.2-3b-preview",
        "llama-3.2-1b-preview",
    ]
    for m in static_fallbacks:
        if m not in candidate_models:
            candidate_models.append(m)

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
    return "FondrAI is currently unable to reach the AI model. Please check your AI API key and provider configuration."
