from fastapi import FastAPI
from common.models import ChatRequest
from agent.ai_agent import get_response_from_ai_agent


ALLOWED_MODELS = [
    "openai/gpt-oss-120b",
    "gpt-4o-mini"
]


app = FastAPI(
    title="Agent Hub API",
    description="Agentic AI Chatbot API",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "message": "Agent Hub API is running"
    }


@app.post("/chat")
def chat_endpoint(
    request: ChatRequest
):

    if request.model_name not in ALLOWED_MODELS:

        return {
            "error": (
                "Invalid model name. "
                "Kindly select a valid AI model."
            )
        }

    response = get_response_from_ai_agent(
        request.model_name,
        request.messages,
        request.allow_search,
        request.system_prompt,
        request.model_provider
    )

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=9999,
        reload=True
    )