"""Configuration for the RAG service."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RAGConfig:
    """Keep RAG infrastructure settings in one place."""

    search_endpoint: str
    search_index: str
    search_api_key: str
    vector_field: str = "contentVector"
    content_field: str = "content"
    embedding_model: str = "text-embedding-3-small"
    default_top_k: int = 5

    @classmethod
    def from_env(cls) -> "RAGConfig":
        """Build configuration from environment variables."""
        return cls(
            search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT", ""),
            search_index=os.getenv("AZURE_SEARCH_INDEX", ""),
            search_api_key=os.getenv("AZURE_SEARCH_API_KEY", ""),
            vector_field=os.getenv("AZURE_SEARCH_VECTOR_FIELD", "contentVector"),
            content_field=os.getenv("AZURE_SEARCH_CONTENT_FIELD", "content"),
            embedding_model=os.getenv(
                "AZURE_FOUNDRY_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
            default_top_k=int(os.getenv("RAG_TOP_K", "5")),
        )
