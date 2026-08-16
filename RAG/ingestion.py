from .chunking import chunk_text


KNOWLEDGE_BASE = [
    "Agentic AI uses an LLM with tools to achieve a goal.",
    "RAG retrieves relevant documents and gives them to the LLM as context.",
    "MCP is a standard protocol for connecting AI applications to external tools.",
]


def load_documents() -> list[str]:
    """Return chunked demo knowledge-base documents."""
    chunks = []
    for document in KNOWLEDGE_BASE:
        chunks.extend(chunk_text(document))
    return chunks
