---
description: Phase 2 Implementation Plan - Expanded Tools and Context
---

# Phase 2: Implementing Advanced Tools and Context

This phase significantly expands Neo-Atom's capabilities beyond basic queries, turning it into a deeply integrated Windows assistant that understands user intent and developer context.

## 2.1 The Scope and Strategy
Before Phase 3 (Voice Integration), Neo-Atom must flawlessly control the OS and distinguish when to act vs. when to converse.
- **How:** We will add specialized Python libraries (`pyautogui` or `keyboard` for keystrokes, `os`/`ctypes` for power states) and refine the LangChain Agent's core system prompt.
- **Why:** To move from a "chatbot that can open a browser" to a "local OS agent" that natively handles media playback, screen locks, and understands who created it.
- **API Keys:** No external API keys are strictly required for YouTube (we use browser automation) or local OS control. If we integrate native Spotify API later, that would require Spotify Developer credentials (Client ID/Secret).

## 2.2 System Power & Media Controls
*We need to give the agent direct control over hardware states and media playback.*
1. **Power Management Tool (`system_tool.py`):** Add functions to lock the workstation, put the PC to sleep, hibernate, or shut down using native Windows `rundll32` and `shutdown` commands.
2. **Media Keystrokes Tool (`media_tool.py`):** Implement a new tool using `pyautogui` or a similar library to simulate native Windows media keys (Play/Pause, Volume Up/Down, Mute, Next Track).

## 2.3 Context & Intent Routing (The Brain)
*The LLM needs to know you and accurately decide WHEN to use tools versus just chatting.*
1. **Developer Context:** Update `SYSTEM_PROMPT` in `ollama_client.py` to hardcode your identity (Developer: Viraj Mavani, Website: etc.).
2. **Strict Tool Routing Rules:** Refine the prompt logic to forcefully prevent the LLM from searching the web for conversational questions. It must understand the difference between:
   - *"What is quantum physics?"* -> Answer directly.
   - *"Search google for quantum physics news"* -> Use `search_web`.
   - *"Play lofi hip hop"* -> Use `search_youtube` (and potentially append "autoplay").
3. **YouTube Playback Automation:** Enhance the browser tool to not just search YouTube, but actively select and play the first result if the user says "play X".

## 2.4 Complex Math & Final Polish
*Ensure math is bulletproof before voice.*
1. **Math Verification:** Ensure the existing `asteval` implementation in `math_tool.py` handles complex orders of operations and trigonometric functions.
2. **Unit Testing Phase 2:** Write comprehensive automated tests for the new power states (mocked!) and media controls to guarantee safety.
