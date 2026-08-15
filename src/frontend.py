## Phase3–Setup Frontend
##1. Setup UI with streamlit (model provider, model, system prompt, query)
import streamlit as st

st.set_page_config(page_title="Chat with LLM", layout="centered")
st.title("Ai Chat bot agent")
st.write("create and interact with your own AI chat bot agent")
system_prompt=st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

Model_Name_Groq = ["openai/gpt-oss-120b","test model"]
Model_Name_OpenAI = ["gpt-4"]

provider=st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider =="Groq":
    selected_model = st.selectbox("Select Groq Model:", Model_Name_Groq)
elif provider =="OpenAI":
    selected_model = st.selectbox("Select Groq Model:", Model_Name_OpenAI)


allow_web_search=st.checkbox("Allow Web Search")

user_query=st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

API_URL="http://127.0.0.1:9999/chat"

if st.button("Ask agent"):
    if user_query.strip():
         #Step2: Connect with backend via URL
        import requests
        payload={
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response=requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data}")
        else:
            st.error(f"API Error: {response.status_code}")
            st.json(response.json())

##2. Connect with backend via URL
