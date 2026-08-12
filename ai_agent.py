from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

#Step1: Setup API Keys for Groq, OpenAI and Tavily
GROQ_API_KEY= os.getenv("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

print("GROQ_API_KEY:", GROQ_API_KEY)
print("TAVILY_API_KEY:", TAVILY_API_KEY)
print("OPENAI_API_KEY:", OPENAI_API_KEY)    

#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily  import TavilySearch
from langchain.agents import create_agent

openai_llm = ChatOpenAI(model_name="gpt-4o-mini")
groq_llm = ChatGroq(model_name="openai/gpt-oss-120b");

search_tool = TavilySearch(max_result=2)

#Step3: Setup AI Agent with Search tool functionality

from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
system_prompt ="Act as Ai ChatBot who is smart and firendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider =="Groq":
        llm = ChatGroq(model_name=llm_id)
    elif provider =="OpenAI":
        llm = ChatOpenAI(model_name=llm_id)

    tools = [TavilySearch(max_result=2)] if allow_search else []
    agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt = system_prompt
    )
    if isinstance(query, list):
     content = "\n".join(query)
    else:
     content = query

    response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": content
        }
    ]
    })
    messages = response.get("messages", [])
    #ai_message = response["messages"][-1]
    return messages

