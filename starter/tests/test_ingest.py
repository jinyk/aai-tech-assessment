from langchain_core.documents import Document

from app.config import CHUNK_SIZE
from app.ingest import chunk


def test_chunk_splits_page_into_fixed_pieces():
    page = Document(page_content="x" * (CHUNK_SIZE * 2 + 10), metadata={"source": "a.pdf", "page": 3})
    chunks = chunk([page])
    assert [len(c.page_content) for c in chunks] == [CHUNK_SIZE, CHUNK_SIZE, 10]


def test_chunk_keeps_source_and_page():
    page = Document(page_content="Some text on a page.", metadata={"source": "a.pdf", "page": 3})
    (only,) = chunk([page])
    assert only.metadata == {"source": "a.pdf", "page": 3}


def test_chunk_skips_empty_pages():
    assert chunk([Document(page_content="   ", metadata={"source": "a.pdf", "page": 1})]) == []
