import pytest
from fastapi.testclient import TestClient

from app import config
from app.agent import build_agent
from app.retrieval import make_search_tool
from app.server import app
from tests.fakes import fake_model, make_pdf


@pytest.fixture
def client(small_index, tmp_path, monkeypatch):
    monkeypatch.setattr(config, "UPLOADS_DIR", tmp_path / "docs")
    monkeypatch.setattr(config, "INDEX_DIR", tmp_path / "index")
    app.state.index = small_index
    app.state.agent = build_agent(make_search_tool(small_index), model=fake_model())
    with TestClient(app) as test_client:
        yield test_client
    del app.state.index, app.state.agent


def test_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Paper Chat" in response.text


def test_chat_returns_answer(client):
    response = client.post("/chat", json={"message": "What is ReAct?", "thread_id": "t1"})
    assert response.status_code == 200
    assert response.json() == {"answer": "ReAct mixes reasoning and acting."}


def test_upload_adds_pdf_to_index(client, small_index, tmp_path):
    before = small_index.index.ntotal
    files = {"file": ("notes.pdf", make_pdf("Uploaded notes about planning."), "application/pdf")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json() == {"file": "notes.pdf", "chunks": 1}
    assert small_index.index.ntotal == before + 1
    assert (tmp_path / "docs" / "notes.pdf").exists()
    assert (tmp_path / "index" / "index.faiss").exists()


def test_upload_rejects_non_pdf(client):
    response = client.post("/upload", files={"file": ("notes.txt", b"hello", "text/plain")})
    assert response.status_code == 400
