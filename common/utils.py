def get_last_ai_message(messages):

    for message in reversed(messages):

        if isinstance(message, dict):
            if message.get("type") == "ai":
                return message.get("content", "")

        elif hasattr(message, "content"):
            return message.content

    return ""