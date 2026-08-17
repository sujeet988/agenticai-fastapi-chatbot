from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent.ai_agent import get_response_from_ai_agent
from agent.reviewer_agent import run_reviewer_agent


class MultiAgentState(TypedDict, total=False):
    query: str
    model_name: str
    model_provider: str
    system_prompt: str
    agent_one_result: str
    agent_two_result: str
    final_result: str


async def agent_one(state: MultiAgentState) -> dict:
    """Agent 1: existing ReAct agent with MCP tools."""
    result = await get_response_from_ai_agent(
        state["model_name"],
        [state["query"]],
        False,
        state["system_prompt"],
        state["model_provider"],
    )
    return {"agent_one_result": result}


async def agent_two(state: MultiAgentState) -> dict:
    """Agent 2: independent reviewer agent."""
    result = await run_reviewer_agent(
        state["query"],
        state["model_name"],
        state["model_provider"],
    )
    return {"agent_two_result": result}


async def aggregate(state: MultiAgentState) -> dict:
    """Aggregate both agent results into one final response."""
    from agent.ai_agent import get_llm

    llm = get_llm(state["model_name"], state["model_provider"])

    prompt = f"""
You are the aggregator agent.
Combine two specialist results into one concise, accurate answer.
Do not mention internal agents or orchestration.

User question:
{state['query']}

Agent 1 result:
{state['agent_one_result']}

Agent 2 result:
{state['agent_two_result']}
"""

    response = await llm.ainvoke([("system", prompt)])
    return {"final_result": response.content}


# Both specialist agents run from START, then the aggregator waits for both.
graph = StateGraph(MultiAgentState)
graph.add_node("agent_one", agent_one)
graph.add_node("agent_two", agent_two)
graph.add_node("aggregate", aggregate)

graph.add_edge(START, "agent_one")
graph.add_edge(START, "agent_two")
graph.add_edge("agent_one", "aggregate")
graph.add_edge("agent_two", "aggregate")
graph.add_edge("aggregate", END)

multi_agent_graph = graph.compile()


async def run_multi_agent(
    query: str,
    model_name: str,
    model_provider: str,
    system_prompt: str = "You are a helpful AI agent.",
) -> str:
    """Run both agents and return the aggregated answer."""
    result = await multi_agent_graph.ainvoke(
        {
            "query": query,
            "model_name": model_name,
            "model_provider": model_provider,
            "system_prompt": system_prompt,
        }
    )

    return result["final_result"]
