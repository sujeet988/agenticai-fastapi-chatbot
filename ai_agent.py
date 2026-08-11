from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

#Step1: Setup API Keys for Groq, OpenAI and Tavily
GROQ_API_KEY= os.getenv("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
