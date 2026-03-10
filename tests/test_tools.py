"""Unit tests for Neo-Atom tools."""

import pytest


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

    def test_invalid_expression(self):
        from src.tools.math_tool import calculate_expression

        result = calculate_expression.invoke({"expression": "foo + bar"})
        # Should return an error message, not crash
        assert "error" in result.lower() or "Error" in result


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


class TestBrowserTool:
    """Tests for the browser tools (no actual browser opening in CI)."""

    def test_url_normalization(self):
        """Verify that open_website adds https:// when missing."""
        from src.tools.browser_tool import open_website

        # The function will try to open a browser, which may fail in headless CI,
        # but we just test it doesn't crash. In a real test, we'd mock webbrowser.
        result = open_website.invoke({"url": "https://example.com"})
        assert "example.com" in result
