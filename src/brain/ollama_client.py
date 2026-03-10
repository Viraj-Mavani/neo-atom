"""Ollama Client: Initializes the LangChain Agent with Ollama and tool bindings."""

import logging
import os

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from src.tools import ALL_TOOLS

logger = logging.getLogger(__name__)

# ── System Prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Neo-Atom, a highly capable local AI assistant running on Windows.
You are helpful, concise, and friendly. You speak naturally and conversationally.

RULES:
1. When the user asks you to do something actionable (open an app, calculate, search the web), \
you MUST use the appropriate tool. Do NOT pretend to do things.
2. If you don't have a tool for the request, say so honestly.
3. Keep responses SHORT — you are a voice assistant, so brevity is critical.
4. NEVER fabricate tool results. If a tool returns an error, inform the user.
5. For math, ALWAYS use the calculate_expression tool instead of computing in your head.
6. When greeting or chatting casually, respond conversationally without using tools."""


def create_agent(
    model: str | None = None,
    base_url: str | None = None,
    temperature: float = 0.1,
) -> tuple:
    """Creates and returns the ChatOllama LLM instance bound with tools.

    Args:
        model: The Ollama model name (defaults to env MODEL_NAME or 'llama3.1:8b').
        base_url: Ollama server URL (defaults to env OLLAMA_BASE_URL or 'http://localhost:11434').
        temperature: Sampling temperature for the LLM.

    Returns:
        A tuple of (llm_with_tools, tools_by_name) where tools_by_name maps
        tool names to their callable functions for agent execution.
    """
    model = model or os.getenv("MODEL_NAME", "llama3.1:8b")
    base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

    logger.info(f"Connecting to Ollama at {base_url} with model '{model}'...")

    llm = ChatOllama(
        model=model,
        base_url=base_url,
        temperature=temperature,
    )

    # Bind all tools to the LLM so it can invoke them dynamically
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # Build a name -> callable lookup for executing tool calls
    tools_by_name: dict = {tool.name: tool for tool in ALL_TOOLS}

    logger.info(
        f"Agent initialized with {len(ALL_TOOLS)} tools: "
        f"{', '.join(tools_by_name.keys())}"
    )

    return llm_with_tools, tools_by_name


def build_messages(
    conversation_history: list,
) -> list:
    """Prepends the system prompt to the conversation history.

    Args:
        conversation_history: List of LangChain message objects.

    Returns:
        Full message list with system prompt prepended.
    """
    return [SystemMessage(content=SYSTEM_PROMPT)] + conversation_history


async def run_agent_turn(
    user_input: str,
    llm_with_tools,
    tools_by_name: dict,
    conversation_history: list,
) -> str:
    """Executes a single turn of the agent: send user message, handle tool calls, return final response.

    Args:
        user_input: The user's text input.
        llm_with_tools: The LLM instance with tools bound.
        tools_by_name: The name -> tool callable mapping.
        conversation_history: Mutable list of conversation messages (modified in-place).

    Returns:
        The assistant's final text response for this turn.
    """
    # 1. Add user message to history
    conversation_history.append(HumanMessage(content=user_input))

    # 2. Build full messages and invoke LLM
    messages = build_messages(conversation_history)
    ai_response: AIMessage = await llm_with_tools.ainvoke(messages)
    conversation_history.append(ai_response)

    # 3. If the LLM wants to call tools, execute them in a loop
    while ai_response.tool_calls:
        for tool_call in ai_response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            logger.info(f"🔧 Tool call: {tool_name}({tool_args})")

            tool_fn = tools_by_name.get(tool_name)
            if tool_fn is None:
                result = f"Error: Tool '{tool_name}' not found."
                logger.error(result)
            else:
                try:
                    result = tool_fn.invoke(tool_args)
                except Exception as e:
                    result = f"Error executing {tool_name}: {e}"
                    logger.error(result)

            # 4. Feed tool result back to the LLM
            conversation_history.append(
                ToolMessage(content=str(result), tool_call_id=tool_id)
            )

        # 5. Re-invoke LLM with updated context to get final answer or more tool calls
        messages = build_messages(conversation_history)
        ai_response = await llm_with_tools.ainvoke(messages)
        conversation_history.append(ai_response)

    return ai_response.content
