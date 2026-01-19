from langchain.agents import create_agent

# Import from root level config folder
from config.prompts import FORMATTER_PROMPT

# Import from src modules
from src.utils.llm import get_llm
from src.tools.formatting_tools import ALL_FORMATTING_TOOLS


# Create the formatter agent
formatter_agent = create_agent(
    model=get_llm(),
    tools=ALL_FORMATTING_TOOLS,
    system_prompt=FORMATTER_PROMPT,
)