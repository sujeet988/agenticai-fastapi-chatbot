ALLOWED_MODELS = {
    "Groq": [
        "openai/gpt-oss-120b"
    ],
    "OpenAI": [
        "gpt-4o-mini"
    ]
}

DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer the user's question clearly and accurately.
"""

DEFAULT_TEMPERATURE = 0