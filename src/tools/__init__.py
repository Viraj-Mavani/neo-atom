"""Tool Registry: Exports all available tools for the LangChain agent."""

from src.tools.math_tool import calculate_expression
from src.tools.browser_tool import open_website, search_web, search_youtube
from src.tools.system_tool import open_application, get_system_time, get_system_info

# Master list of all tools the agent can use.
# Add new tools here as they are created.
ALL_TOOLS = [
    calculate_expression,
    open_website,
    search_web,
    search_youtube,
    open_application,
    get_system_time,
    get_system_info,
]

__all__ = [
    "ALL_TOOLS",
    "calculate_expression",
    "open_website",
    "search_web",
    "search_youtube",
    "open_application",
    "get_system_time",
    "get_system_info",
]
