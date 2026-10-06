import time
import uuid
import logging
from fastapi import APIRouter, HTTPException
from httpx import request
from app.models.chat import ChatCompletionRequest, ChatCompletionResponse, Choice, ChoiceMessage, Usage
from app.services.orchestrator import run_agent

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    try:
        # Generate the response through the agent orchestrator
        content = run_agent(request.messages, request.role)

        # Construct OpenAI-compatible response format
        response_id = f"chatcmpl-fondrai-{uuid.uuid4().hex[:8]}"
        created_time = int(time.time())

        choice = Choice(
            index=0,
            message=ChoiceMessage(
                role="assistant",
                content=content
            ),
            finish_reason="stop"
        )

        return ChatCompletionResponse(
            id=response_id,
            object="chat.completion",
            created=created_time,
            model=request.model,
            choices=[choice],
            usage=Usage(
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0
            )
        )

    except Exception as e:
        logger.error(
            f"Failed to process chat completions request: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the chat completion."
        )