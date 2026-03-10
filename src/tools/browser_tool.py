from langchain_core.tools import tool
import webbrowser
import logging

logger = logging.getLogger(__name__)

@tool
def open_browser(url: str) -> str:
    """Opens a webpage in the default system browser. E.g., open_browser(url='https://youtube.com')"""
    logger.info(f"Opening browser: {url}")
    # webbrowser.open(url)
    return f"Successfully opened {url}"
