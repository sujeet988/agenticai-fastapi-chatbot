from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression."""
    allowed = set("0123456789+-*/(). %")
    if any(ch not in allowed for ch in expression):
        return "Invalid expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Could not calculate expression"


@tool
def get_product_info(product: str) -> str:
    """Return demo product information."""
    products = {
        "laptop": "Laptop: 16GB RAM, 512GB SSD, price $1200",
        "phone": "Phone: 8GB RAM, 256GB storage, price $700",
    }
    return products.get(product.lower(), "Product not found")
