"""Small, provider-independent RAG service."""

from .interfaces import EmbeddingProvider, SearchProvider
from .ingestion import DocumentChunk


class RAGService:
    """Orchestrates query embedding and document retrieval."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        search_provider: SearchProvider,
        default_top_k: int = 5,
        vector_field: str = "contentVector",
    ) -> None:
        self.embedding_provider = embedding_provider
        self.search_provider = search_provider
        self.default_top_k = default_top_k
        self.vector_field = vector_field

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

    def ingest(self, chunks: list[DocumentChunk]) -> int:
        """Embed and store document chunks in the configured vector backend."""
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_provider.embed_documents(texts)
        documents = [
            {
                "id": f"{chunk.source}-{chunk.page}-{chunk.chunk}".replace(" ", "-").lower(),
                "content": chunk.content,
                self.vector_field: embedding,
                "source": chunk.source,
                "page": chunk.page,
            }
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        return self.search_provider.add_documents(documents)
