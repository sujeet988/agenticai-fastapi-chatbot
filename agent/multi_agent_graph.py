from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent.ai_agent import get_response_from_ai_agent, get_llm
from agent.reviewer_agent import run_reviewer_agent


class MultiAgentState(TypedDict, total=False):
    query: str
    model_name: str
    model_provider: str
    system_prompt: str
    agent_one_result: str
    agent_two_result: str
    final_result: str
    agent_one_execution: dict
    agent_two_execution: dict


async def agent_one(state: MultiAgentState) -> dict:
    """Agent 1: ReAct agent that can use MCP tools."""
    result = await get_response_from_ai_agent(
        state["model_name"],
        [state["query"]],
        False,
        state["system_prompt"],
        state["model_provider"],
        include_execution_details=True,
    )

    return {
        "agent_one_result": result["answer"],
        "agent_one_execution": result["execution"],
    }


async def agent_two(state: MultiAgentState) -> dict:
    """Agent 2: independent reviewer; it does not call tools."""
    result = await run_reviewer_agent(
        state["query"],
        state["model_name"],
        state["model_provider"],
    )

    return {
        "agent_two_result": result,
        "agent_two_execution": {
            "name": "reviewer_agent",
            "status": "completed",
            "tool_called": False,
            "tools": [],
        },
    }


async def aggregate(state: MultiAgentState) -> dict:
    """Aggregate both agent results into one final response."""
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


# Fan-out: both agents start together; aggregation waits for both.
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
    include_execution_details: bool = False,
):
    """Run both agents and optionally return execution details."""
    result = await multi_agent_graph.ainvoke(
        {
            "query": query,
            "model_name": model_name,
            "model_provider": model_provider,
            "system_prompt": system_prompt,
        }
    )

    if not include_execution_details:
        return result["final_result"]

    return {
        "answer": result["final_result"],
        "execution": {
            "agents_called": 2,
            "execution_path": [
                "tool_agent",
                "reviewer_agent",
                "aggregator",
            ],
            "agents": [
                result["agent_one_execution"],
                result["agent_two_execution"],
                {
                    "name": "aggregator",
                    "status": "completed",
                    "tool_called": False,
                    "tools": [],
                },
            ],
        },
    }
