import os

from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


API_HOST = os.getenv(
    "API_HOST",
    "127.0.0.1"
)

API_PORT = int(
    os.getenv(
        "API_PORT",
        "9999"
    )
)