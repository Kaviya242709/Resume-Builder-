from langchain.tools import tool


@tool
def format_summary_section(
    professional_title: str,
    years_experience: str,
    key_strengths: str,
    career_goals: str,
) -> str:
    """Formats the professional summary section of a CV with title, experience, strengths, and goals."""
    return f"\\section*{{Professional Summary}}\n{professional_title} — {years_experience} experience.\n{key_strengths}\n{career_goals}\n"


@tool
def format_education_section(
    degree: str, institution: str, graduation_year: str, achievements: str
) -> str:
    """Formats the education section of a CV with degree, institution, graduation year, and achievements."""
    return f"\\section*{{Education}}\n\\textbf{{{degree}}} — {institution} ({graduation_year})\n{achievements}\n"


@tool
def format_work_section(
    job_title: str, company: str, duration: str, responsibilities: str
) -> str:
    """Formats the work experience section of a CV with job title, company, duration, and responsibilities."""
    return f"\\section*{{Work Experience}}\n\\textbf{{{job_title}}} — {company} \\textit{{{duration}}}\n{responsibilities}\n"


@tool
def format_skills_section(
    technical_skills: str, soft_skills: str, tools_technologies: str
) -> str:
    """Formats the skills section of a CV with technical skills, soft skills, and tools/technologies."""
    return f"\\section*{{Skills}}\nTechnical: {technical_skills}\nSoft: {soft_skills}\nTools: {tools_technologies}\n"


@tool
def format_certifications_section(
    certification_name: str, issuing_organization: str, date_obtained: str
) -> str:
    """Formats the certifications section of a CV with certification name, issuing organization, and date obtained."""
    return f"\\section*{{Certifications}}\n\\textbf{{{certification_name}}} — {issuing_organization} ({date_obtained})\n"


@tool
def format_achievements_section(
    achievement_title: str, description: str, impact: str
) -> str:
    """Formats the key achievements section of a CV with achievement title, description, and impact."""
    return f"\\section*{{Key Achievements}}\n\\textbf{{{achievement_title}}}\n{description}\nImpact: {impact}\n"


@tool
def format_projects_section(
    project_name: str, description: str, technologies: str, outcome: str
) -> str:
    """Formats the projects section of a CV with project name, description, technologies used, and outcome."""
    return f"\\section*{{Projects}}\n\\textbf{{{project_name}}}\n{description}\nTechnologies: {technologies}\nOutcome: {outcome}\n"


# Export list so formatter_agent can import it
ALL_FORMATTING_TOOLS = [
    format_summary_section,
    format_education_section,
    format_work_section,
    format_skills_section,
    format_certifications_section,
    format_achievements_section,
    format_projects_section,
]
