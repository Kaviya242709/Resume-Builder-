import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Use the direct import approach with API key from .env
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY")
)


# SEQUENTIAL FLOW EXPLANATION:

# This CV builder follows CrewAI's sequential pattern:
#
# FLOW: User Input → COLLECTOR → FORMATTER → REVIEWER → Final CV
#
# Step 1: COLLECTOR extracts raw info from user text
# Step 2: FORMATTER uses low-level tools to format each section
# Step 3: REVIEWER polishes and quality checks the final CV
#
# Each step MUST complete before the next one starts (sequential execution)
# Output of each step becomes INPUT to the next step


# LOW LEVEL TOOLS (Basic Formatting Functions)

# WHY: These are atomic operations - they do ONE specific formatting task
# WHERE USED: Called by the FORMATTER AGENT (Agent 2) only
# SPECIALTY: @tool decorator makes regular Python functions usable by LangChain agents
#            Without @tool, agents cannot see or use these functions


@tool
def format_summary_section(
    professional_title: str,
    years_experience: str,
    key_strengths: str,
    career_goals: str,
) -> str:
    """Format professional summary section for CV"""
    # WHY: Creates consistent summary format
    # CALLED BY: formatter_agent when it needs to format summary section
    return f"""## Professional Summary
{professional_title} with {years_experience} of experience. {key_strengths}
{career_goals}
"""


@tool
def format_education_section(
    degree: str, institution: str, graduation_year: str, achievements: str
) -> str:
    """Format education section for CV"""
    # WHY: Creates consistent education format
    # CALLED BY: formatter_agent when it needs to format education section
    return f"""## Education
**{degree}**
{institution} | {graduation_year}
{achievements}
"""


@tool
def format_work_section(
    job_title: str, company: str, duration: str, responsibilities: str
) -> str:
    """Format work experience section for CV"""
    # WHY: Creates consistent work experience format
    # CALLED BY: formatter_agent when it needs to format work section
    return f"""## Work Experience
**{job_title}** at {company}
*{duration}*
{responsibilities}
"""


@tool
def format_skills_section(
    technical_skills: str, soft_skills: str, tools_technologies: str
) -> str:
    """Format skills section for CV"""
    # WHY: Creates consistent skills format with categorization
    # CALLED BY: formatter_agent when it needs to format skills section
    return f"""## Skills
**Technical Skills:** {technical_skills}
**Soft Skills:** {soft_skills}
**Tools & Technologies:** {tools_technologies}
"""


@tool
def format_certifications_section(
    certification_name: str, issuing_organization: str, date_obtained: str
) -> str:
    """Format certifications section for CV"""
    # WHY: Creates consistent certification format
    # CALLED BY: formatter_agent when it needs to format certifications section
    return f"""## Certifications
**{certification_name}**
Issued by: {issuing_organization} | {date_obtained}
"""


@tool
def format_achievements_section(
    achievement_title: str, description: str, impact: str
) -> str:
    """Format achievements section for CV"""
    # WHY: Creates consistent achievements format with measurable impact
    # CALLED BY: formatter_agent when it needs to format achievements section
    return f"""## Key Achievements
**{achievement_title}**
{description}
Impact: {impact}
"""


@tool
def format_projects_section(
    project_name: str, description: str, technologies: str, outcome: str
) -> str:
    """Format projects section for CV"""
    # WHY: Creates consistent project format showing technical skills
    # CALLED BY: formatter_agent when it needs to format projects section
    return f"""## Projects
**{project_name}**
{description}
Technologies: {technologies}
Outcome: {outcome}
"""


# AGENT 1: CV INFORMATION COLLECTOR (Matches CrewAI's Planner Role)

# WHY: Extracts and organizes raw user input into structured format
# WHEN USED: First step in the sequential pipeline
# TOOLS GIVEN: None (it just extracts info using LLM intelligence, no tools needed)
# OUTPUT: Organized text with all 7 sections clearly labeled


