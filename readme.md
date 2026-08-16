# Agentic AI FastAPI Chatbot

Simple Agentic AI example using FastAPI + LangGraph + RAG + MCP.

## Flow

`FastAPI -> ReAct Agent -> Tools / RAG`

- **Tool 1:** calculator
- **Tool 2:** product information
- **RAG:** small local knowledge base
- **MCP:** same two tools exposed from `MCP/servers/devops_server.py`

## Run

```bash
pip install -r requirements.txt
python -m uvicorn api.main:app --reload --port 9999
```

MCP server:

```bash
python MCP/servers/devops_server.py
```

## Example requests

Ask:
- `Calculate 25 * 4`
- `What is the price of a laptop?`
- `What is RAG?`

For RAG questions set `allow_search: true`.
