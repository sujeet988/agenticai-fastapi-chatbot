"""Backward-compatible RAG retrieval entry point."""

from .factory import create_rag_service


# Keep the API layer simple while the implementation stays behind RAGService.
def retrieve_context(query: str, k: int = 5) -> str:
    """Retrieve grounded context from the configured Azure AI Search index."""
    return create_rag_service().retrieve_context(query, k)