collector_agent = create_agent(
    model=model,
    tools=[],  # NO TOOLS - this agent only extracts and organizes information
    system_prompt="""You are a CV Information Collector.
        Role: Extract and organize ALL CV information from user input.
        Goal: Collect complete details for all 7 CV sections.
        Backstory: You're working on collecting comprehensive information for a professional CV.
        You analyze what the user provides and organize it into structured sections covering
        their entire professional profile.

        Extract information for these sections:
        1. SUMMARY - professional title, years of experience, key strengths, career goals
        2. EDUCATION - degree, institution, graduation year, academic achievements
        3. WORK EXPERIENCE - job title, company, duration, key responsibilities
        4. SKILLS - technical skills, soft skills, tools & technologies
        5. CERTIFICATIONS - certification name, issuing org, date obtained
        6. ACHIEVEMENTS - achievement title, description, measurable impact
        7. PROJECTS - project name, description, technologies used, outcomes

        Output in this exact format:

        SUMMARY:
        - Professional Title: [extracted]
        - Years of Experience: [extracted]
        - Key Strengths: [extracted]
        - Career Goals: [extracted]

        EDUCATION:
        - Degree: [extracted]
        - Institution: [extracted]
        - Graduation Year: [extracted]
        - Achievements: [extracted]

        WORK EXPERIENCE:
        - Job Title: [extracted]
        - Company: [extracted]
        - Duration: [extracted]
        - Responsibilities: [extracted]

        SKILLS:
        - Technical Skills: [extracted]
        - Soft Skills: [extracted]
        - Tools & Technologies: [extracted]

        CERTIFICATIONS:
        - Certification Name: [extracted]
        - Issuing Organization: [extracted]
        - Date Obtained: [extracted]

        ACHIEVEMENTS:
        - Achievement Title: [extracted]
        - Description: [extracted]
        - Impact: [extracted]

        PROJECTS:
        - Project Name: [extracted]
        - Description: [extracted]
        - Technologies: [extracted]
        - Outcome: [extracted]

        If any section is missing from user input, note it as "Not provided".""",
)


# WRAPPER TOOL 1: Wraps the Collector Agent

# WHY: Makes the collector_agent callable by the supervisor (cv_crew)
# SPECIALTY: This is a "HIGH-LEVEL TOOL" - it wraps an entire agent
#            Low-level tools do formatting, high-level tools invoke agents
# CALLING FLOW: cv_crew → process_collecting → collector_agent → returns organized text


@tool
def collect_cv_information(cv_details: str) -> str:
    """Task 1: Collect and organize all CV information.
    Extracts summary, education, work exp, skills, certifications, achievements, projects.

    This is a WRAPPER TOOL that invokes the collector_agent.
    It's called by the supervisor (cv_crew) in Step 1 of sequential flow."""

    # INVOKES the collector_agent and passes user's CV details
    result = collector_agent.invoke(
        {"messages": [{"role": "user", "content": cv_details}]}
    )
    # Returns the organized information from the agent's response
    return result["messages"][-1].content


# AGENT 2: CV FORMATTER (Matches CrewAI's Writer Role)

# WHY: Takes organized info and creates professionally formatted CV sections
# WHEN USED: Second step in sequential pipeline (after COLLECTOR)
# TOOLS GIVEN: All 7 format_*_section tools (low-level formatting tools)
# INPUT: Organized text from COLLECTOR
# OUTPUT: Fully formatted CV in markdown


