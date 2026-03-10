"""Neo-Atom: Entry point and main agent interaction loop."""

import asyncio
import logging
import sys
from pathlib import Path

# Ensure the project root (parent of src/) is on sys.path so imports work
# regardless of whether you run `python src/main.py` or `python -m src.main`
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from dotenv import load_dotenv

from src.brain.ollama_client import create_agent, run_agent_turn

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("neo-atom")

# ── Constants ──────────────────────────────────────────────────────────────────
BANNER = r"""
 ╔══════════════════════════════════════════════════╗
 ║   _   _                  _                       ║
 ║  | \ | | ___  ___       / \   ___ ___   _ __ ___  ║
 ║  |  \| |/ _ \/ _ \ ─── / _ \ / __/ _ \ | '_ ` _ \ ║
 ║  | |\  |  __/ (_) |   / ___ \ (_| (_) || | | | | |║
 ║  |_| \_|\___|\___/   /_/   \_\___\___/ |_| |_| |_|║
 ║                                                    ║
 ║       Local AI Assistant for Windows               ║
 ╚════════════════════════════════════════════════════╝
"""

EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "stop"}

# Maximum conversation history messages to keep (to avoid context overflow)
MAX_HISTORY_LENGTH = 20


def trim_history(conversation_history: list) -> list:
    """Trims conversation history to the last MAX_HISTORY_LENGTH messages.

    Keeps the most recent messages so the LLM retains context without overflowing.
    """
    if len(conversation_history) > MAX_HISTORY_LENGTH:
        return conversation_history[-MAX_HISTORY_LENGTH:]
    return conversation_history


async def text_mode_loop() -> None:
    """Runs the assistant in text-only CLI mode (Phase 1 default)."""
    load_dotenv()

    print(BANNER)
    logger.info("Initializing Neo-Atom in text mode...")

    try:
        llm_with_tools, tools_by_name = create_agent()
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        print(f"\n❌ Could not initialize agent: {e}")
        print("   Make sure Ollama is running and a model is pulled:")
        print("   > ollama run llama3.1:8b")
        sys.exit(1)

    conversation_history: list = []
    print("\n🟢 Neo-Atom is ready. Type your message (or 'exit' to quit).\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            print("\n👋 Goodbye! Neo-Atom signing off.")
            break

        try:
            response = await run_agent_turn(
                user_input=user_input,
                llm_with_tools=llm_with_tools,
                tools_by_name=tools_by_name,
                conversation_history=conversation_history,
            )
            conversation_history = trim_history(conversation_history)
            print(f"\nNeo-Atom: {response}\n")

        except Exception as e:
            logger.error(f"Error during agent turn: {e}", exc_info=True)
            print(f"\n⚠️  Something went wrong: {e}\n")


async def main() -> None:
    """Entry point: determines run mode and starts the appropriate loop."""
    # Phase 1: text mode only. Phase 3 will add voice mode.
    await text_mode_loop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Neo-Atom shut down gracefully by user.")
