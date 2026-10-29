# Paper Chat

A small chat bot that answers questions about the PDF papers in `docs/papers/`.
The tasks are in `README.html`, one folder up.

## Run it

| What | Command |
|---|---|
| Install | `uv sync` |
| Build the search index | `uv run ingest.py` |
| Chat page | `uv run uvicorn app.server:app`, then open http://localhost:8000 |
| Ask one question | `uv run ask.py "your question"` |
| Tests (no key needed) | `uv run pytest` |
| Download the papers again | `uv run fetch_papers.py` |

Copy `.env.example` to `.env` and put an OpenAI key in it before you build the index or ask a question.

## Files

| File | What it does |
|---|---|
| `app/config.py` | Paths and settings |
| `app/ingest.py` | Reads PDFs, splits the text into passages, adds them to the index |
| `app/retrieval.py` | Loads the index; the `search_documents` tool |
| `app/agent.py` | The agent: model, tool and instructions |
| `app/server.py` | The web server: `GET /`, `POST /chat`, `POST /upload` |
| `static/index.html` | The chat page |
