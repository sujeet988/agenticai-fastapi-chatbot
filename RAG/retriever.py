from .ingestion import load_documents


DOCUMENTS = load_documents()


def retrieve_context(query: str, k: int = 2) -> str:
    """Simple lexical retriever for the demo RAG pipeline."""
    words = set(query.lower().split())
    ranked = sorted(
        DOCUMENTS,
        key=lambda document: len(words & set(document.lower().split())),
        reverse=True,
    )
    return "\n\n".join(ranked[:k])
