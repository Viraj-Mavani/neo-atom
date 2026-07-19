---
description: Neo-Atom Coding Standards
---

# Neo-Atom Coding Standards

**Full standards, with per-rule compliance status and rationale: [`_artifact/docs/04-coding-standards.md`](../../_artifact/docs/04-coding-standards.md)**

The six binding rules, in brief:

1. **Type Hints** — every function and method. For `@tool` functions, argument types *become the JSON schema the model fills in*; an untyped argument is an unusable tool.
2. **Docstrings** — Google-style, on all modules, classes, and complex functions. For LangChain `@tool`s the docstring **is the prompt** — it is the only description the LLM receives.
3. **Async IO** — `main.py` and all network/IO-dependent tools must be genuinely asynchronous, so nothing blocks the loop. ⚠️ *Currently violated: `async` is used but nothing runs concurrently. Blocking calls must be `await`ed or offloaded via `asyncio.to_thread`.*
4. **Error Handling & Logging** — use `logging`, not `print()`. Any tool that can fail (network, OS commands) must be wrapped in `try/except` and **return a graceful error string rather than raising**, so the LLM can apologise or retry.
5. **Modularity** — tools in `src/tools/` are standalone functions with no global state and no cross-tool imports.
6. **Secrets** — never hardcode API keys or system paths. Load from `.env` via `python-dotenv`.

Four further rules — security in code (never in the prompt), destructive-action confirmation, test-pinned safety invariants, and structured logging — are defined in `_artifact/docs/04` and are equally binding.
