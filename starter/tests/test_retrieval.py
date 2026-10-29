from app.config import TOP_K
from app.retrieval import make_search_tool


def test_search_returns_top_k_passages(small_index):
    search = make_search_tool(small_index)
    result = search.invoke({"query": "agents"})
    assert len(result.split("\n\n")) == TOP_K
    assert all(part.startswith("Passage number") for part in result.split("\n\n"))
