---
description: /run command to start the main loop
---

# Run Assistant

**Full runbook — setup, configuration, testing, troubleshooting: [`_artifact/docs/05-runbook.md`](../../_artifact/docs/05-runbook.md)**

To start the main loop of Neo-Atom:

1. **Activate the environment:**
   ```bat
   call venv\Scripts\activate.bat
   ```

2. **Confirm Ollama is running** (check the system tray, or):
   ```bash
   ollama list
   ```
   The model must match `OLLAMA_MODEL` in `.env`.

3. **Execute the entry point:**
   ```bash
   python src/main.py
   ```

You should see the banner, then `🟢 Neo-Atom is ready.` Exit with `exit`, `quit`, `bye`, `goodbye`, `stop`, or `Ctrl-C`.

## Development

**Text mode is the only mode** — there is no `--text-only` flag, and none is needed; voice is not implemented. To exercise tools in isolation:

```bash
pytest tests/ -v
```
