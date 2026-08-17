# Agent Hub — System Design

## 1. Current Architecture

```text
                           ┌──────────────────────┐
                           │       User           │
                           └──────────┬───────────┘
                                      │
                                      ▼
                           ┌──────────────────────┐
                           │   Streamlit UI       │
                           │  Configuration + Chat│
                           └──────────┬───────────┘
                                      │ HTTP / JSON
                                      ▼
                    ┌──────────────────────────────────┐
                    │          FastAPI Backend          │
                    │                                  │
                    │  POST /chat ──► ReAct Agent      │
                    │                                  │
                    │  POST /multi-agent               │
                    │        │                         │
                    │        ▼                         │
                    │   LangGraph Graph                │
                    └─────────┬────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │    Agent 1      │       │    Agent 2      │
        │ ReAct + MCP     │       │    Reviewer     │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    ┌──────────────────────┐
                    │ Aggregator Agent     │
                    │ combines both results│
                    └──────────┬───────────┘
                               │
                               ▼
                         Final API response

Agent 1 tool path:
Agent 1 → MCP Client Adapter → Streamable HTTP → MCP Server → Tools
```

## 2. Component Responsibilities

### Streamlit UI

- Collects system prompt, provider, and model.
- Provides the chat interface.
- Keeps chat history in `st.session_state` for the current UI session.
- Sends the current user question to FastAPI.
- Does not own persistent backend memory yet.

### FastAPI

Entry point: `api/main.py`

Responsibilities:

- Exposes `/chat` for the original single-agent flow.
- Exposes `/multi-agent` for the two-agent graph.
- Validates the incoming request using Pydantic.
- Returns the final response to the UI/client.

### Agent 1 — ReAct + MCP

Entry point: `agent/ai_agent.py`

Responsibilities:

- Creates the LangGraph ReAct agent.
- Selects the configured LLM provider/model.
- Gives the agent access to MCP tools.
- Lets the LLM decide when a tool should be called.
- Returns the first specialist result to the multi-agent graph.

### Agent 2 — Reviewer

Entry point: `agent/reviewer_agent.py`

Responsibilities:

- Uses the same configured LLM provider/model.
- Independently reviews the same user question.
- Produces a second specialist result.
- Does not call MCP tools in this simple example.

### Multi-Agent Graph

Entry point: `agent/multi_agent_graph.py`

Responsibilities:

- Starts Agent 1 and Agent 2 from the same user query.
- Runs the two specialist nodes independently.
- Waits for both results.
- Sends both results to the aggregator node.
- Returns one final answer.

### Aggregator Agent

Implemented in `agent/multi_agent_graph.py`.

Responsibilities:

- Receives both specialist outputs.
- Resolves differences.
- Produces one concise final answer for the API.

### MCP Client Adapter

Location: `common/mcp_client_adapter.py`

Responsibilities:

- Encapsulates MCP client details.
- Connects to the MCP server using Streamable HTTP.
- Initializes an MCP session.
- Calls remote tools.
- Exposes MCP tools to Agent 1.

### MCP Server

Location: `MCP/servers/server.py`

Responsibilities:

- Exposes tools through the MCP protocol.
- Runs using Streamable HTTP.
- Currently exposes two demo tools:
  - `calculator`
  - `get_product_info`

## 3. Single-Agent Request Flow

Example:

```text
User: What is 10 + 20?
```

```text
Streamlit
   ↓
FastAPI /chat
   ↓
Agent 1 (ReAct)
   ↓
MCP Client Adapter
   ↓
MCP Server
   ↓
calculator("10 + 20")
   ↓
30
   ↓
Final response
```

## 4. Multi-Agent Request Flow

Endpoint:

```text
POST /multi-agent
```

The important part is the graph fan-out:

```text
                    User Query
                        │
                        ▼
                 ┌─────────────┐
                 │  LangGraph  │
                 │ Orchestrator│
                 └──────┬──────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌─────────────┐     ┌─────────────┐
       │   Agent 1   │     │   Agent 2   │
       │ ReAct + MCP │     │   Reviewer  │
       └──────┬──────┘     └──────┬──────┘
              │                   │
              └─────────┬─────────┘
                        ▼
                ┌──────────────┐
                │   Aggregate  │
                │   Agent      │
                └──────┬───────┘
                       ▼
                 Final Answer
```

For example:

```text
Question
  ↓
Agent 1 → uses calculator/product tool when needed
  ↓
Agent 2 → independently reviews the question
  ↓
Aggregator → compares both results
  ↓
API → returns one answer
```

## 5. Why This Demonstrates Multi-Agent / A2A-Like Behavior

The graph demonstrates **multi-agent collaboration** because two independent agents receive the same task and a third agent aggregates their outputs.

```text
Agent 1 ─────┐
             ├──► Aggregator ───► Final response
Agent 2 ─────┘
```

This is an **A2A-style learning example**, not a full A2A protocol implementation. There is no separate network protocol between the agents yet; communication happens through shared LangGraph state.

## 6. Configuration

Configuration is loaded from `.env` through `common/config.py`.

Example:

```env
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key

MCP_HOST=127.0.0.1
MCP_PORT=8000

API_HOST=127.0.0.1
API_PORT=9999

UI_API_URL=http://127.0.0.1:9999
```

The `.env` file should not be committed to source control.

## 7. Local Services

Run from the project root.

### Terminal 1 — MCP Server

```powershell
python -m MCP.servers.server
```

### Terminal 2 — FastAPI

```powershell
python -m api.main
```

### Terminal 3 — Streamlit

```powershell
streamlit run ui/streamlit_app.py
```

## 8. Testing the Multi-Agent Graph

Open Swagger:

```text
http://127.0.0.1:9999/docs
```

Call:

```text
POST /multi-agent
```

Example request:

```json
{
  "model_name": "openai/gpt-oss-120b",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful AI agent.",
  "messages": [
    "What is 10 + 20?"
  ],
  "allow_search": false
}
```

Expected behavior:

```text
Agent 1 → calculator → 30
Agent 2 → independent answer
Aggregator → final combined answer
```

## 9. RAG Status

RAG remains separate from the current multi-agent graph.

Current direction:

```text
Document
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Store Interface
   ├── ChromaDB
   └── Azure AI Search
```

RAG can later become another specialized agent in the graph.

## 10. Current Project Structure

```text
agenticai-fastapi-chatbot/
│
├── agent/
│   ├── __init__.py
│   ├── ai_agent.py
│   ├── reviewer_agent.py
│   └── multi_agent_graph.py
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── common/
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── models.py
│   ├── utils.py
│   └── mcp_client_adapter.py
│
├── MCP/
│   ├── __init__.py
│   └── servers/
│       ├── __init__.py
│       └── server.py
│
├── RAG/
│   ├── __init__.py
│   ├── chunking.py
│   ├── ingestion.py
│   ├── retriever.py
│   └── vector_store.py
│
├── ui/
│   └── streamlit_app.py
│
├── .env
├── .gitignore
├── requirements.txt
├── LOCAL_SETUP.md
└── SYSTEM_DESIGN.md
```

## 11. Future Extension

The current graph can grow naturally:

```text
Agent 1 ─────┐
Agent 2 ─────┼──► Aggregator
RAG Agent ───┤
SQL Agent ───┤
DevOps Agent ┘
```

Later, the graph can add:

- Persistent state / memory.
- Human approval nodes.
- Guardrails.
- Planning nodes.
- Multiple MCP servers.
- True networked A2A communication.
