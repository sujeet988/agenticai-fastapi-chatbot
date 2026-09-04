"""Small, provider-independent RAG service."""

from .interfaces import EmbeddingProvider, SearchProvider


class RAGService:
    """Orchestrates query embedding and document retrieval."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        search_provider: SearchProvider,
        default_top_k: int = 5,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.search_provider = search_provider
        self.default_top_k = default_top_k

    def retrieve(self, query: str, top_k: int | None = None) -> list[str]:
        """Embed the query, search the index, and return relevant chunks."""
        if not query.strip():
            return []

        vector = self.embedding_provider.embed_query(query)
        return self.search_provider.search(
            vector,
            top_k or self.default_top_k,
        )

    def retrieve_context(self, query: str, top_k: int | None = None) -> str:
        """Return retrieved chunks formatted as LLM context."""
        return "\n\n".join(self.retrieve(query, top_k))
