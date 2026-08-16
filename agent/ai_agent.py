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
):
    """Simple ReAct agent using only remote MCP tools for now."""
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

    return result["messages"][-1].content
