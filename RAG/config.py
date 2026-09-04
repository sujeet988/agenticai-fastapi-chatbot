"""Configuration for the RAG service."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RAGConfig:
    """All RAG infrastructure settings live in one configurable object."""

    search_endpoint: str
    search_index: str
    search_api_key: str
    embedding_endpoint: str
    embedding_api_key: str
    embedding_model: str
    vector_field: str = "contentVector"
    content_field: str = "content"
    default_top_k: int = 5

    @classmethod
    def from_env(cls) -> "RAGConfig":
        """Build configuration from environment variables."""
        return cls(
            search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT", ""),
            search_index=os.getenv("AZURE_SEARCH_INDEX", ""),
            search_api_key=os.getenv("AZURE_SEARCH_API_KEY", ""),
            embedding_endpoint=os.getenv("AZURE_FOUNDRY_ENDPOINT", ""),
            embedding_api_key=os.getenv("AZURE_FOUNDRY_API_KEY", ""),
            embedding_model=os.getenv("AZURE_FOUNDRY_EMBEDDING_MODEL", ""),
            vector_field=os.getenv("AZURE_SEARCH_VECTOR_FIELD", "contentVector"),
            content_field=os.getenv("AZURE_SEARCH_CONTENT_FIELD", "content"),
            default_top_k=int(os.getenv("RAG_TOP_K", "5")),
        )
