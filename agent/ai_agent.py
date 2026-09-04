from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from common.config import GROQ_API_KEY, OPENAI_API_KEY
from common.evaluation import BasicResponseEvaluator
from common.mcp_client_adapter import get_mcp_tools
from RAG.factory import create_rag_service


# Keep infrastructure configuration outside the agent logic.
r_response_evaluator = BasicResponseEvaluator()


def get_llm(model_name: str, model_provider: str):
    """Create the configured chat model."""
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
    """Run the ReAct agent, optional RAG, MCP tools, and evaluation."""
    llm = get_llm(model_name, model_provider)
    mcp_tools = get_mcp_tools()

    # RAG is optional: when enabled, retrieve enterprise context first.
    context = ""
    if allow_search and messages:
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

    agent = create_react_agent(llm, mcp_tools)
    result = await agent.ainvoke({"messages": conversation})
    answer = result["messages"][-1].content

    # Evaluation is a separate layer so it can later be replaced by
    # Azure AI Foundry evaluators without changing the agent workflow.
    evaluation = await r_response_evaluator.evaluate(
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
