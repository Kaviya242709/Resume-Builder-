from langchain.agents import create_agent

# Import from root level config folder
from config.prompts import COLLECTOR_PROMPT

# Import from src.utils
from src.utils.llm import get_llm


# Create the collector agent
collector_agent = create_agent(
    model=get_llm(),
    tools=[],  # No tools needed
    system_prompt=COLLECTOR_PROMPT,
)