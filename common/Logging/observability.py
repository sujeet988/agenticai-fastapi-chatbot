import os

from common.config import (
    LANGFUSE_BASE_URL,
    LANGFUSE_ENABLED,
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

    os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
    os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_BASE_URL"] = LANGFUSE_BASE_URL

    handler = CallbackHandler(public_key=LANGFUSE_PUBLIC_KEY)

    return {
        "callbacks": [handler],
        "run_name": run_name,
        "metadata": metadata or {},
    }


def flush_traces() -> None:
    """Send pending Langfuse traces to the cloud."""
    if not LANGFUSE_ENABLED:
        return

    try:
        from langfuse import get_client

        get_client().flush()
    except Exception:
        pass