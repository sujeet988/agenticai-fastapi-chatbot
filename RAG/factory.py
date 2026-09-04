"""Build the configured RAG service."""

from .azure_search import AzureAISearchProvider
from .config import RAGConfig
from .embeddings import AzureFoundryEmbeddingProvider
from .service import RAGService


def create_rag_service(config: RAGConfig | None = None) -> RAGService:
    """Create RAG with Azure AI Search and Azure Foundry embeddings."""
    config = config or RAGConfig.from_env()

    embedding = AzureFoundryEmbeddingProvider(
        endpoint=config.embedding_endpoint,
        api_key=config.embedding_api_key,
        model=config.embedding_model,
    )

    search = AzureAISearchProvider(
        endpoint=config.search_endpoint,
        index_name=config.search_index,
        api_key=config.search_api_key,
        vector_field=config.vector_field,
        content_field=config.content_field,
    )

    return RAGService(embedding, search, config.default_top_k)