formatter_agent = create_agent(
    model=model,
    # IMPORTANT: This agent has access to all 7 low-level formatting tools
    tools=[
        format_summary_section,  # Tool for formatting summary
        format_education_section,  # Tool for formatting education
        format_work_section,  # Tool for formatting work experience
        format_skills_section,  # Tool for formatting skills
        format_certifications_section,  # Tool for formatting certifications
        format_achievements_section,  # Tool for formatting achievements
        format_projects_section,  # Tool for formatting projects
    ],
    system_prompt="""You are a CV Formatter.
        Role: Format all CV sections professionally.
        Goal: Create a complete, well-formatted professional CV with all 7 sections.
        Backstory: You receive organized CV information from the Collector. You use formatting
        tools to create professionally structured CV sections following industry standards.

        Your tasks:
        1. Format SUMMARY using format_summary_section
        2. Format EDUCATION using format_education_section
        3. Format WORK EXPERIENCE using format_work_section
        4. Format SKILLS using format_skills_section
        5. Format CERTIFICATIONS using format_certifications_section
        6. Format ACHIEVEMENTS using format_achievements_section
        7. Format PROJECTS using format_projects_section

        Combine all sections into a cohesive, professional CV.
        Use proper markdown formatting with clear section headers.
        If a section wasn't provided by the user, skip it gracefully.""",
)


# WRAPPER TOOL 2: Wraps the Formatter Agent

# WHY: Makes the formatter_agent callable by the supervisor (cv_crew)
# SPECIALTY: High-level wrapper tool that invokes an agent with tools
# CALLING FLOW: cv_crew → format_cv_sections → formatter_agent → uses 7 low-level tools
# INPUT: Organized info from Step 1 (collect_cv_information output)


@tool
def format_cv_sections(collected_info: str) -> str:
    """Task 2: Format all CV sections professionally.
    Creates formatted output for all 7 sections.

    This is a WRAPPER TOOL that invokes the formatter_agent.
    It's called by the supervisor (cv_crew) in Step 2 of sequential flow.
    The formatter_agent will use the 7 low-level formatting tools."""

    request = f"""Format these CV details into professional sections:

{collected_info}

Use the appropriate formatting tools for each section to create a complete, professional CV."""

    # INVOKES the formatter_agent with the organized information
    result = formatter_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    # Returns the formatted CV from the agent's response
    return result["messages"][-1].content


# AGENT 3: CV REVIEWER (Matches CrewAI's Editor Role)

# WHY: Quality checks the formatted CV and polishes it for final output
# WHEN USED: Third/final step in sequential pipeline (after FORMATTER)
# TOOLS GIVEN: None (it just reviews using LLM intelligence, no tools needed)
# INPUT: Formatted CV from FORMATTER
# OUTPUT: Final polished, reviewed CV ready for use


reviewer_agent = create_agent(
    model=model,
    tools=[],  # NO TOOLS - this agent only reviews and polishes
    system_prompt="""You are a CV Reviewer and Quality Checker.
        Role: Review and polish the complete CV.
        Goal: Ensure the CV is comprehensive, professional, and ready for job applications.
        Backstory: You receive the formatted CV from the Formatter. You review it to ensure
        all sections are complete, properly formatted, and present the candidate effectively.

        Review checklist:
        1. Summary - Clear professional identity and value proposition
        2. Education - Complete academic background
        3. Work Experience - Clear responsibilities and achievements
        4. Skills - Relevant technical and soft skills
        5. Certifications - Valid credentials
        6. Achievements - Quantifiable results
        7. Projects - Technical capabilities demonstrated

        Check for:
        - Consistency in formatting
        - Clear, concise language
        - No grammatical errors
        - Professional tone throughout
        - Proper section ordering
        - Complete information in each section

        Provide the final, polished CV ready for job applications.""",
)


# WRAPPER TOOL 3: Wraps the Reviewer Agent

# WHY: Makes the reviewer_agent callable by the supervisor (cv_crew)
# SPECIALTY: Final high-level wrapper tool in the sequential chain
# CALLING FLOW: cv_crew → review_cv → reviewer_agent → returns final polished CV
# INPUT: Formatted CV from Step 2 (format_cv_sections output)


