from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from common.mcp_client_adapter import get_mcp_tools
from common.config import GROQ_API_KEY, OPENAI_API_KEY


def get_llm(model_name: str, model_provider: str):
    if model_provider == "Groq":
        return ChatGroq(
            model=model_name,
            api_key=GROQ_API_KEY,
            temperature=0,
        )

    if model_provider == "OpenAI":
        return ChatOpenAI(
            model=model_name,
            api_key=OPENAI_API_KEY,
            temperature=0,
        )

    raise ValueError(f"Unsupported model provider: {model_provider}")


async def get_response_from_ai_agent(
    model_name: str,
    messages: list[str],
    allow_search: bool,
    system_prompt: str,
    model_provider: str,
    include_execution_details: bool = False,
):
    """Run the ReAct agent and optionally return tool execution details."""
    del allow_search  # RAG will be added separately after MCP is verified.

    llm = get_llm(model_name, model_provider)
    mcp_tools = get_mcp_tools()

    prompt = (
        system_prompt
        + "\nUse the available MCP tools when they are appropriate."
    )

    conversation = [("system", prompt)] + [
        ("human", message) for message in messages
    ]

    agent = create_react_agent(llm, mcp_tools)
    result = await agent.ainvoke({"messages": conversation})

    answer = result["messages"][-1].content

    if not include_execution_details:
        return answer

    # LangGraph records tool calls/results as messages in the execution state.
    tool_calls = []
    for message in result["messages"]:
        message_type = getattr(message, "type", "")
        if message_type == "tool":
            tool_calls.append(
                {
                    "name": getattr(message, "name", "unknown"),
                    "result": getattr(message, "content", ""),
                }
            )

    return {
        "answer": answer,
        "execution": {
            "agents_called": 1,
            "execution_path": ["tool_agent"],
            "tool_called": bool(tool_calls),
            "tools": tool_calls,
        },
    }
