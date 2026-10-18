
from app.services.ai_service import generate_response
from app.models.chat import ChatMessage


SUPPORTED_ROLES = {
    "founder",
    "cfo",
    "cto",
    "cmo",
    "product",
}


def run_agent(messages: list[ChatMessage], role: str = None) -> str:
    """Route the conversation to the appropriate AI agent."""

    if role not in SUPPORTED_ROLES:
        role = "founder"

    if role == "founder":
        return generate_response(messages, role=None)

    return generate_response(messages, role=role)