@tool
def review_cv(formatted_cv: str) -> str:
    """Task 3: Review and polish the complete CV.
    Final quality check for all 7 sections.

    This is a WRAPPER TOOL that invokes the reviewer_agent.
    It's called by the supervisor (cv_crew) in Step 3 of sequential flow."""

    request = f"""Review this complete CV for professional standards:

{formatted_cv}

Check all 7 sections (Summary, Education, Work Experience, Skills, Certifications, Achievements, Projects)
for completeness and quality. Provide the final, polished version."""

    # INVOKES the reviewer_agent with the formatted CV
    result = reviewer_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # Returns the final reviewed CV from the agent's response
    return result["messages"][-1].content


# SUPERVISOR AGENT: CV Crew Coordinator (Matches CrewAI's Crew)

# WHY: Orchestrates the entire sequential workflow
# ROLE: This is the SUPERVISOR - it manages and calls the 3 wrapper tools in order
# TOOLS GIVEN: 3 high-level wrapper tools (collect, format, review)
#
# CALLING HIERARCHY:
# cv_crew (supervisor)
#    ├─ calls collect_cv_information (wrapper tool 1)
#    │     └─ invokes collector_agent (agent 1, no tools)
#    │
#    ├─ calls format_cv_sections (wrapper tool 2)
#    │     └─ invokes formatter_agent (agent 2, has 7 low-level tools)
#    │           ├─ uses format_summary_section
#    │           ├─ uses format_education_section
#    │           ├─ uses format_work_section
#    │           ├─ uses format_skills_section
#    │           ├─ uses format_certifications_section
#    │           ├─ uses format_achievements_section
#    │           └─ uses format_projects_section
#    │
#    └─ calls review_cv (wrapper tool 3)
#          └─ invokes reviewer_agent (agent 3, no tools)


cv_crew = create_agent(
    model=model,
    # SUPERVISOR TOOLS: These are the 3 high-level wrapper tools
    # Each wrapper tool invokes a specialized agent
    tools=[
        collect_cv_information,  # Wrapper for Agent 1 (Collector)
        format_cv_sections,  # Wrapper for Agent 2 (Formatter)
        review_cv,  # Wrapper for Agent 3 (Reviewer)
    ],
    system_prompt="""You are a CV Building Crew Coordinator (SUPERVISOR).
    You manage the complete sequential CV building process for all 7 sections:
    1. Summary
    2. Education
    3. Work Experience
    4. Skills
    5. Certifications
    6. Achievements
    7. Projects

    CRITICAL: Execute these steps IN EXACT ORDER:

    Step 1 - COLLECT: Call collect_cv_information with user's CV details
       → Extract and organize all 7 sections
       → Save the organized information

    Step 2 - FORMAT: Call format_cv_sections with the organized information from Step 1
       → Format all 7 sections professionally
       → Save the formatted CV

    Step 3 - REVIEW: Call review_cv with the formatted CV from Step 2
       → Quality check all sections
       → This is the final output

    YOU MUST execute all three steps sequentially.
    Pass the output of each step as input to the next step.
    Return ONLY the final reviewed CV from Step 3.""",
)


# KICKOFF FUNCTION (Matches CrewAI's crew.kickoff method)

# WHY: Entry point to start the entire sequential CV building process
# WHAT IT DOES: Invokes the supervisor (cv_crew) which then orchestrates everything
#
# COMPLETE FLOW WHEN kickoff() IS CALLED:
# 1. kickoff() calls cv_crew (supervisor)
# 2. cv_crew calls collect_cv_information (wrapper tool)
# 3. collect_cv_information invokes collector_agent
# 4. collector_agent returns organized info
# 5. cv_crew calls format_cv_sections (wrapper tool) with organized info
# 6. format_cv_sections invokes formatter_agent
# 7. formatter_agent uses 7 low-level format tools to create CV
# 8. formatter_agent returns formatted CV
# 9. cv_crew calls review_cv (wrapper tool) with formatted CV
# 10. review_cv invokes reviewer_agent
# 11. reviewer_agent returns final polished CV
# 12. cv_crew returns final CV to kickoff()
# 13. kickoff() returns final CV to user


