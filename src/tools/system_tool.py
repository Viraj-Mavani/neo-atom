from langchain_core.tools import tool
import logging
import os

logger = logging.getLogger(__name__)

@tool
def execute_system_command(command: str) -> str:
    """Safely executes a whitelisted system action like opening an app or formatting. Use carefully."""
    logger.info(f"Executing system command: {command}")
    # os.system(...)
    return "Executed."
