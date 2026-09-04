"""Simple MCP server exposing tools used by the Agent."""

from common.config import MCP_HOST, MCP_PORT
from mcp.server.mcpserver import MCPServer


# Create the MCP server. Agents connect here to discover and call tools.
mcp = MCPServer("agent-hub-tools")


@mcp.tool()
def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression."""
    # Restrict the demo calculator to basic arithmetic characters.
    allowed = set("0123456789+-*/(). %")
    if any(char not in allowed for char in expression):
        return "Invalid expression"

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Could not calculate expression"


@mcp.tool()
def get_product_info(product: str) -> str:
    """Return demo product information."""
    products = {
        "laptop": "Laptop: 16GB RAM, 512GB SSD, price $1200",
        "phone": "Phone: 8GB RAM, 256GB storage, price $700",
        "tablet": "Tablet: 8GB RAM, 128GB storage, price $400",
    }
    return products.get(product.lower(), "Product not found")


if __name__ == "__main__":
    # Streamable HTTP allows the Agent/MCP client to call these tools remotely.
    mcp.run(
        transport="streamable-http",
        host=MCP_HOST,
        port=MCP_PORT,
    )
