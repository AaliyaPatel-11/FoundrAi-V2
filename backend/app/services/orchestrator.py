from app.services.ai_service import generate_response
from app.models.chat import ChatMessage


def run_agent(messages: list[ChatMessage], role: str = None) -> str:
    """
    Route the conversation to the appropriate AI agent.
    """

    if role == "cfo":
        return generate_response(messages, role="cfo")

    return generate_response(messages, role=None)