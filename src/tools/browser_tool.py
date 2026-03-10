"""Browser Tool: Opens URLs and searches the web via the default system browser."""

import logging
import webbrowser
from urllib.parse import quote_plus

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def open_website(url: str) -> str:
    """Opens a website URL in the user's default web browser.

    Use this tool when the user asks to open a specific website, URL, or webpage.
    The URL should include the protocol (https://).
    Examples: 'https://youtube.com', 'https://github.com', 'https://google.com'.

    Args:
        url: The full URL to open (e.g., 'https://youtube.com').

    Returns:
        A confirmation message.
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        webbrowser.open(url)
        logger.info(f"Opened browser: {url}")
        return f"Successfully opened {url} in the browser."
    except Exception as e:
        logger.error(f"Failed to open URL '{url}': {e}")
        return f"Error: Could not open the browser. {e}"


@tool
def search_web(query: str) -> str:
    """Searches the web using Google in the default browser.

    Use this tool when the user asks to search for something, look something up,
    or find information online.
    Examples: 'Python asyncio tutorial', 'weather in New York', 'latest tech news'.

    Args:
        query: The search query string.

    Returns:
        A confirmation message.
    """
    try:
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
        webbrowser.open(search_url)
        logger.info(f"Searched web for: {query}")
        return f"Successfully opened a Google search for '{query}'."
    except Exception as e:
        logger.error(f"Failed to search for '{query}': {e}")
        return f"Error: Could not perform web search. {e}"


@tool
def search_youtube(query: str) -> str:
    """Searches YouTube for a video in the default browser.

    Use this tool when the user asks to find a video, play something on YouTube,
    or search YouTube for content.
    Examples: 'Python tutorial for beginners', 'lofi hip hop beats', 'how to cook pasta'.

    Args:
        query: The YouTube search query string.

    Returns:
        A confirmation message.
    """
    try:
        yt_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        webbrowser.open(yt_url)
        logger.info(f"Searched YouTube for: {query}")
        return f"Successfully opened a YouTube search for '{query}'."
    except Exception as e:
        logger.error(f"Failed to search YouTube for '{query}': {e}")
        return f"Error: Could not search YouTube. {e}"
