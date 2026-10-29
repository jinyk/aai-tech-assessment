from deepagents import create_deep_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from app.config import MODEL

SYSTEM_PROMPT = """You answer questions about a set of research papers.

Before you answer, call search_documents with the user's question as the query.
Answer from the search result. Keep the answer short and direct.
Do not use the file, todo or task tools."""


def build_agent(search_tool: BaseTool, model: BaseChatModel | None = None):
    return create_deep_agent(
        model=model or ChatOpenAI(model=MODEL),
        tools=[search_tool],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )


def ask(agent, message: str, thread_id: str) -> str:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    return result["messages"][-1].text
