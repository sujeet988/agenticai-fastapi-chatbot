"""Embedding provider implementations."""

from openai import OpenAI

from .interfaces import EmbeddingProvider


class AzureFoundryEmbeddingProvider(EmbeddingProvider):
    """Embedding client for an Azure Foundry OpenAI-compatible endpoint."""

    def __init__(self, endpoint: str, api_key: str, model: str) -> None:
        self.model = model
        self.client = OpenAI(base_url=endpoint, api_key=api_key)

    def embed_query(self, text: str) -> list[float]:
        """Create one embedding for a search query."""
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Create embeddings in one request for efficient document ingestion."""
        if not texts:
            return []
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
