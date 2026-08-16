import streamlit as st
import requests


st.set_page_config(
    page_title="Chat with LLM",
    layout="centered"
)


st.title("AI Chat Bot Agent")

st.write(
    "Create and interact with your own AI chat bot agent"
)


# --------------------------------
# System Prompt
# --------------------------------

system_prompt = st.text_area(
    "Define your AI Agent:",
    height=70,
    placeholder="Type your system prompt here..."
)


# --------------------------------
# Models
# --------------------------------

MODEL_NAME_GROQ = [
    "openai/gpt-oss-120b"
]

MODEL_NAME_OPENAI = [
    "gpt-4o-mini"
]


provider = st.radio(
    "Select Provider:",
    ("Groq", "OpenAI")
)


if provider == "Groq":

    selected_model = st.selectbox(
        "Select Groq Model:",
        MODEL_NAME_GROQ
    )

else:

    selected_model = st.selectbox(
        "Select OpenAI Model:",
        MODEL_NAME_OPENAI
    )


# --------------------------------
# RAG
# --------------------------------

allow_rag = st.checkbox(
    "Allow RAG"
)


# --------------------------------
# User Query
# --------------------------------

user_query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask Anything!"
)


# --------------------------------
# Backend API
# --------------------------------

API_URL = "http://127.0.0.1:9999/chat"


# --------------------------------
# Ask Agent
# --------------------------------

if st.button("Ask Agent"):

    if not user_query.strip():

        st.warning(
            "Please enter a query."
        )

    else:

        payload = {

            "model_name": selected_model,

            "model_provider": provider,

            "system_prompt": system_prompt,

            "messages": [
                user_query
            ],

            "allow_search": allow_rag
        }


        try:

            response = requests.post(
                API_URL,
                json=payload
            )


            if response.status_code == 200:

                response_data = response.json()


                if "error" in response_data:

                    st.error(
                        response_data["error"]
                    )

                else:

                    st.subheader(
                        "Agent Response"
                    )

                    if isinstance(
                        response_data,
                        dict
                    ):

                        final_response = (
                            response_data
                            .get("response", "")
                        )

                        st.markdown(
                            final_response
                        )

                    else:

                        st.markdown(
                            str(response_data)
                        )


            else:

                st.error(
                    f"API Error: "
                    f"{response.status_code}"
                )

                st.json(
                    response.json()
                )


        except requests.exceptions.RequestException as e:

            st.error(
                f"Unable to connect to backend: {e}"
            )
