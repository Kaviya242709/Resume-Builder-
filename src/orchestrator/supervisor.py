from langchain.agents import create_agent

# Import from root level config
from config.prompts import SUPERVISOR_PROMPT

# Import from src modules
from src.utils.llm import get_llm
from src.tools.wrapper_tools import ALL_WRAPPER_TOOLS


# Create the supervisor agent
cv_crew = create_agent(
    model=get_llm(),
    tools=ALL_WRAPPER_TOOLS,
    system_prompt=SUPERVISOR_PROMPT,
)


def kickoff(cv_details: str) -> str:
    """
    Execute the CV building crew with sequential tasks.
    
    Args:
        cv_details: User's complete CV information (raw text)
    
    Returns:
        Final polished CV with all sections (formatted markdown)
    """
    result = cv_crew.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""Build a complete professional CV with these details:

{cv_details}

Execute all three sequential tasks to create a CV with these sections:
1. Professional Summary
2. Education
3. Work Experience
4. Skills
5. Certifications
6. Achievements
7. Projects

Collect → Format → Review all sections.""",
                }
            ]
        }
    )
    return result["messages"][-1].content