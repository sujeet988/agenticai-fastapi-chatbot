from langchain_core.tools import StructuredTool
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"


async def get_mcp_tools():
    """Discover tools from the remote MCP server and adapt them to LangChain."""
    async with streamable_http_client(MCP_SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()

            tools = []
            for item in result.tools:
                async def call_tool(args, name=item.name):
                    response = await session.call_tool(name, args)
                    return "\n".join(
                        getattr(content, "text", str(content))
                        for content in response.content
                    )

                tools.append(
                    StructuredTool.from_function(
                        coroutine=call_tool,
                        name=item.name,
                        description=item.description or item.name,
                    )
                )

            return tools
