"""Azure AI Search implementation of the RAG search provider."""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from .interfaces import SearchProvider


class AzureAISearchProvider(SearchProvider):
    """Vector search against an existing Azure AI Search index."""

    def __init__(
        self,
        endpoint: str,
        index_name: str,
        api_key: str,
        vector_field: str = "contentVector",
        content_field: str = "content",
    ) -> None:
        self.vector_field = vector_field
        self.content_field = content_field
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
        )

    def search(self, query_vector: list[float], top_k: int) -> list[str]:
        """Run vector search and return only the requested content field."""
        vector_query = VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=top_k,
            fields=self.vector_field,
        )

        results = self.client.search(
            search_text=None,
            vector_queries=[vector_query],
            top=top_k,
            select=[self.content_field],
        )

        return [
            str(result[self.content_field])
            for result in results
            if result.get(self.content_field)
        ]
