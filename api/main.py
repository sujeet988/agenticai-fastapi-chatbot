from fastapi import FastAPI

from common.models import (
    ChatRequest,
    ChatResponse
)

from common.constants import ALLOWED_MODELS

from agent.ai_agent import (
    get_response_from_ai_agent
)


app = FastAPI(
    title="Agent Hub API",
    description="Agentic AI API using FastAPI",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "message": "Agent Hub API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat_endpoint(
    request: ChatRequest
):

    # -----------------------------
    # Validate provider
    # -----------------------------

    if request.model_provider not in ALLOWED_MODELS:

        return ChatResponse(
            content=(
                "Invalid model provider. "
                "Please select a valid provider."
            )
        )

    # -----------------------------
    # Validate model
    # -----------------------------

    allowed_models = ALLOWED_MODELS[
        request.model_provider
    ]

    if request.model_name not in allowed_models:

        return ChatResponse(
            content=(
                f"Invalid model '{request.model_name}' "
                f"for provider '{request.model_provider}'."
            )
        )

    # -----------------------------
    # Call Agent
    # -----------------------------

    response = get_response_from_ai_agent(
        model_name=request.model_name,
        messages=request.messages,
        allow_search=request.allow_search,
        system_prompt=request.system_prompt,
        model_provider=request.model_provider
    )

    return ChatResponse(
        content=response
    )