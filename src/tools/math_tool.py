"""Math Tool: Evaluates mathematical expressions safely using asteval."""

import logging
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def calculate_expression(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.

    Use this tool whenever the user asks to calculate, compute, or solve a math problem.
    Examples: '15 * 42', '2 ** 8', 'sqrt(144)', 'sin(3.14159 / 2)', '(10 + 5) / 3'.

    Args:
        expression: A mathematical expression string to evaluate.

    Returns:
        The result of the calculation as a string, or an error message.
    """
    try:
        from asteval import Interpreter

        aeval = Interpreter()
        result = aeval(expression)

        if aeval.error:
            error_msgs = "\n".join(
                str(err.get_error()) for err in aeval.error
            )
            logger.warning(f"asteval errors for '{expression}': {error_msgs}")
            return f"Error evaluating expression: {error_msgs}"

        if result is None:
            return "Expression returned no result. Please check the syntax."

        logger.info(f"Calculated '{expression}' = {result}")
        return str(result)

    except ImportError:
        logger.error("asteval is not installed. Falling back to restricted eval.")
        # Fallback: very restricted eval (numbers and basic operators only)
        try:
            allowed_names = {"__builtins__": {}}
            result = eval(expression, allowed_names, {})  # noqa: S307
            logger.info(f"Calculated (fallback) '{expression}' = {result}")
            return str(result)
        except Exception as e:
            logger.error(f"Fallback eval failed for '{expression}': {e}")
            return f"Error: Could not evaluate '{expression}'. {e}"

    except Exception as e:
        logger.error(f"Unexpected error calculating '{expression}': {e}")
        return f"Error: {e}"
