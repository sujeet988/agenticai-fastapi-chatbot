from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool = False
    include_execution_details: bool = False


class RagRequest(BaseModel):
    query: str
    top_k: int = 2


class MultiAgentRequest(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str = "You are a helpful AI agent."
    query: str
    include_execution_details: bool = False
