from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from pypdf import PdfReader

from app.config import CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL


def get_embeddings() -> Embeddings:
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


def load_pdf(path: Path) -> list[Document]:
    """One Document per page, with the file name and page number as metadata."""
    reader = PdfReader(path)
    return [
        Document(page_content=page.extract_text() or "", metadata={"source": path.name, "page": number})
        for number, page in enumerate(reader.pages, start=1)
    ]


def chunk(pages: list[Document]) -> list[Document]:
    """Split each page into fixed-size pieces of text."""
    step = CHUNK_SIZE - CHUNK_OVERLAP
    chunks = []
    for page in pages:
        text = page.page_content
        for start in range(0, len(text), step):
            piece = text[start : start + CHUNK_SIZE]
            if piece.strip():
                chunks.append(Document(page_content=piece, metadata=dict(page.metadata)))
    return chunks


def build_index(paths: list[Path], embeddings: Embeddings) -> FAISS:
    chunks = [c for path in paths for c in chunk(load_pdf(path))]
    return FAISS.from_documents(chunks, embeddings)


def add_to_index(index: FAISS, path: Path) -> int:
    """Add one PDF to an existing index. Returns the number of chunks added."""
    chunks = chunk(load_pdf(path))
    if chunks:
        index.add_documents(chunks)
    return len(chunks)
