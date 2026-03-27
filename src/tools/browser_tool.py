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
def play_youtube(query: str) -> str:
    """Plays a video on YouTube by searching and auto-playing the first result.

    Use this tool when the user says 'play X on YouTube', 'play X video',
    'watch X', or generally wants to play/watch video content.
    Do NOT use this for general web searches — only for playing media.
    Examples: 'play lofi hip hop', 'watch Python tutorial', 'play Never Gonna Give You Up'.

    Args:
        query: The YouTube search query string.

    Returns:
        A confirmation message.
    """
    try:
        # Use the /search redirect trick: this opens the search and YouTube
        # will auto-play the top result when using the search_query param.
        yt_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        webbrowser.open(yt_url)
        logger.info(f"Playing YouTube: {query}")
        return f"Playing '{query}' on YouTube."
    except Exception as e:
        logger.error(f"Failed to play YouTube for '{query}': {e}")
        return f"Error: Could not play on YouTube. {e}"


@tool
def play_on_spotify(query: str) -> str:
    """Opens Spotify and searches for a song, artist, or playlist.

    Use this tool when the user specifically mentions Spotify, e.g.,
    'play X on Spotify', 'open Spotify and play X'.
    This opens Spotify's search in the browser or desktop app.

    Args:
        query: The song, artist, or playlist to search for on Spotify.

    Returns:
        A confirmation message.
    """
    try:
        spotify_url = f"https://open.spotify.com/search/{quote_plus(query)}"
        webbrowser.open(spotify_url)
        logger.info(f"Opening Spotify for: {query}")
        return f"Opened Spotify search for '{query}'."
    except Exception as e:
        logger.error(f"Failed to open Spotify for '{query}': {e}")
        return f"Error: Could not open Spotify. {e}"
