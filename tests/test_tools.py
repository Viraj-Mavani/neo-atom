"""Unit tests for Neo-Atom tools (Phase 1 + Phase 2)."""

import pytest
from unittest.mock import patch, MagicMock


# ── Math Tool Tests ────────────────────────────────────────────────────────────

class TestMathTool:
    """Tests for the math calculation tool."""

    def test_basic_addition(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "2 + 2"})
        assert result == "4"

    def test_multiplication(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "15 * 42"})
        assert result == "630"

    def test_exponentiation(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "2 ** 8"})
        assert result == "256"

    def test_float_division(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "10 / 3"})
        assert "3.333" in result

    def test_complex_order_of_operations(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "(2 + 3) * (7 - 1) / 2"})
        assert result == "15.0"

    def test_sqrt(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "sqrt(144)"})
        assert result == "12.0"

    def test_trig_sin(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "sin(0)"})
        assert result == "0.0"

    def test_large_exponent(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "2 ** 20"})
        assert result == "1048576"

    def test_invalid_expression(self):
        from src.tools.math_tool import calculate_expression
        result = calculate_expression.invoke({"expression": "foo + bar"})
        assert "error" in result.lower() or "Error" in result


# ── System Tool Tests ──────────────────────────────────────────────────────────

class TestSystemTool:
    """Tests for the system tools."""

    def test_get_system_time(self):
        from src.tools.system_tool import get_system_time
        result = get_system_time.invoke({})
        assert "current date and time" in result.lower()

    def test_get_system_info(self):
        from src.tools.system_tool import get_system_info
        result = get_system_info.invoke({})
        assert "OS:" in result
        assert "Username:" in result

    def test_blocked_app(self):
        from src.tools.system_tool import open_application
        result = open_application.invoke({"app_name": "malware.exe"})
        assert "not in my approved list" in result

    def test_whitelisted_app_names(self):
        """Check that common app aliases are in the whitelist."""
        from src.tools.system_tool import _SAFE_APPS
        assert "chrome" in _SAFE_APPS
        assert "vs code" in _SAFE_APPS
        assert "spotify" in _SAFE_APPS
        assert "discord" in _SAFE_APPS
        assert "calculator" in _SAFE_APPS
        assert "terminal" in _SAFE_APPS

    @patch("src.tools.system_tool.ctypes")
    def test_lock_pc(self, mock_ctypes):
        from src.tools.system_tool import lock_pc
        result = lock_pc.invoke({})
        assert "locked" in result.lower()
        mock_ctypes.windll.user32.LockWorkStation.assert_called_once()

    @patch("src.tools.system_tool.subprocess.run")
    def test_shutdown_pc(self, mock_run):
        from src.tools.system_tool import shutdown_pc
        result = shutdown_pc.invoke({})
        assert "shutdown" in result.lower()
        mock_run.assert_called_once_with(["shutdown", "/s", "/t", "30"], check=True)

    @patch("src.tools.system_tool.subprocess.run")
    def test_cancel_shutdown(self, mock_run):
        from src.tools.system_tool import cancel_shutdown
        result = cancel_shutdown.invoke({})
        assert "cancelled" in result.lower()
        mock_run.assert_called_once_with(["shutdown", "/a"], check=True)

    @patch("src.tools.system_tool.subprocess.run")
    def test_restart_pc(self, mock_run):
        from src.tools.system_tool import restart_pc
        result = restart_pc.invoke({})
        assert "restart" in result.lower()
        mock_run.assert_called_once_with(["shutdown", "/r", "/t", "30"], check=True)

    @patch("src.tools.system_tool.subprocess.run")
    def test_hibernate_pc(self, mock_run):
        from src.tools.system_tool import hibernate_pc
        result = hibernate_pc.invoke({})
        assert "hibernat" in result.lower()
        mock_run.assert_called_once_with(["shutdown", "/h"], check=True)

    @patch("src.tools.system_tool.subprocess.run")
    def test_sleep_pc(self, mock_run):
        from src.tools.system_tool import sleep_pc
        result = sleep_pc.invoke({})
        assert "sleep" in result.lower()


