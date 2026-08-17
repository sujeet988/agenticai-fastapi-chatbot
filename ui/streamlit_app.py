import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

UI_API_URL = os.getenv(
    "UI_API_URL",
    "http://127.0.0.1:9999",
)


st.set_page_config(
    page_title="Agent Hub",
    page_icon="🤖",
    layout="centered",
)


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.title("Agent Hub")
    st.caption("FastAPI + LangGraph + MCP Streamable HTTP")

    st.subheader("Agent Configuration")

    system_prompt = st.text_area(
        "System Prompt",
        height=120,
        placeholder="You are a helpful AI agent.",
    )

    provider = st.radio(
        "Provider",
        ("Groq", "OpenAI"),
    )

    models = {
        "Groq": ["openai/gpt-oss-120b"],
        "OpenAI": ["gpt-4o-mini"],
    }

    selected_model = st.selectbox(
        "Model",
        models[provider],
    )

    agent_mode = st.radio(
        "Agent Mode",
        ("Single Agent", "Multi Agent"),
        help="Multi Agent runs the MCP/tool agent and reviewer agent, then aggregates both results.",
    )

    show_execution_details = st.checkbox(
        "Show execution details",
        value=False,
        help="Show agent and tool execution metadata for learning/debugging.",
    )

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


st.title("Chat")
st.caption(f"Using {provider} · {selected_model} · {agent_mode}")

if not st.session_state.messages:
    st.info("Ask a question below to start the conversation.")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_query = st.chat_input("Ask your agent...")


if user_query:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    # Single-agent and multi-agent APIs use different request shapes.
    if agent_mode == "Multi Agent":
        endpoint = f"{UI_API_URL}/multi-agent"
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "query": user_query,
            "include_execution_details": show_execution_details,
        }
    else:
        endpoint = f"{UI_API_URL}/chat"
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": False,
            "include_execution_details": show_execution_details,
        }

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    endpoint,
                    json=payload,
                    timeout=120,
                )
                response.raise_for_status()
                result = response.json()

                # Backend returns either a plain answer or answer + execution metadata.
                if isinstance(result, str):
                    answer = result
                    execution = None
                else:
                    answer = result.get("answer")
                    if answer is None:
                        answer = result.get("error", str(result))
                    execution = result.get("execution")

                st.markdown(answer)

                if show_execution_details and execution:
                    with st.expander("Execution Details", expanded=True):
                        st.json(execution)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    except requests.exceptions.RequestException as exc:
        error_message = f"Unable to connect to backend: {exc}"

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )
