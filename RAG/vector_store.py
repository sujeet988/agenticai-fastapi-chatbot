from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from common.config import OPENAI_API_KEY


_documents = [
    Document(page_content="Agentic AI uses an LLM with tools to achieve a goal."),
    Document(page_content="RAG retrieves relevant documents before generating an answer."),
    Document(page_content="MCP provides a standard way for an AI application to use external tools."),
]


_vector_store = InMemoryVectorStore.from_documents(
    _documents,
    embedding=OpenAIEmbeddings(api_key=OPENAI_API_KEY),
)


def retrieve_context(query: str, k: int = 2) -> str:
    docs = _vector_store.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in docs)
