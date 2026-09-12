import logging
import os

from common.config import (
    LANGFUSE_BASE_URL,
    LANGFUSE_ENABLED,
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
)

logger = logging.getLogger(__name__)

try:
    from langfuse import get_client
    from langfuse.langchain import CallbackHandler

    LANGFUSE_AVAILABLE = True
except ImportError:
    get_client = None
    CallbackHandler = None
    LANGFUSE_AVAILABLE = False


def configure_langfuse() -> bool:
    if not LANGFUSE_ENABLED:
        logger.warning("Langfuse is disabled.")
        return False

    if not LANGFUSE_AVAILABLE:
        logger.error("Langfuse package is not available.")
        return False

    if not LANGFUSE_PUBLIC_KEY:
        logger.error("LANGFUSE_PUBLIC_KEY is missing.")
        return False

    if not LANGFUSE_SECRET_KEY:
        logger.error("LANGFUSE_SECRET_KEY is missing.")
        return False

    if not LANGFUSE_BASE_URL:
        logger.error("LANGFUSE_BASE_URL is missing.")
        return False

    os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
    os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_BASE_URL"] = LANGFUSE_BASE_URL

    return True


def get_trace_config(run_name: str, metadata: dict | None = None):
    if not configure_langfuse():
        return None

    try:
        # Initialize Langfuse client
        get_client()

        handler = CallbackHandler()

        return {
            "callbacks": [handler],
            "run_name": run_name,
            "metadata": metadata or {},
        }

    except Exception:
        logger.exception("Failed to initialize Langfuse")
        return None


def flush_traces():
    if not LANGFUSE_ENABLED or not LANGFUSE_AVAILABLE:
        return

    try:
        get_client().flush()
    except Exception:
        logger.exception("Langfuse flush failed")