# Agent Hub — Local Setup

## 1. Clone the repository

```powershell
git clone --branch agent-hub --single-branch https://github.com/sujeet988/agenticai-fastapi-chatbot.git
cd agenticai-fastapi-chatbot
```

## 2. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Create `.env`

Create `.env` in the project root and replace the placeholder values with your own keys:

```env
# -----------------------------
# LLM / AI provider keys
# -----------------------------
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

# -----------------------------
# MCP Server
# -----------------------------
MCP_HOST=127.0.0.1
MCP_PORT=8000

# -----------------------------
# FastAPI
# -----------------------------
API_HOST=127.0.0.1
API_PORT=9999

# -----------------------------
# Streamlit -> FastAPI
# -----------------------------
UI_API_URL=http://127.0.0.1:9999
RAG_ENABLED=false

# -----------------------------
# RAG / Azure AI Search
# -----------------------------
AZURE_SEARCH_ENDPOINT=https://<search-service>.search.windows.net
AZURE_SEARCH_INDEX=<index-name>
AZURE_SEARCH_API_KEY=<search-api-key>
AZURE_SEARCH_VECTOR_FIELD=contentVector
AZURE_SEARCH_CONTENT_FIELD=content
RAG_TOP_K=5
AZURE_FOUNDRY_ENDPOINT=https://<resource>.openai.azure.com/openai/v1/
AZURE_FOUNDRY_API_KEY=<foundry-api-key>
AZURE_FOUNDRY_EMBEDDING_MODEL=<embedding-deployment-name>
```

> Do not commit `.env` to Git. Use real secret values only in your local environment.

## 5. Run the services

Open three terminals from the project root, activate the virtual environment in each, and run:

### Terminal 1 — MCP Server

```powershell
python -m MCP.servers.server
```

MCP endpoint:

```text
http://127.0.0.1:8000/mcp
```

### Terminal 2 — FastAPI

```powershell
python -m api.main
```

API:

```text
http://127.0.0.1:9999
```

Swagger:

```text
http://127.0.0.1:9999/docs
```

### Terminal 3 — Streamlit

```powershell
streamlit run ui/streamlit_app.py
```

UI:

```text
http://localhost:8501
```

## 6. Quick test

In the UI, try:

```text
What is 10 + 20?
```

Expected flow:

```text
Streamlit
  ↓
FastAPI
  ↓
LangGraph Agent
  ↓
MCP Client Adapter
  ↓
MCP Server
  ↓
calculator
  ↓
30
## 7. Deactivate the virtual environment

When you're finished working, deactivate the virtual environment to return to your system Python:

```powershell
deactivate
```

Thesame command works on macOS / Linux when you used `python -m venv`:

```bash
deactivate
```

```
