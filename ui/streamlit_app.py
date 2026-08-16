import requests
import streamlit as st


st.set_page_config(page_title="Agent Hub", layout="centered")
st.title("Agent Hub")
st.write("FastAPI + LangGraph + MCP Streamable HTTP")

system_prompt = st.text_area(
    "System Prompt",
    height=80,
    placeholder="You are a helpful AI agent.",
)

provider = st.radio("Provider", ("Groq", "OpenAI"))

models = {
    "Groq": ["openai/gpt-oss-120b"],
    "OpenAI": ["gpt-4o-mini"],
}
selected_model = st.selectbox("Model", models[provider])

user_query = st.text_area(
    "Query",
    height=120,
    placeholder="Try: Calculate 25 * 4 or What is the price of a laptop?",
)

if st.button("Ask Agent"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": False,
        }

        try:
            response = requests.post(
                "http://127.0.0.1:9999/chat",
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            st.subheader("Agent Response")
            st.markdown(response.json() if isinstance(response.json(), str) else str(response.json()))
        except requests.exceptions.RequestException as exc:
            st.error(f"Unable to connect to backend: {exc}")
