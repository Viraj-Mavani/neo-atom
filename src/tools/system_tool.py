"""System Tool: Executes whitelisted Windows OS actions safely."""

import logging
import os
import subprocess
from datetime import datetime

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Whitelist of safe applications that can be launched by name
_SAFE_APPS: dict[str, str] = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "settings": "ms-settings:",
    "snipping tool": "snippingtool.exe",
    "control panel": "control.exe",
}


@tool
def open_application(app_name: str) -> str:
    """Opens a Windows application by name.

    Use this tool when the user asks to open, launch, or start a Windows application.
    Supported apps include: notepad, calculator, paint, file explorer, task manager,
    command prompt, terminal, settings, snipping tool, control panel.

    Args:
        app_name: The name of the application to open (e.g., 'calculator', 'notepad').

    Returns:
        A confirmation message or an error if the app is not whitelisted.
    """
    normalized = app_name.strip().lower()
    executable = _SAFE_APPS.get(normalized)

    if executable is None:
        logger.warning(f"Blocked non-whitelisted app request: '{app_name}'")
        available = ", ".join(sorted(_SAFE_APPS.keys()))
        return (
            f"Sorry, '{app_name}' is not in my approved list of applications. "
            f"I can open: {available}."
        )

    try:
        os.startfile(executable)
        logger.info(f"Opened application: {executable}")
        return f"Successfully opened {app_name}."
    except Exception as e:
        logger.error(f"Failed to open '{executable}': {e}")
        return f"Error: Could not open {app_name}. {e}"


@tool
def get_system_time() -> str:
    """Returns the current system date and time.

    Use this tool when the user asks for the current time, date, or day of the week.

    Returns:
        The current date and time as a formatted string.
    """
    now = datetime.now()
    formatted = now.strftime("%A, %B %d, %Y at %I:%M %p")
    logger.info(f"System time requested: {formatted}")
    return f"The current date and time is: {formatted}"


@tool
def get_system_info() -> str:
    """Returns basic system information like OS name, version, and username.

    Use this tool when the user asks about their computer, system info, or machine specs.

    Returns:
        A summary string of key system details.
    """
    try:
        info_parts = [
            f"OS: {os.name}",
            f"Username: {os.getlogin()}",
            f"Computer Name: {os.environ.get('COMPUTERNAME', 'Unknown')}",
            f"Processor: {os.environ.get('PROCESSOR_IDENTIFIER', 'Unknown')}",
            f"Number of CPUs: {os.cpu_count()}",
        ]
        result = "\n".join(info_parts)
        logger.info("System info retrieved.")
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve system info: {e}")
        return f"Error retrieving system info: {e}"
