import pytest
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding


@pytest.fixture
def embeddings():
    return DeterministicFakeEmbedding(size=64)


@pytest.fixture
def small_index(embeddings):
    docs = [
        Document(page_content=f"Passage number {i} about agents.", metadata={"source": f"paper{i % 2}.pdf", "page": i})
        for i in range(10)
    ]
    return FAISS.from_documents(docs, embeddings)
