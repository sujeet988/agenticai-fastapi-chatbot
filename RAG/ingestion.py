from dataclasses import dataclass
from io import BytesIO

from pypdf import PdfReader

from .chunking import chunk_text


@dataclass(frozen=True)
class DocumentChunk:
    """Text and metadata for one searchable PDF chunk."""

    content: str
    source: str
    page: int
    chunk: int


def extract_pdf_chunks(pdf_bytes: bytes, filename: str) -> list[DocumentChunk]:
    """Extract text page by page, then create overlapping searchable chunks."""
    reader = PdfReader(BytesIO(pdf_bytes))
    chunks = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for chunk_number, content in enumerate(chunk_text(text), start=1):
            chunks.append(DocumentChunk(content, filename, page_number, chunk_number))
    return chunks


KNOWLEDGE_BASE = [
    "Agentic AI uses an LLM with tools to achieve a goal.",
    "RAG retrieves relevant documents and gives them to the LLM as context.",
    "MCP is a standard protocol for connecting AI applications to external tools.",
]


def load_documents() -> list[str]:
    """Return chunked demo knowledge-base documents."""
    chunks = []
    for document in KNOWLEDGE_BASE:
        chunks.extend(chunk_text(document))
    return chunks
