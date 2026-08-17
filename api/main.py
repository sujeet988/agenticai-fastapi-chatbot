from fastapi import FastAPI

from agent.ai_agent import get_response_from_ai_agent
from agent.multi_agent_graph import run_multi_agent
from common.config import API_HOST, API_PORT
from common.models import ChatRequest, RagRequest
from RAG.retriever import retrieve_context


ALLOWED_MODELS = [
    "openai/gpt-oss-120b",
    "gpt-4o-mini",
]


app = FastAPI(
    title="Agent Hub API",
    description="Agentic AI API with MCP, multi-agent graph, and standalone RAG",
    version="1.2.0",
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


@app.post("/multi-agent")
async def multi_agent_endpoint(request: ChatRequest):
    """Run two agents, aggregate their results, and return one answer."""
    if request.model_name not in ALLOWED_MODELS:
        return {
            "error": "Invalid model name. Kindly select a valid AI model."
        }

    query = request.messages[-1] if request.messages else ""

    if not query.strip():
        return {"error": "Please provide a question."}

    return await run_multi_agent(
        query=query,
        model_name=request.model_name,
        model_provider=request.model_provider,
        system_prompt=request.system_prompt,
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
        host=API_HOST,
        port=API_PORT,
        reload=True,
    )
