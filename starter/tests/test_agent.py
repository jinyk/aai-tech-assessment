from langchain_core.messages import ToolMessage

from app.agent import ask, build_agent
from app.retrieval import make_search_tool
from tests.fakes import fake_model


def test_agent_calls_search_and_answers(small_index):
    agent = build_agent(make_search_tool(small_index), model=fake_model())
    answer = ask(agent, "What is ReAct?", thread_id="t1")
    assert answer == "ReAct mixes reasoning and acting."

    state = agent.get_state({"configurable": {"thread_id": "t1"}})
    tool_results = [m for m in state.values["messages"] if isinstance(m, ToolMessage)]
    assert [m.name for m in tool_results] == ["search_documents"]
    assert "Passage number" in tool_results[0].content
