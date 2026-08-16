def chunk_text(text: str, chunk_size: int = 300) -> list[str]:
    """Split text into small chunks for the demo RAG pipeline."""
    text = " ".join(text.split())
    return [
        text[i : i + chunk_size]
        for i in range(0, len(text), chunk_size)
        if text[i : i + chunk_size]
    ]
