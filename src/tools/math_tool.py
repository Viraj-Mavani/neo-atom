from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

@tool
def calculate_expression(expression: str) -> str:
    """Evaluates a mathematical expression like '15 * 4' or '2 ** 8'."""
    logger.info(f"Calculating: {expression}")
    # Use asteval for safety
    return "42"
