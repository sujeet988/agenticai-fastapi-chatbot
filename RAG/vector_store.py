from langchain_core.documents import Document


# Small local knowledge base for the RAG demo.
_documents = [
    Document(page_content="Agentic AI uses an LLM with tools to achieve a goal."),
    Document(page_content="RAG retrieves relevant documents and gives them to the LLM as context."),
    Document(page_content="MCP is a standard protocol for connecting AI applications to external tools."),
]


def retrieve_context(query: str, k: int = 2) -> str:
    """Simple lexical retrieval for the RAG demo; no external vector DB is required."""
    words = set(query.lower().split())
    ranked = sorted(
        _documents,
        key=lambda doc: len(words & set(doc.page_content.lower().split())),
        reverse=True,
    )
    return "\n\n".join(doc.page_content for doc in ranked[:k])
