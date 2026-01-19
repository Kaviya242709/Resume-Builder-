from langchain.agents import create_agent

# Import from root level config folder
from config.prompts import REVIEWER_PROMPT

# Import from src.utils
from src.utils.llm import get_llm


# Create the reviewer agent
reviewer_agent = create_agent(
    model=get_llm(),
    tools=[],  # No tools needed
    system_prompt=REVIEWER_PROMPT,
)