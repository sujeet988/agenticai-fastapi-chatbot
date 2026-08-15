from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

class ChatResponse(BaseModel):
    content: str