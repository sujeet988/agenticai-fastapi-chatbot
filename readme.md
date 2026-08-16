# Agentic AI FastAPI Chatbot

Simple Agentic AI example using FastAPI + LangGraph + RAG + MCP Streamable HTTP.

## Architecture

`Streamlit -> FastAPI -> ReAct Agent -> MCP Client -> MCP Server -> Tools`

`ReAct Agent -> RAG Retriever -> Local Knowledge Base`

- **Agent:** LangGraph ReAct agent
- **MCP Tool 1:** calculator
- **MCP Tool 2:** product information
- **MCP Transport:** Streamable HTTP (`/mcp`)
- **RAG:** small local lexical knowledge base; no vector DB required

## Run

Terminal 1 - MCP server:

```bash
python MCP/servers/devops_server.py
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

## Example questions

```text
Calculate 25 * 4
What is the price of a laptop?
What is RAG?
What is MCP?
```

Enable **Allow RAG** in the UI for knowledge-base retrieval.
