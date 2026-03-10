---
description: Neo-Atom Coding Standards
---

# Neo-Atom Coding Standards

1. **Type Hints:** All functions and methods must use Python type hints (e.g., `def calculate(a: int, b: int) -> int:`).
2. **Docstrings:** All modules, classes, and complex functions must have Google-style docstrings. When creating LangChain `@tool`s, the docstring is *critical* because it acts as the prompt that instructs the LLM on what the tool does.
3. **Async IO:** The main loop (`main.py`) and network/IO dependent tools should be asynchronous (`async def`) using the `asyncio` library to prevent blocking the UI/Voice thread.
4. **Error Handling/Logging:** Do not use plain `print()` statements for everything. Use the standard `logging` library. Any tool that could fail (network requests, OS commands) must be enclosed in `try...except` blocks and return a graceful error string rather than raising a fatal exception, so the LLM can apologize or retry.
5. **Modularity:** Tools in `src/tools/` must be completely independent functions that do not rely on global state.
6. **Secrets:** API keys or system paths should never be hardcoded. Load from `.env` using `python-dotenv`.
