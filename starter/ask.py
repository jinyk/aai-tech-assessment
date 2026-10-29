"""Ask one question from the terminal: uv run ask.py "What is ReAct?" """

import sys
import uuid

from app.agent import ask, build_agent
from app.ingest import get_embeddings
from app.retrieval import load_index, make_search_tool


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: uv run ask.py "your question"')
    question = " ".join(sys.argv[1:])
    agent = build_agent(make_search_tool(load_index(get_embeddings())))
    print(ask(agent, question, thread_id=str(uuid.uuid4())))


if __name__ == "__main__":
    main()
