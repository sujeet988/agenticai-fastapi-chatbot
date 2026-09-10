from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from common.config import GROQ_API_KEY, OPENAI_API_KEY, RAG_ENABLED
from common.evaluation import BasicResponseEvaluator
from common.Logging.observability import get_trace_config
from common.mcp_client_adapter import get_mcp_tools
from RAG.factory import create_rag_service


# Keep evaluation independent from the agent implementation.
response_evaluator = BasicResponseEvaluator()


def get_llm(model_name: str, model_provider: str):
    """Create the configured chat model."""
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
    include_execution_details: bool = False,
):
    """Run the ReAct agent with optional RAG, MCP tools, and evaluation."""
    llm = get_llm(model_name, model_provider)
    mcp_tools = get_mcp_tools()

    # RAG is optional. The configured provider handles embeddings + retrieval.
    context = ""
    if RAG_ENABLED and allow_search and messages:
        context = create_rag_service().retrieve_context(messages[-1])

    prompt = system_prompt + "\nUse the available MCP tools when appropriate."
    if context:
        prompt += (
            "\n\nUse the following retrieved context to ground your answer. "
            "If the context does not contain the answer, say so.\n\n"
            f"Retrieved context:\n{context}"
        )

    conversation = [("system", prompt)] + [
        ("human", message) for message in messages
    ]

    trace_config = get_trace_config(
        run_name="agent_hub_chat",
        metadata={
            "model_name": model_name,
            "model_provider": model_provider,
            "rag_enabled": bool(context),
            "allow_search": allow_search,
        },
    )

    agent = create_react_agent(llm, mcp_tools)
    result = await agent.ainvoke(
        {"messages": conversation},
        config=trace_config,
    )
    answer = result["messages"][-1].content

    # Evaluation is a replaceable layer; Azure AI Foundry evaluators can be
    # plugged in later without changing the agent workflow.
    evaluation = await response_evaluator.evaluate(
        question=messages[-1] if messages else "",
        answer=answer,
        context=context,
    )

    if not include_execution_details:
        return answer

    tool_calls = []
    for message in result["messages"]:
        if getattr(message, "type", "") == "tool":
            tool_calls.append(
                {
                    "name": getattr(message, "name", "unknown"),
                    "result": getattr(message, "content", ""),
                }
            )

    return {
        "answer": answer,
        "evaluation": evaluation,
        "execution": {
            "agents_called": 1,
            "execution_path": ["tool_agent"],
            "tool_called": bool(tool_calls),
            "tools": tool_calls,
        },
    }
