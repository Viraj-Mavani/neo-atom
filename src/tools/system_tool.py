"""System Tool: Executes whitelisted Windows OS actions safely."""

import logging
import os
import subprocess
import ctypes
from datetime import datetime

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Whitelist of safe applications that can be launched by name
_SAFE_APPS: dict[str, str] = {
    # Built-in Windows
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "powershell": "powershell.exe",
    "settings": "ms-settings:",
    "snipping tool": "snippingtool.exe",
    "snip and sketch": "ms-screenclip:",
    "control panel": "control.exe",
    "device manager": "devmgmt.msc",
    "disk management": "diskmgmt.msc",
    "event viewer": "eventvwr.msc",
    "resource monitor": "resmon.exe",
    "system information": "msinfo32.exe",
    "registry editor": "regedit.exe",
    "character map": "charmap.exe",
    "magnifier": "magnify.exe",
    "on-screen keyboard": "osk.exe",
    "wordpad": "wordpad.exe",
    "remote desktop": "mstsc.exe",
    # Common third-party (will fail gracefully if not installed)
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "vs code": "code",
    "visual studio code": "code",
    "spotify": "spotify.exe",
    "discord": "discord.exe",
    "slack": "slack.exe",
    "teams": "ms-teams:",
    "microsoft teams": "ms-teams:",
    "word": "winword.exe",
    "microsoft word": "winword.exe",
    "excel": "excel.exe",
    "microsoft excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "outlook": "outlook.exe",
    "obs": "obs64.exe",
    "obs studio": "obs64.exe",
    "steam": "steam.exe",
    "vlc": "vlc.exe",
}


@tool
def open_application(app_name: str) -> str:
    """Opens a Windows application by name.

    Use this tool when the user asks to open, launch, or start a Windows application.
    Supports many built-in and common third-party apps.

    Args:
        app_name: The name of the application to open (e.g., 'calculator', 'chrome', 'spotify').

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


# ── Power Management Tools ─────────────────────────────────────────────────────

@tool
def lock_pc() -> str:
    """Locks the Windows workstation immediately.

    Use this tool when the user says 'lock my PC', 'lock the computer',
    or 'lock screen'.

    Returns:
        A confirmation message.
    """
    try:
        ctypes.windll.user32.LockWorkStation()
        logger.info("Workstation locked.")
        return "The PC has been locked."
    except Exception as e:
        logger.error(f"Failed to lock PC: {e}")
        return f"Error: Could not lock the PC. {e}"


@tool
def sleep_pc() -> str:
    """Puts the Windows PC into sleep mode.

    Use this tool when the user says 'put the PC to sleep', 'sleep mode',
    or 'go to sleep'.

    Returns:
        A confirmation message.
    """
    try:
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"],
            check=True,
        )
        logger.info("PC entering sleep mode.")
        return "The PC is going to sleep."
    except Exception as e:
        logger.error(f"Failed to sleep PC: {e}")
        return f"Error: Could not put the PC to sleep. {e}"


@tool
def shutdown_pc() -> str:
    """Shuts down the Windows PC after a 30-second delay (can be cancelled).

    Use this tool when the user says 'shut down', 'turn off the computer',
    or 'power off'.

    Returns:
        A confirmation message.
    """
    try:
        subprocess.run(["shutdown", "/s", "/t", "30"], check=True)
        logger.info("Shutdown initiated (30s delay).")
        return "Shutdown initiated. The PC will turn off in 30 seconds. Say 'cancel shutdown' to abort."
    except Exception as e:
        logger.error(f"Failed to initiate shutdown: {e}")
        return f"Error: Could not shut down. {e}"


@tool
def cancel_shutdown() -> str:
    """Cancels a pending Windows shutdown.

    Use this tool when the user says 'cancel shutdown', 'abort shutdown',
    or 'don't shut down'.

    Returns:
        A confirmation message.
    """
    try:
        subprocess.run(["shutdown", "/a"], check=True)
        logger.info("Shutdown cancelled.")
        return "Shutdown has been cancelled."
    except Exception as e:
        logger.error(f"Failed to cancel shutdown: {e}")
        return f"Error: Could not cancel shutdown. {e}"


@tool
def restart_pc() -> str:
    """Restarts the Windows PC after a 30-second delay (can be cancelled).

    Use this tool when the user says 'restart', 'reboot', or 'restart the computer'.

    Returns:
        A confirmation message.
    """
    try:
        subprocess.run(["shutdown", "/r", "/t", "30"], check=True)
        logger.info("Restart initiated (30s delay).")
        return "Restart initiated. The PC will reboot in 30 seconds. Say 'cancel shutdown' to abort."
    except Exception as e:
        logger.error(f"Failed to initiate restart: {e}")
        return f"Error: Could not restart. {e}"


@tool
def hibernate_pc() -> str:
    """Puts the Windows PC into hibernation mode.

    Use this tool when the user says 'hibernate', 'hibernation mode',
    or 'put the PC to hibernation'.

    Returns:
        A confirmation message.
    """
    try:
        subprocess.run(["shutdown", "/h"], check=True)
        logger.info("PC entering hibernation.")
        return "The PC is entering hibernation mode."
    except Exception as e:
        logger.error(f"Failed to hibernate PC: {e}")
        return f"Error: Could not hibernate. {e}"

