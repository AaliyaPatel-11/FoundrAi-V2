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
    """
    Generate a response based on the complete conversation history.
    Selects the appropriate startup agent based on the requested role.
    Dynamically discovers and uses active models from the AI provider.
    """

    if not AI_API_KEY:
        logger.info(
            "AI_API_KEY is not configured. Using offline development fallback."
        )
        return "FondrAI is online, but its AI provider isn't configured yet."

    # Select the appropriate agent system prompt
    if role == "cfo":
        system_prompt = CFO_SYSTEM_PROMPT
    elif role == "cto":
        system_prompt = CTO_SYSTEM_PROMPT
    elif role == "cmo":
        system_prompt = CMO_SYSTEM_PROMPT
    elif role == "product":
        system_prompt = PRODUCT_SYSTEM_PROMPT
    else:
        system_prompt = FONDRAI_SYSTEM_PROMPT

    # Prepare conversation history payload
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

    # Discover active models from the provider
    try:
        available_models = _fetch_available_models()
    except Exception as e:
        logger.warning(
            f"Failed to discover available models: {str(e)}"
        )
        available_models = []

    models_to_try = available_models or [AI_MODEL]

    last_error = None

    for model in models_to_try:
        try:
            response = httpx.post(
                f"{AI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": formatted_messages,
                    "temperature": 0.7,
                },
                timeout=60.0,
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            logger.error(
                f"Upstream AI provider error: status_code={response.status_code}"
            )
            last_error = response

        except Exception as e:
            logger.warning(
                f"AI model request failed for model={model}: {str(e)}"
            )
            last_error = e

    logger.error("All AI provider models failed.")

    return (
        "I'm having trouble connecting to the AI provider right now. "
        "Please try again in a moment."
    )


def _fetch_available_models() -> List[str]:
    """
    Fetch available models from the configured AI provider.
    """

    response = httpx.get(
        f"{AI_BASE_URL}/models",
        headers={
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30.0,
    )

    if response.status_code != 200:
        logger.warning(
            f"Failed to fetch available models: "
            f"status_code={response.status_code}"
        )
        return []

    data = response.json()

    return [
        model["id"]
        for model in data.get("data", [])
        if model.get("id")
    ]