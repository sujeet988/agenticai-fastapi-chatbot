from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from common.config import (
    GROQ_API_KEY,
    OPENAI_API_KEY
)


def get_llm(
    model_name: str,
    model_provider: str
):
    """
    Create LLM based on provider.
    """

    if model_provider == "Groq":

        return ChatGroq(
            model=model_name,
            api_key=GROQ_API_KEY,
            temperature=0
        )

    elif model_provider == "OpenAI":

        return ChatOpenAI(
            model=model_name,
            api_key=OPENAI_API_KEY,
            temperature=0
        )

    else:

        raise ValueError(
            f"Unsupported model provider: {model_provider}"
        )


def get_response_from_ai_agent(
    model_name: str,
    messages: list[str],
    allow_search: bool,
    system_prompt: str,
    model_provider: str
):
    """
    Execute the AI agent.

    RAG and MCP will be added here later.
    """

    llm = get_llm(
        model_name,
        model_provider
    )

    # Currently we are not using web search.
    # It will be added as a tool later.

    conversation = [
        (
            "system",
            system_prompt
        )
    ]

    for message in messages:

        conversation.append(
            (
                "human",
                message
            )
        )

    response = llm.invoke(
        conversation
    )

    return response.content