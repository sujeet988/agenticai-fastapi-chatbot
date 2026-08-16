from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from MCP.client import get_mcp_tools
from RAG.vector_store import retrieve_context
from common.config import GROQ_API_KEY, OPENAI_API_KEY
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


@tool
def search_knowledge_base(query: str) -> str:
    """Retrieve relevant information from the local RAG knowledge base."""
    return retrieve_context(query)


def get_llm(model_name: str, model_provider: str):
    if model_provider == "Groq":
        return ChatGroq(model=model_name, api_key=GROQ_API_KEY, temperature=0)
    if model_provider == "OpenAI":
        return ChatOpenAI(model=model_name, api_key=OPENAI_API_KEY, temperature=0)
    raise ValueError(f"Unsupported model provider: {model_provider}")


async def get_response_from_ai_agent(
    model_name: str,
    messages: list[str],
    allow_search: bool,
    system_prompt: str,
    model_provider: str,
):
    """ReAct agent using remote MCP tools plus the local RAG retriever."""
    llm = get_llm(model_name, model_provider)

    # The MCP client creates async LangChain wrappers for the remote tools.
    mcp_tools = get_mcp_tools()
    tools = mcp_tools + ([search_knowledge_base] if allow_search else [])

    agent = create_react_agent(llm, tools)
    prompt = system_prompt + "\nUse MCP tools when appropriate. Use the knowledge base for RAG questions."
    conversation = [("system", prompt)] + [("human", message) for message in messages]

    result = await agent.ainvoke({"messages": conversation})
    return result["messages"][-1].content
