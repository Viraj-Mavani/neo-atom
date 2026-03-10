# Neo-Atom Phased Implementation Plan

## Phase 1: Core Text-based Agent & Ollama Setup
**Goal:** Establish the fundamental intelligence of Neo-Atom using an offline LLM.
- **Code Implementation:**
  - Initialize the `src/main.py` entry point with a basic `asyncio` event loop.
  - Implement `src/brain/ollama_client.py` using `langchain-core` and `langchain-community` (specifically `ChatOllama` binding to `localhost:11434`).
  - Configure the system prompt instructing the AI on its identity (Neo-Atom) and constraints.
  - Test the LangChain agent with conversational text inside the CLI (no tools or voice yet).

## Phase 2: Implementing Basic Tools (Math, Web, OS)
**Goal:** Empower the Agent with local machine control and internet capabilities.
- **Code Implementation:**
  - Create `src/tools/math_tool.py`: Expose a LangChain `@tool` for calculating advanced expressions securely (using `asteval` or safe `eval`).
  - Create `src/tools/browser_tool.py`: Leverage Python's built-in `webbrowser` to open URLs or search YouTube directly.
  - Create `src/tools/system_tool.py`: A tool to execute safe Windows OS commands (e.g., launching an app via `os.startfile` or reading system status).
  - Bind these tools to the LangChain agent in `ollama_client.py` via `bind_tools()`.
  - Validate tool execution: Type "open youtube" -> Watch the LLM return the structured tool call -> Agent Executor runs the Python function.

## Phase 3: Voice Integration (STT/TTS loop)
**Goal:** Replace the CLI with a hands-free voice interface.
- **Code Implementation:**
  - Implement `src/voice/listener.py`: Use Python `sounddevice` and `faster-whisper` for high-speed local transcription on the CPU/GPU.
  - Implement `src/voice/speaker.py`: Integrate `piper-tts` to stream the LLM's text response back to the user audibly bypassing robotic system voices.
  - Wire the full `Listen -> Think -> Tool_Action -> Think -> Speak` flow inside `main.py`.

## Phase 4: Refinement, Memory, and Polish
**Goal:** Ensure the assistant is extremely fast, reliable, and remembers context.
- **Code Implementation:**
  - **Latency Optimization:** Implement generator streams for TTS. As the LLM generates tokens, pipe them immediately into `speaker.py` before the sentence finishes.
  - **Memory:** Implement `ConversationBufferWindowMemory` or SQLite for long-term recall.
  - **Hallucination Mitigation:** Hardcode specific system prompts to bind the agent tightly to tool usage and prevent it from inventing fake shell commands.

---

### Implementation Guidelines
- **Modularity:** Every tool in `src/tools/` MUST be a standalone Python function that the LLM can call.
- **Async Execution:** Use `asyncio` for the main loop so the assistant can "listen" for interruptions while "processing" or "speaking."
- **Environment:** Use a virtual environment. The provided `setup.bat` completely automates installation.
