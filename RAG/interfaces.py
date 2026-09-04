"""Interfaces for pluggable RAG components."""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Create embeddings without coupling RAG to a specific model provider."""

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        raise NotImplementedError


class SearchProvider(ABC):
    """Retrieve relevant documents from a search/vector backend."""

    @abstractmethod
    def search(self, query_vector: list[float], top_k: int) -> list[str]:
        raise NotImplementedError
