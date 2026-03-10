---
description: /run command to start the main loop
---

# Run Assistant

To start the main loop of Neo-Atom, simply follow these steps in your terminal:

1. **Ensure Environment is Active:**
   ```bash
   .\venv\Scripts\activate
   ```

2. **Verify Ollama is Running:**
   Ensure the Ollama application is active in your system tray or run:
   ```bash
   ollama run llama3.1:8b
   # Or whatever model is defined in the .env or client configuration.
   ```

3. **Execute the Entry Point:**
   ```bash
   python src/main.py
   ```

## Development Mode
If you want to run the assistant in CLI text mode only (skipping Voice activation for debugging tools), pass the `--text-only` flag if implemented, or simply test individual modules using `pytest tests/`.
