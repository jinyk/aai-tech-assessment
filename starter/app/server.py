from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app import config
from app.agent import ask, build_agent
from app.ingest import add_to_index, get_embeddings
from app.retrieval import load_index, make_search_tool


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tests put their own index and agent on app.state first.
    if not hasattr(app.state, "index"):
        app.state.index = load_index(get_embeddings())
        app.state.agent = build_agent(make_search_tool(app.state.index))
    yield


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def page() -> FileResponse:
    return FileResponse(config.ROOT / "static" / "index.html")


@app.post("/chat")
def chat(body: ChatRequest, request: Request) -> ChatResponse:
    return ChatResponse(answer=ask(request.app.state.agent, body.message, body.thread_id))


@app.post("/upload")
def upload(file: UploadFile, request: Request) -> dict:
    name = Path(file.filename or "").name
    if not name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    config.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    path = config.UPLOADS_DIR / name
    path.write_bytes(file.file.read())
    index = request.app.state.index
    added = add_to_index(index, path)
    index.save_local(str(config.INDEX_DIR))
    return {"file": name, "chunks": added}