# ── Browser Tool Tests ─────────────────────────────────────────────────────────

class TestBrowserTool:
    """Tests for the browser tools."""

    @patch("src.tools.browser_tool.webbrowser.open")
    def test_open_website(self, mock_open):
        from src.tools.browser_tool import open_website
        result = open_website.invoke({"url": "https://example.com"})
        assert "example.com" in result
        mock_open.assert_called_once()

    @patch("src.tools.browser_tool.webbrowser.open")
    def test_search_web(self, mock_open):
        from src.tools.browser_tool import search_web
        result = search_web.invoke({"query": "Python tutorial"})
        assert "Python tutorial" in result
        mock_open.assert_called_once()

    @patch("src.tools.browser_tool.webbrowser.open")
    def test_play_youtube(self, mock_open):
        from src.tools.browser_tool import play_youtube
        result = play_youtube.invoke({"query": "lofi hip hop"})
        assert "lofi hip hop" in result
        assert "YouTube" in result
        mock_open.assert_called_once()

    @patch("src.tools.browser_tool.webbrowser.open")
    def test_play_on_spotify(self, mock_open):
        from src.tools.browser_tool import play_on_spotify
        result = play_on_spotify.invoke({"query": "Blinding Lights"})
        assert "Blinding Lights" in result
        assert "Spotify" in result
        mock_open.assert_called_once()


# ── Media Tool Tests ───────────────────────────────────────────────────────────

class TestMediaTool:
    """Tests for media key simulation tools."""

    @patch("src.tools.media_tool.pyautogui")
    def test_play_pause(self, mock_pyautogui):
        from src.tools.media_tool import play_pause_media
        result = play_pause_media.invoke({})
        assert "play/pause" in result.lower()
        mock_pyautogui.press.assert_called_once_with("playpause")

    @patch("src.tools.media_tool.pyautogui")
    def test_next_track(self, mock_pyautogui):
        from src.tools.media_tool import next_track
        result = next_track.invoke({})
        assert "next" in result.lower()
        mock_pyautogui.press.assert_called_once_with("nexttrack")

    @patch("src.tools.media_tool.pyautogui")
    def test_previous_track(self, mock_pyautogui):
        from src.tools.media_tool import previous_track
        result = previous_track.invoke({})
        assert "previous" in result.lower()
        mock_pyautogui.press.assert_called_once_with("prevtrack")

    @patch("src.tools.media_tool.pyautogui")
    def test_volume_up(self, mock_pyautogui):
        from src.tools.media_tool import volume_up
        result = volume_up.invoke({})
        assert "volume" in result.lower()
        mock_pyautogui.press.assert_called_once_with("volumeup")

    @patch("src.tools.media_tool.pyautogui")
    def test_volume_down(self, mock_pyautogui):
        from src.tools.media_tool import volume_down
        result = volume_down.invoke({})
        assert "volume" in result.lower()
        mock_pyautogui.press.assert_called_once_with("volumedown")

    @patch("src.tools.media_tool.pyautogui")
    def test_mute_unmute(self, mock_pyautogui):
        from src.tools.media_tool import mute_unmute
        result = mute_unmute.invoke({})
        assert "mute" in result.lower()
        mock_pyautogui.press.assert_called_once_with("volumemute")


# ── Tool Registry Test ─────────────────────────────────────────────────────────

class TestToolRegistry:
    """Verify all tools are registered correctly."""

    def test_all_tools_count(self):
        from src.tools import ALL_TOOLS
        assert len(ALL_TOOLS) == 20, f"Expected 20 tools, got {len(ALL_TOOLS)}"

    def test_all_tools_have_names(self):
        from src.tools import ALL_TOOLS
        for tool in ALL_TOOLS:
            assert hasattr(tool, "name"), f"Tool {tool} is missing a name attribute"
            assert tool.name, f"Tool has empty name"
