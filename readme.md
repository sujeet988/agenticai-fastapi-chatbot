# Agentic AI FastAPI Chatbot

Simple Agentic AI example using FastAPI + LangGraph + MCP Streamable HTTP + a small standalone RAG pipeline.

## Architecture

```text
Streamlit
   ↓
FastAPI /chat
   ↓
LangGraph ReAct Agent
   ↓
MCP Client
   ↓ Streamable HTTP
MCP Server
   ├── calculator
   └── get_product_info
```

RAG is currently kept separate so MCP can be verified independently:

```text
FastAPI /rag
   ↓
RAG Retriever
   ↓
Chunked Local Knowledge Base
```

## Project structure

```text
agent/
  ai_agent.py
api/
  main.py
MCP/
  client.py
  servers/server.py
RAG/
  chunking.py
  ingestion.py
  retriever.py
  vector_store.py
ui/
  streamlit_app.py
```

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Terminal 1 - MCP server:

```bash
python MCP/servers/server.py
```

MCP endpoint:

```text
http://127.0.0.1:8000/mcp
```

Terminal 2 - FastAPI:

```bash
python -m uvicorn api.main:app --reload --port 9999
```

Terminal 3 - Streamlit:

```bash
streamlit run ui/streamlit_app.py
```

## Test MCP through the agent

```text
Calculate 25 * 4
What is the price of a laptop?
```

## Test RAG directly

```http
POST /rag
```

Example body:

```json
{
  "query": "What is RAG?",
  "top_k": 2
}
```

RAG is intentionally simple for now. It does not use a vector database and is not yet connected to the agent. It can be added after the MCP flow is verified.
