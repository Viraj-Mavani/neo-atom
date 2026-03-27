"""Media Tool: Simulates hardware media keys for playback and volume control."""

import logging

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

try:
    import pyautogui
    _HAS_PYAUTOGUI = True
except ImportError:
    _HAS_PYAUTOGUI = False
    logger.warning("pyautogui not installed — media key tools will be unavailable.")


def _press_key(key: str, description: str) -> str:
    """Internal helper to press a key and return a status message.

    Args:
        key: The pyautogui key name to press.
        description: Human-readable description of the action.

    Returns:
        Confirmation or error string.
    """
    if not _HAS_PYAUTOGUI:
        return "Error: pyautogui is not installed. Run: pip install pyautogui"
    try:
        pyautogui.press(key)
        logger.info(f"Media key pressed: {key} ({description})")
        return f"Done — {description}."
    except Exception as e:
        logger.error(f"Failed to press '{key}': {e}")
        return f"Error pressing media key: {e}"


@tool
def play_pause_media() -> str:
    """Toggles play/pause for the currently active media player.

    Use this tool when the user says 'play', 'pause', 'resume',
    'stop the music', or 'pause the video'.

    Returns:
        A confirmation message.
    """
    return _press_key("playpause", "Toggled play/pause")


@tool
def next_track() -> str:
    """Skips to the next track in the current media player.

    Use this tool when the user says 'next song', 'skip', or 'next track'.

    Returns:
        A confirmation message.
    """
    return _press_key("nexttrack", "Skipped to the next track")


@tool
def previous_track() -> str:
    """Goes back to the previous track in the current media player.

    Use this tool when the user says 'previous song', 'go back', or 'previous track'.

    Returns:
        A confirmation message.
    """
    return _press_key("prevtrack", "Went back to the previous track")


@tool
def volume_up() -> str:
    """Increases the system volume by one step.

    Use this tool when the user says 'volume up', 'louder', or 'increase volume'.
    Call this tool multiple times if the user asks for a big increase.

    Returns:
        A confirmation message.
    """
    return _press_key("volumeup", "Volume increased")


@tool
def volume_down() -> str:
    """Decreases the system volume by one step.

    Use this tool when the user says 'volume down', 'quieter', or 'decrease volume'.
    Call this tool multiple times if the user asks for a big decrease.

    Returns:
        A confirmation message.
    """
    return _press_key("volumedown", "Volume decreased")


@tool
def mute_unmute() -> str:
    """Toggles mute/unmute for the system audio.

    Use this tool when the user says 'mute', 'unmute', or 'toggle mute'.

    Returns:
        A confirmation message.
    """
    return _press_key("volumemute", "Toggled mute/unmute")