def kickoff(cv_details: str):
    """
    Execute the CV building crew with sequential tasks for all 7 sections.
    This is the ENTRY POINT - it starts the entire pipeline.

    Args:
        cv_details: User's complete CV information (raw text)

    Returns:
        Final polished CV with all sections (formatted markdown)

    Flow: kickoff → cv_crew → collect → format → review → final CV
    """
    # Invoke the SUPERVISOR agent (cv_crew) with user's CV details
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
    # Return the final CV from the supervisor's response
    return result["messages"][-1].content


# EXECUTION EXAMPLES - can be deleted one stored all your files in rag;)

# This demonstrates how to use the CV builder


if __name__ == "__main__":
    # Comprehensive CV example with all 7 sections
    result = kickoff(
        """
        I am a Senior Software Engineer with 5 years of experience specializing in cloud architecture
        and microservices. Strong problem-solver with excellent communication skills.
        Looking to lead engineering teams in innovative tech companies.

        I have a Bachelor's degree in Computer Science from MIT, graduated in 2019 with honors.

        Currently working as Software Engineer at Google for 3 years (2021-2024), where I design
        and implement scalable cloud infrastructure, lead a team of 5 engineers, and reduced
        system latency by 40%.

        My technical skills include Python, Java, Kubernetes, Docker, AWS, and microservices.
        I have strong leadership, communication, and agile methodology skills.
        I'm proficient with Git, Jenkins, Terraform, and Prometheus.

        I am AWS Certified Solutions Architect from Amazon Web Services, obtained in 2022.

        One of my key achievements was leading migration of monolithic application to microservices
        architecture, which reduced deployment time by 60% and improved system reliability to 99.9% uptime.

        I built an E-commerce Platform using React, Node.js, MongoDB, and Kubernetes, which now
        handles 100K+ daily transactions with 99.95% uptime.
        """
    )
    print(result)

    print("\n" + "=" * 80 + "\n")

    # Try it yourself with different profile
    cv_details = """
    Data Scientist with 3 years experience in machine learning and analytics.
    Master's in Data Science from Stanford, 2021.
    Working at Microsoft as Data Analyst, analyzing user behavior and building predictive models.
    Skills: Python, R, SQL, TensorFlow, scikit-learn, data visualization.
    Google Data Analytics Professional Certificate, 2022.
    Developed ML model that improved customer retention by 25%.
    Built recommendation system using collaborative filtering and deep learning.
    """
    result = kickoff(cv_details)
    print(result)


# ============================================================================
# SUMMARY OF ARCHITECTURE
# ============================================================================
#
# TOOL TYPES:
# 1. LOW-LEVEL TOOLS (7 total) - Basic formatting functions
#    - format_summary_section
#    - format_education_section
#    - format_work_section
#    - format_skills_section
#    - format_certifications_section
#    - format_achievements_section
#    - format_projects_section
#
# 2. HIGH-LEVEL WRAPPER TOOLS (3 total) - Invoke specialized agents
#    - collect_cv_information (wraps collector_agent)
#    - format_cv_sections (wraps formatter_agent)
#    - review_cv (wraps reviewer_agent)
#
# AGENTS:
# 1. collector_agent - Extracts info (no tools)
# 2. formatter_agent - Formats CV (has 7 low-level tools)
# 3. reviewer_agent - Reviews CV (no tools)
# 4. cv_crew - SUPERVISOR (has 3 high-level wrapper tools)
#
# SEQUENTIAL FLOW:
# User → kickoff() → cv_crew (supervisor)
#    → Step 1: collect_cv_information → collector_agent → organized info
#    → Step 2: format_cv_sections → formatter_agent (uses 7 tools) → formatted CV
#    → Step 3: review_cv → reviewer_agent → final polished CV
#    → Return to user
#
# WHY THIS ARCHITECTURE:
# - Separation of concerns: Each agent has one job
# - Reusability: Low-level tools can be reused
# - Sequential control: Supervisor ensures proper order
# - Matches CrewAI pattern: Planner → Writer → Editor workflow
# ============================================================================
