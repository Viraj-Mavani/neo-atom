import logging
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# TODO: Import explicit Tools

logger = logging.getLogger(__name__)

def create_agent():
    """Initializes the LLM and binds tools."""
    logger.info("Initializing Agent with Ollama...")
    # llm = ChatOllama(model="llama3.1:8b", temperature=0)
    # tools = [math_tool, browser_tool, system_tool]
    # llm_with_tools = llm.bind_tools(tools)
    # return agent_executor
    ...
