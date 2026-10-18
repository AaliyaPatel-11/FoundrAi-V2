
import httpx
import logging
from typing import List

from app.models.chat import ChatMessage
from app.config import AI_API_KEY, AI_BASE_URL, AI_MODEL

from app.prompts.system_prompt import FONDRAI_SYSTEM_PROMPT
from app.prompts.cfo_prompt import CFO_SYSTEM_PROMPT
from app.prompts.cto_prompt import CTO_SYSTEM_PROMPT
from app.prompts.cmo_prompt import CMO_SYSTEM_PROMPT
from app.prompts.product_prompt import PRODUCT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def generate_response(messages: List[ChatMessage], role: str = None) -> str:
    """Generate a response using the selected startup agent."""

    if not AI_API_KEY:
        logger.info(
            "AI_API_KEY is not configured. Using offline development fallback."
        )
        return "FondrAI is online, but its AI provider isn't configured yet."

    # Select the appropriate agent system prompt.
    prompts = {
        "cfo": CFO_SYSTEM_PROMPT,
        "cto": CTO_SYSTEM_PROMPT,
        "cmo": CMO_SYSTEM_PROMPT,
        "product": PRODUCT_SYSTEM_PROMPT,
    }
    system_prompt = prompts.get(role, FONDRAI_SYSTEM_PROMPT)

    formatted_messages = [
        {"role": "system", "content": system_prompt}
    ]

    for message in messages:
        formatted_messages.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

    base_url = (
        AI_BASE_URL or "https://api.groq.com/openai/v1"
    ).rstrip("/")

    # Discover available models, then fall back to the configured model.
    try:
        available_models = _fetch_available_models(base_url)
    except Exception as e:
        logger.warning(
            "Failed to discover available models: %s", str(e)
        )
        available_models = []

    models_to_try = available_models or [AI_MODEL]
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    for model in models_to_try:
        if not model:
            continue

        try:
            response = httpx.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": formatted_messages,
                    "temperature": 0.7,
                    "max_tokens": 800,
                },
                timeout=60.0,
            )

            if response.status_code == 200:
                data = response.json()
                choices = data.get("choices", [])

                if choices:
                    content = choices[0].get("message", {}).get("content")
                    if isinstance(content, str):
                        return content

                logger.warning(
                    "AI provider returned an unexpected response structure."
                )
                continue

            logger.error(
                "Upstream AI provider error: status_code=%s",
                response.status_code,
            )

        except Exception as e:
            logger.warning(
                "AI model request failed for model=%s: %s",
                model,
                str(e),
            )

    logger.error("All AI provider models failed.")

    return (
        "I'm having trouble connecting to the AI provider right now. "
        "Please try again in a moment."
    )


def _fetch_available_models(base_url: str = None) -> List[str]:
    """Fetch available model IDs from the configured AI provider."""

    if not AI_API_KEY:
        return []

    if base_url is None:
        base_url = (
            AI_BASE_URL or "https://api.groq.com/openai/v1"
        ).rstrip("/")

    response = httpx.get(
        f"{base_url}/models",
        headers={
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30.0,
    )

    if response.status_code != 200:
        logger.warning(
            "Failed to fetch available models: status_code=%s",
            response.status_code,
        )
        return []

    data = response.json()

    return [
        model["id"]
        for model in data.get("data", [])
        if model.get("id")
    ]
