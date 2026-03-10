# Neo-Atom Project Specifications

## Tech Stack Recommendations

### 1. Speech-to-Text (STT)
- **Recommendation:** `faster-whisper`
- **Justification:** Faster-Whisper is a reimplementation of OpenAI's Whisper model using CTranslate2. It is drastically faster than the original `whisper` library and requires significantly less memory. This makes it ideal for a real-time voice assistant running locally on Windows. It works efficiently on a CPU but can be accelerated considerably if an NVIDIA GPU is available.

### 2. Text-to-Speech (TTS)
- **Recommendation:** `piper-tts` (Piper)
- **Justification:** Piper is a fast, local neural Text-to-Speech engine. Unlike `pyttsx3`, which sounds robotic and uses legacy OS voices, Piper is highly natural and allows for a variety of high-quality voices while running totally offline. 
- *(Alternative: `edge-tts` if an internet connection is acceptable. It leverages Microsoft's Edge TTS API for free, yielding the absolute highest possible quality with zero latency. For a 100% offline goal, Piper remains the top choice).*

### 3. Large Language Model (LLM) Integration
- **Recommendation:** `ollama` (running `llama3.1:8b` or `mistral-nemo`)
- **Justification:** Ollama is the premier local LLM runner for Windows, running silently in the background and exposing a fast, OpenAI-compatible local API. `llama3.1:8b` is currently the state-of-the-art for its size, especially regarding its native ability to perform Tool Calling/Function Calling accurately.

### 4. Agent Framework
- **Recommendation:** `langchain` (using `langchain-core` and `langchain-community`)
- **Justification:** Rather than brittle `if/else` keyword matching or massive regex trees, LangChain allows us to define standard Python functions and decorate them as tools (`@tool`). We can bind these tools to the Ollama model. The LLM natively analyzes the user's prompt (e.g., "What is 15 * 42?") and dynamically decides to execute the `math_tool` autonomously, extracting and passing the correct arguments.

---

## Conceptual Architecture Flow

1. **Wake/Listen:** `voice/listener.py` records audio from the microphone (using VAD - Voice Activity Detection to know when you stop speaking) and transcribes it instantly using `faster-whisper`.
2. **Think/Decide:** The transcribed text is sent to the LangChain Agent located in `brain/ollama_client.py`. The LLM evaluates if it needs to use a tool (like `math_tool.py` or `system_tool.py`) to fulfill the request, or if it should just respond conversationally.
3. **Act:** If a tool is necessary, the Agent Executor automatically runs the relevant Python function in `src/tools/` and feeds the result back into the LLM's context.
4. **Respond:** The LLM formulates the final conversational text based on the tool's output.
5. **Speak:** `voice/speaker.py` receives the LLM's text and synthesizes it into natural speech using `piper-tts` (or `edge-tts`), streaming the audio back to the user.
