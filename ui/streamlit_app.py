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
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root { --ink: #17202a; --muted: #66727d; --accent: #e05a3f; --line: #e5e8eb; }
    .stApp { background: #f7f8f6; color: var(--ink); }
    [data-testid="stSidebar"] { background: #17202a; }
    [data-testid="stSidebar"] * { color: #f7f8f6; }
    [data-testid="stSidebar"] [data-baseweb="select"] * { color: #17202a; }
    [data-testid="stSidebar"] textarea, [data-testid="stSidebar"] input { color: #17202a; }
    .hero { padding: 1.4rem 0 1rem; border-bottom: 1px solid var(--line); }
    .eyebrow { color: var(--accent); font-size: .72rem; font-weight: 700; letter-spacing: .12em; }
    .hero h1 { margin: .2rem 0; font-size: 2.4rem; letter-spacing: 0; }
    .hero p { color: var(--muted); margin: 0; }
    .section-label { color: var(--muted); font-size: .75rem; font-weight: 700; letter-spacing: .08em; }
    div[data-testid="stMetric"] { background: white; border: 1px solid var(--line); padding: .8rem 1rem; }
    div.stButton > button { border-radius: 5px; border: 1px solid var(--line); }
    div.stButton > button[kind="primary"] { background: var(--accent); border-color: var(--accent); color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.markdown("## AGENT HUB")
    st.caption("A focused workspace for agents and retrieval.")

    st.markdown("### 01 / Agent setup")

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

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### 02 / Knowledge base")
    st.caption("Upload a PDF to extract, chunk, embed, and index it in Azure AI Search.")
    uploaded_pdf = st.file_uploader("PDF document", type=["pdf"], label_visibility="collapsed")
    if uploaded_pdf and st.button("Index PDF", use_container_width=True):
        try:
            response = requests.post(
                f"{UI_API_URL}/rag/upload",
                files={
                    "file": (
                        uploaded_pdf.name,
                        uploaded_pdf.getvalue(),
                        "application/pdf",
                    )
                },
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            st.success(f"Indexed {result['indexed']} chunks from {result['filename']}.")
        except requests.exceptions.RequestException as exc:
            st.error(f"PDF indexing failed: {exc}")

    st.markdown("### 03 / Retrieval")
    rag_query = st.text_input("Search indexed documents", placeholder="Ask your knowledge base", label_visibility="collapsed")
    if st.button("Search knowledge base", use_container_width=True, disabled=not rag_query.strip()):
        try:
            response = requests.post(
                f"{UI_API_URL}/rag",
                json={"query": rag_query, "top_k": 5},
                timeout=120,
            )
            response.raise_for_status()
            st.write(response.json().get("context", "No matching context found."))
        except requests.exceptions.RequestException as exc:
            st.error(f"RAG search failed: {exc}")


st.markdown(
    f'<div class="hero"><div class="eyebrow">AGENT WORKSPACE</div>'
    f'<h1>Conversation</h1><p>{provider} / {selected_model} / {agent_mode}</p></div>',
    unsafe_allow_html=True,
)

metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("Messages", len(st.session_state.messages))
metric_two.metric("Mode", agent_mode)
metric_three.metric("Knowledge", "Azure AI Search")
st.markdown('<div class="section-label">LIVE THREAD</div>', unsafe_allow_html=True)

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
