def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 120,
) -> list[str]:
    """Split text on word boundaries while preserving overlap between chunks."""
    words = " ".join(text.split()).split()
    if not words:
        return []

    chunks = []
    current = []
    current_length = 0
    for word in words:
        added_length = len(word) + (1 if current else 0)
        if current and current_length + added_length > chunk_size:
            chunks.append(" ".join(current))
            overlap_words = []
            overlap_length = 0
            for previous_word in reversed(current):
                word_length = len(previous_word) + (1 if overlap_words else 0)
                if overlap_length + word_length > overlap:
                    break
                overlap_words.append(previous_word)
                overlap_length += word_length
            current = list(reversed(overlap_words))
            current_length = len(" ".join(current))

        current.append(word)
        current_length += added_length

    if current:
        chunks.append(" ".join(current))
    return chunks
