from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agent.tools import calculator, get_product_info
from common.config import GROQ_API_KEY, OPENAI_API_KEY
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from RAG.vector_store import retrieve_context


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


def get_response_from_ai_agent(
    model_name: str,
    messages: list[str],
    allow_search: bool,
    system_prompt: str,
    model_provider: str,
):
    """Simple ReAct agent: LLM decides when to use tools or RAG."""
    llm = get_llm(model_name, model_provider)

    tools = [calculator, get_product_info, search_knowledge_base]
    if not allow_search:
        tools = [calculator, get_product_info]

    agent = create_react_agent(llm, tools)
    prompt = system_prompt + "\nUse tools when they improve the answer. Use the knowledge base for RAG questions."
    conversation = [("system", prompt)] + [("human", message) for message in messages]

    result = agent.invoke({"messages": conversation})
    return result["messages"][-1].content
