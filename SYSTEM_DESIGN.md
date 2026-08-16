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
                    │  POST /chat                      │
                    │        │                         │
                    │        ▼                         │
                    │   LangGraph ReAct Agent          │
                    │        │                         │
                    │        ▼                         │
                    │   MCP Client Adapter             │
                    └─────────┬────────────────────────┘
                              │
                              │ Streamable HTTP
                              ▼
                    ┌──────────────────────────────┐
                    │        MCP Server             │
                    │                              │
                    │  calculator                  │
                    │  get_product_info            │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         External Tools / Systems
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

- Exposes the `/chat` API.
- Validates the incoming request using Pydantic.
- Calls the agent layer.
- Returns the final agent response to the UI.

### Agent Layer

Entry point: `agent/ai_agent.py`

Responsibilities:

- Creates the LangGraph ReAct agent.
- Selects the configured LLM provider/model.
- Gives the agent access to MCP tools.
- Lets the LLM decide when a tool should be called.
- Returns the final answer.

### MCP Client Adapter

Location: `common/mcp_client_adapter.py`

Responsibilities:

- Encapsulates MCP client details.
- Connects to the MCP server using Streamable HTTP.
- Initializes an MCP session.
- Calls remote tools.
- Exposes MCP tools to the LangGraph agent.

The agent does not need to know MCP protocol details.

### MCP Server

Location: `MCP/servers/server.py`

Responsibilities:

- Exposes tools through the MCP protocol.
- Runs using Streamable HTTP.
- Currently exposes two demo tools:
  - `calculator`
  - `get_product_info`

## 3. Agentic Request Flow

Example request:

```text
User: What is 10 + 20?
```

Flow:

```text
1. Streamlit sends the question to FastAPI.
2. FastAPI invokes the LangGraph ReAct agent.
3. The agent determines that a calculator tool is useful.
4. Agent calls the MCP client adapter.
5. MCP client connects to the MCP server over Streamable HTTP.
6. MCP server executes calculator("10 + 20").
7. Tool result = 30.
8. Agent produces the final response.
9. FastAPI returns the response to Streamlit.
```

## 4. Why This Is Agentic

The LLM is not limited to direct text generation. It can decide whether an external tool is required and invoke that tool through MCP before producing the final response.

```text
User Goal
   ↓
LLM / Agent
   ↓
Tool needed?
   ├── No ──► Final answer
   │
   └── Yes
        ↓
   MCP Client Adapter
        ↓
   MCP Server
        ↓
   Tool execution
        ↓
   Tool result
        ↓
   Agent
        ↓
   Final answer
```

## 5. Configuration

Configuration is loaded from `.env` through `common/config.py`.

Example:

```env
MCP_HOST=127.0.0.1
MCP_PORT=8000

API_HOST=127.0.0.1
API_PORT=9999

UI_API_URL=http://127.0.0.1:9999
```

The `.env` file should not be committed to source control.

## 6. Runtime Services

Run the services from the project root.

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

API endpoint:

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

## 7. Current Project Structure

```text
agenticai-fastapi-chatbot/
│
├── agent/
│   ├── __init__.py
│   └── ai_agent.py
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
└── SYSTEM_DESIGN.md
```

## 8. RAG Status

RAG is kept separate from the current agent flow while MCP is being verified.

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

The RAG layer can later be exposed as another agent tool without changing the MCP architecture.

## 9. Extensibility

The current boundaries are intended to support future capabilities without rewriting the core request flow.

```text
Current
  ↓
MCP tools
  ↓
RAG
  ↓
Persistent conversation state
  ↓
Long-term memory
  ↓
Multi-agent supervisor
  ↓
Planning
  ↓
Human approval
  ↓
Guardrails
  ↓
Multiple MCP servers
  ↓
A2A communication
```

## 10. Design Principles

- **Loose coupling:** Agent, MCP adapter, MCP server, and RAG are separate concerns.
- **Protocol isolation:** MCP-specific code is contained in the MCP server and client adapter.
- **Provider independence:** LLM selection is configured through the API/UI rather than hard-coded into the agent flow.
- **Pluggable RAG:** Vector storage can be switched behind an interface.
- **Incremental architecture:** Advanced capabilities can be added without changing the basic FastAPI → Agent → MCP flow.
