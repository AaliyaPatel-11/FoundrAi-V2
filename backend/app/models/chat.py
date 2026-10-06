from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "foundrai"
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    role: Optional[str] = None

class ChoiceMessage(BaseModel):
    role: str = "assistant"
    content: str

class Choice(BaseModel):
    index: int = 0
    message: ChoiceMessage
    finish_reason: str = "stop"

class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str = "fondrai"
    choices: List[Choice]
    usage: Usage = Field(default_factory=Usage)
