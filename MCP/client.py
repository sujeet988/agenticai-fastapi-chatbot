from langchain_core.tools import StructuredTool
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from common.config import MCP_SERVER_URL


async def _call_mcp_tool(name: str, arguments: dict) -> str:
    """Call one MCP tool through Streamable HTTP."""
    async with streamable_http_client(MCP_SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments)
            return "\n".join(
                getattr(content, "text", str(content))
                for content in result.content
            )


def get_mcp_tools():
    """Expose remote MCP tools as LangChain tools."""
    return [
        StructuredTool.from_function(
            coroutine=lambda expression: _call_mcp_tool(
                "calculator", {"expression": expression}
            ),
            name="calculator",
            description="Calculate a simple arithmetic expression.",
        ),
        StructuredTool.from_function(
            coroutine=lambda product: _call_mcp_tool(
                "get_product_info", {"product": product}
            ),
            name="get_product_info",
            description="Return demo product information.",
        ),
    ]
