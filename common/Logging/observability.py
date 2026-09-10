from common.config import (LANGFUSE_ENABLED, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST)

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