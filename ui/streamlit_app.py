import requests
import streamlit as st


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Agent Hub",
    layout="centered"
)


# --------------------------------
# Header
# --------------------------------

st.title("🤖 Agent Hub")

st.write(
    "Create and interact with your own AI agent."
)


# --------------------------------
# System Prompt
# --------------------------------

system_prompt = st.text_area(
    "Define your AI Agent",
    height=100,
    placeholder=(
        "Example: You are a helpful AI assistant "
        "specialized in software engineering."
    )
)


# --------------------------------
# Provider
# --------------------------------

provider = st.radio(
    "Select Provider",
    (
        "Groq",
        "OpenAI"
    ),
    horizontal=True
)


# --------------------------------
# Model
# --------------------------------

if provider == "Groq":

    models = [
        "openai/gpt-oss-120b"
    ]

else:

    models = [
        "gpt-4o-mini"
    ]


selected_model = st.selectbox(
    "Select Model",
    models
)


# --------------------------------
# Web Search
# --------------------------------

allow_web_search = st.checkbox(
    "Allow Web Search"
)


# --------------------------------
# User Query
# --------------------------------

user_query = st.text_area(
    "Enter your query",
    height=150,
    placeholder="Ask anything..."
)


# --------------------------------
# API
# --------------------------------

API_URL = (
    "http://127.0.0.1:9999/chat"
)


# --------------------------------
# Ask Agent
# --------------------------------

if st.button(
    "Ask Agent",
    type="primary"
):

    if not user_query.strip():

        st.warning(
            "Please enter a query."
        )

    else:

        payload = {

            "model_name": selected_model,

            "model_provider": provider,

            "system_prompt": (
                system_prompt.strip()
                if system_prompt.strip()
                else
                "You are a helpful AI assistant."
            ),

            "messages": [
                user_query
            ],

            "allow_search": allow_web_search
        }

        try:

            with st.spinner(
                "Agent is thinking..."
            ):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

            # -------------------------
            # Success
            # -------------------------

            if response.status_code == 200:

                response_data = response.json()

                st.subheader(
                    "Agent Response"
                )

                # API returns:
                # {
                #   "content": "..."
                # }

                st.markdown(
                    response_data.get(
                        "content",
                        "No response received."
                    )
                )

            # -------------------------
            # Validation Error
            # -------------------------

            elif response.status_code == 422:

                st.error(
                    "Invalid request sent to API."
                )

                st.json(
                    response.json()
                )

            # -------------------------
            # Other API Error
            # -------------------------

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.json(
                    response.json()
                )

        except requests.exceptions.RequestException as ex:

            st.error(
                f"Unable to connect to API: {ex}"
            )