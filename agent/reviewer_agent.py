from langchain_core.messages import HumanMessage

from agent.ai_agent import get_llm


async def run_reviewer_agent(
    query: str,
    model_name: str,
    model_provider: str,
) -> str:
    """Second specialist: independently reviews the user's question."""
    llm = get_llm(model_name, model_provider)

    prompt = (
        "You are a review agent. Analyze the user's question independently. "
        "Give a concise answer and mention important assumptions."
    )

    response = await llm.ainvoke(
        [
            ("system", prompt),
            HumanMessage(content=query),
        ]
    )

    return response.content
