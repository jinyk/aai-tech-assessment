from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_core.tools import BaseTool, tool

from app.config import INDEX_DIR, TOP_K


def load_index(embeddings: Embeddings) -> FAISS:
    if not (INDEX_DIR / "index.faiss").exists():
        raise SystemExit(f"No index in {INDEX_DIR}. Run: uv run ingest.py")
    # The index is a file this project wrote itself.
    return FAISS.load_local(str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True)


def make_search_tool(index: FAISS) -> BaseTool:
    @tool
    def search_documents(query: str) -> str:
        """Search the documents for passages that match the query."""
        docs = index.similarity_search(query, k=TOP_K)
        return "\n\n".join(doc.page_content for doc in docs)

    return search_documents
