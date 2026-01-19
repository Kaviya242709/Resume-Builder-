from langchain.tools import tool

# Import agents from src.agents
from src.agents.collector import collector_agent
from src.agents.formatter import formatter_agent
from src.agents.reviewer import reviewer_agent


@tool
def collect_cv_information(cv_details: str) -> str:
    """Task 1: Collect and organize all CV information."""
    result = collector_agent.invoke(
        {"messages": [{"role": "user", "content": cv_details}]}
    )
    return result["messages"][-1].content


@tool
def format_cv_sections(collected_info: str) -> str:
    """Task 2: Format all CV sections professionally."""
    request = f"""Format these CV details into professional sections:

{collected_info}

Use the appropriate formatting tools for each section to create a complete, professional CV."""
    
    result = formatter_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return result["messages"][-1].content


@tool
def review_cv(formatted_cv: str) -> str:
    """Task 3: Review and polish the complete CV."""
    request = f"""Review this complete CV for professional standards:

{formatted_cv}

Check all 7 sections for completeness and quality. Provide the final, polished version."""
    
    result = reviewer_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return result["messages"][-1].content


# Export all wrapper tools
ALL_WRAPPER_TOOLS = [
    collect_cv_information,
    format_cv_sections,
    review_cv,
]