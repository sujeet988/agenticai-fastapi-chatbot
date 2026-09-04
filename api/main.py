from fastapi import FastAPI, File, HTTPException, UploadFile

from agent.ai_agent import get_response_from_ai_agent
from agent.multi_agent_graph import run_multi_agent
from common.config import API_HOST, API_PORT
from common.models import ChatRequest, MultiAgentRequest, RagRequest
from RAG.retriever import retrieve_context
from RAG.ingestion import extract_pdf_chunks
from RAG.factory import create_rag_service


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
        request.include_execution_details,
    )


@app.post("/multi-agent")
async def multi_agent_endpoint(request: MultiAgentRequest):
    """Run two agents, aggregate their results, optionally return trace details."""
    if request.model_name not in ALLOWED_MODELS:
        return {
            "error": "Invalid model name. Kindly select a valid AI model."
        }

    if not request.query.strip():
        return {"error": "Please provide a question."}

    return await run_multi_agent(
        query=request.query,
        model_name=request.model_name,
        model_provider=request.model_provider,
        system_prompt=request.system_prompt,
        include_execution_details=request.include_execution_details,
    )


@app.post("/rag")
def rag_endpoint(request: RagRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Please provide a question.")
    return {
        "query": request.query,
        "context": retrieve_context(request.query, request.top_k),
    }


@app.post("/rag/upload")
async def rag_upload_endpoint(file: UploadFile = File(...)):
    """Extract, chunk, embed, and index one PDF in Azure AI Search."""
    filename = file.filename or "uploaded.pdf"
    if file.content_type != "application/pdf" and not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")

    try:
        chunks = extract_pdf_chunks(pdf_bytes, filename)
        indexed = create_rag_service().ingest(chunks)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF ingestion failed: {exc}") from exc

    return {
        "filename": filename,
        "chunks": len(chunks),
        "indexed": indexed,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
    )
