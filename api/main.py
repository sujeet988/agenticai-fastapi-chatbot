from fastapi import FastAPI

from agent.ai_agent import get_response_from_ai_agent
from common.models import ChatRequest, RagRequest
from RAG.retriever import retrieve_context


ALLOWED_MODELS = [
    "openai/gpt-oss-120b",
    "gpt-4o-mini",
]


app = FastAPI(
    title="Agent Hub API",
    description="Agentic AI API with MCP and standalone RAG",
    version="1.1.0",
)


@app.get("/")
def root():
    return {"message": "Agent Hub API is running"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if request.model_name not in ALLOWED_MODELS:
        return {
            "error": "Invalid model name. Kindly select a valid AI model."
        }

    return await get_response_from_ai_agent(
        request.model_name,
        request.messages,
        request.allow_search,
        request.system_prompt,
        request.model_provider,
    )


@app.post("/rag")
def rag_endpoint(request: RagRequest):
    return {
        "query": request.query,
        "context": retrieve_context(request.query, request.top_k),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=9999,
        reload=True,
    )
