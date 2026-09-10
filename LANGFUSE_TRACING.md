# Langfuse Cloud Tracing

Simple plan to add Langfuse tracing at the common layer and use it inside the agent.

## Goal

- Keep tracing code outside `agent/ai_agent.py`.
- Add one reusable helper in `common/Logging/observability.py`.
- Use Langfuse Cloud through LangChain/LangGraph callbacks.
- Keep the implementation simple and optional.

## Files to change

```text
common/config.py
common/Logging/observability.py
agent/ai_agent.py
requirements.txt
```

## 1. Add dependency

Add to `requirements.txt`:

```text
langfuse>=3.0.0
```

Install it:

```powershell
pip install langfuse
```

## 2. Add environment variables

Add these values to `.env`:

```env
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

For Langfuse US cloud, use:

```env
LANGFUSE_HOST=https://us.cloud.langfuse.com
```

## 3. Add config values

Add this to `common/config.py`:

```python
LANGFUSE_ENABLED = os.getenv("LANGFUSE_ENABLED", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
```

## 4. Add common tracing helper

Add this to `common/Logging/observability.py`:

```python
from common.config import (
    LANGFUSE_ENABLED,
    LANGFUSE_HOST,
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
)

try:
    from langfuse.langchain import CallbackHandler
except ImportError:
    CallbackHandler = None


def get_trace_config(run_name: str, metadata: dict | None = None):
    """Return Langfuse tracing config for LangChain/LangGraph calls."""
    if not LANGFUSE_ENABLED or CallbackHandler is None:
        return None

    if not LANGFUSE_PUBLIC_KEY or not LANGFUSE_SECRET_KEY:
        return None

    handler = CallbackHandler(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST,
    )

    return {
        "callbacks": [handler],
        "run_name": run_name,
        "metadata": metadata or {},
    }
```

## 5. Use tracing in agent

In `agent/ai_agent.py`, add:

```python
from common.Logging.observability import get_trace_config
```

Then replace:

```python
result = await agent.ainvoke({"messages": conversation})
```

With:

```python
trace_config = get_trace_config(
    run_name="agent_hub_chat",
    metadata={
        "model_name": model_name,
        "model_provider": model_provider,
        "rag_enabled": bool(context),
        "allow_search": allow_search,
    },
)

result = await agent.ainvoke(
    {"messages": conversation},
    config=trace_config,
)
```

## Expected result

When `LANGFUSE_ENABLED=true`, agent runs should appear in Langfuse Cloud with:

- model calls
- tool calls
- latency
- metadata
- execution trace

When Langfuse is disabled or keys are missing, the app continues to run normally without tracing.
