"""Tool Registry: Exports all available tools for the LangChain agent."""

from src.tools.math_tool import calculate_expression
from src.tools.browser_tool import open_website, search_web, play_youtube, play_on_spotify
from src.tools.system_tool import (
    open_application,
    get_system_time,
    get_system_info,
    lock_pc,
    sleep_pc,
    shutdown_pc,
    cancel_shutdown,
    restart_pc,
    hibernate_pc,
)
from src.tools.media_tool import (
    play_pause_media,
    next_track,
    previous_track,
    volume_up,
    volume_down,
    mute_unmute,
)

# Master list of all tools the agent can use.
# Add new tools here as they are created.
ALL_TOOLS = [
    # Math
    calculate_expression,
    # Browser & Media Playback
    open_website,
    search_web,
    play_youtube,
    play_on_spotify,
    # System Apps
    open_application,
    get_system_time,
    get_system_info,
    # Power Management
    lock_pc,
    sleep_pc,
    shutdown_pc,
    cancel_shutdown,
    restart_pc,
    hibernate_pc,
    # Media Keys
    play_pause_media,
    next_track,
    previous_track,
    volume_up,
    volume_down,
    mute_unmute,
]
