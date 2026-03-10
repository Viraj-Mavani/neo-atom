# Neo-Atom: Local Windows AI Assistant

Neo-Atom is a state-of-the-art, voice-activated Personal AI Assistant designed natively for Windows. It prioritizes absolute privacy by processing Large Language Models locally using Ollama (Llama-3/Mistral) and executes tasks via a robust Agentic Tool Calling architecture instead of rigid scripts.

## Core Features
- **Local AI Brain:** Powered by Ollama + LangChain Tool Architecture.
- **Micro-Latency Transcription:** Uses `faster-whisper` to interpret voice instantly.
- **Natural Voice:** Text-To-Speech powered by Piper.
- **Extensible Toolkit:** Natively controls math, open system apps, and searches the web autonomously.

## Getting Started

1. **Setup:**
   Run the included batch script to initialize Python and install dependencies:
   ```bash
   setup.bat
   ```

2. **Configure:**
   Ensure Ollama is running (`ollama run llama3.1:8b`). Update the `.env` file if needed.

3. **Run:**
   Activate your environment and start the agent:
   ```bash
   call venv\Scripts\activate.bat
   python src/main.py
   ```

*See `.agent/workflows/Phased_Implementation_Plan.md` for our exact roadmap.*
