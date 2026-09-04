import sys
import types
from fastapi.testclient import TestClient


# Insert lightweight stubs for heavy modules so tests can import api.main
# without installing all external dependencies.
ai_agent_stub = types.ModuleType("agent.ai_agent")
async def _stub_get_response_from_ai_agent(*args, **kwargs):
    return "stub-answer"
ai_agent_stub.get_response_from_ai_agent = _stub_get_response_from_ai_agent

multi_agent_stub = types.ModuleType("agent.multi_agent_graph")
async def _stub_run_multi_agent(*args, **kwargs):
    return "multi-stub"
multi_agent_stub.run_multi_agent = _stub_run_multi_agent

retriever_stub = types.ModuleType("RAG.retriever")
def _stub_retrieve_context(query: str, k: int = 2) -> str:
    return "stub-context"
retriever_stub.retrieve_context = _stub_retrieve_context

sys.modules["agent.ai_agent"] = ai_agent_stub
sys.modules["agent.multi_agent_graph"] = multi_agent_stub
sys.modules["RAG.retriever"] = retriever_stub


def test_root():
    from api.main import app

    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Agent Hub API is running"}


def test_chat_invalid_model():
    from api.main import app

    client = TestClient(app)

    payload = {
        "model_name": "invalid-model",
        "model_provider": "OpenAI",
        "system_prompt": "You are helpful.",
        "messages": ["hello"],
        "allow_search": False,
        "include_execution_details": False,
    }

    resp = client.post("/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("error") is not None


def test_multi_agent_missing_query():
    from api.main import app

    client = TestClient(app)

    payload = {
        "model_name": "openai/gpt-oss-120b",
        "model_provider": "Groq",
        "system_prompt": "You are helpful.",
        "query": "",
        "include_execution_details": False,
    }

    resp = client.post("/multi-agent", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("error") == "Please provide a question."
