#Step1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name:str
    model_provider:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

#Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

Allowed_model = ["openai/gpt-oss-120b", "gpt-4o-mini"]

app = FastAPI(title="Langraph Ai  Agent")
@app.post("/chat")
def chat_endpoint(request: RequestState):
    """API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request"""
    if request.model_name not in Allowed_model:
        return {"error":"Invalid model name. Kindly select a valid AI model"}

    llmid = request.model_name
    query = request.messages
    allowsearch = request.allow_search
    systemprompt = request.system_prompt
    provider = request.model_provider
     # Create AI Agent and get response from it! 
    response = get_response_from_ai_agent(llmid,query,allowsearch, systemprompt, provider)
    return response

#Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host = "127.0.0.1",port=9999)