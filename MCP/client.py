"""Minimal MCP client entry point.

Run the MCP server directly for local development:
    python MCP/servers/devops_server.py

The agent currently uses the same two tools locally in agent/tools.py.
The MCP server exposes the identical contract so the tools can be moved
behind MCP without changing the agent's tool semantics.
"""
