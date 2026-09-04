"""Build the configured RAG service."""

import os

from .azure_search import AzureAISearchProvider
from .config import RAGConfig
from .embeddings import AzureFoundryEmbeddingProvider
from .service import RAGService


def create_rag_service(config: RAGConfig | None = None) -> RAGService:
    """Create RAG using Azure AI Search + Azure Foundry embeddings."""
    config = config or RAGConfig.from_env()

    embedding = AzureFoundryEmbeddingProvider(
        endpoint=os.getenv("AZURE_FOUNDRY_ENDPOINT", ""),
        api_key=os.getenv("AZURE_FOUNDRY_API_KEY", ""),
        model=config.embedding_model,
    )

    search = AzureAISearchProvider(
        endpoint=config.search_endpoint,
        index_name=config.search_index,
        api_key=config.search_api_key,
        vector_field=config.vector_field,
        content_field=config.content_field,
    )

    return RAGService(
        embedding_provider=embedding,
        search_provider=search,
        default_top_k=config.default_top_k,
    )
