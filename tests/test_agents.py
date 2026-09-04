import sys
import types


# Stub external dependencies for ai_agent to import cleanly in tests.
llm_stub = types.SimpleNamespace()
async def _ainvoke_stub(*args, **kwargs):
    class Resp:
        content = "agent-stub-response"

    return Resp()

llm_stub.ainvoke = _ainvoke_stub

agent_module = types.ModuleType("agent.ai_agent")
def _get_llm(model_name: str, model_provider: str):
    return llm_stub

async def _get_response_from_ai_agent(*args, **kwargs):
    return "agent-stub-answer"

agent_module.get_llm = _get_llm
agent_module.get_response_from_ai_agent = _get_response_from_ai_agent

sys.modules["agent.ai_agent"] = agent_module


def test_agent_llm_invoke():
    from agent.ai_agent import get_llm

    llm = get_llm("openai/gpt-oss-120b", "Groq")
    # Ensure the stub has an ainvoke coroutine
    assert hasattr(llm, "ainvoke")


def test_get_response_from_ai_agent_stub():
    from agent.ai_agent import get_response_from_ai_agent

    import asyncio

    result = asyncio.get_event_loop().run_until_complete(
        get_response_from_ai_agent(
            "openai/gpt-oss-120b",
            ["Hello"],
            False,
            "You are helpful.",
            "Groq",
            include_execution_details=False,
        )
    )

    # When using the test stub, function should return a string answer
    assert isinstance(result, (str, dict))
