# AI RESUME BUILDER: RAG driven career evolution
- An automated RAG based pipeline that evolves your career "Skeleton" into a polished LaTex "Skin".

## Introduction:-
- Building a resume shouldnt be a repetitive manual task or process. AI-Resume Builder is a production ready tool designed to solve the "RELEVANCE GAP" in job applications. Using Langgraph for state management and ChromaDB for semantic retrieval (RAG), this tool intelligently selects the most impactful experirence from your history and tailors them to fit specific JD and user needs. 

- By focusing on ATS and LaTex percision, this ensures your proffesional identity is always presented at its biological test.


## System Anatomy:(Architechtural diagram)
- Here the system is built as a Directed Acyclic Graph(DAG). As workflow is more essential for understanding how the "Nerves" interact with "Memory":

```mermaid
graph TD
    A["main.py<br/>Input JD"] --> B["graph.py<br/>Workflow Logic"]
    B --> C["nodes.py<br/>RAG Retrieval<br/>& Tailoring"]
    C --> D["state.py<br/>Memory Persistence"]
    D --> E["edges.py<br/>Conditional Routing"]
    E --> F["main.py<br/>Final LaTeX Output"]
```


## Setup & Installation
- For end users(Quick Start)
- If you just want to generate a resume, follow these steps:
1) Clone : git clone https://github.com/yourusername/Resume-Builder.git
2) Environment: Create a .env file and add your OPEN_API_KEY
3) Execute: 
   * Windows: python main.py
   * Linux/Mac: python3 main.py


# Guide to 'OPERATE THE ORGANISM'
- Follow the instruction to actually use the tool once its installed.

1) Prepare the Skeleton: Open master_resume.txt and paste your professional history.
2) Run the application: python main.py 
3) Feed the JD: When prompted , make sure you paste the Job Description you are targeting.
4) Retrieve teh skin: Once the process completes, find your tailored Final_resume.tex in the root folder and upload this to 'OVERLEAF' or your local LaTex compiler.


# Research DNA: Credits
- To give credit to the vedios and documents that helped me build each functions are as follows:
  * Vector Search : Inspired by https://docs.trychroma.com/docs/overview/getting-started. Used for high precision expereince retrieval | https://docs.trychroma.com/guides/deploy/gcp.
  * Workflow orchestration: Built using patterns from https://docs.langchain.com/oss/python/langgraph/overview.
  * Documentation: Structured based on https://www.youtube.com/watch?v=E6NO0rgFub4 | https://www.youtube.com/watch?v=T-D1OfcDW1M
  * Errors handling: https://stackoverflow.com/questions/2541616/how-to-escape-strip-special-characters-in-the-latex-document,


## Future Enhancement
```mermaid
graph TD
    subgraph Input_Layer [Environment & DNA]
        A[Job Description] --> B{The Engine}
        C[Master Career Skeleton] --> B
    end
    subgraph Processing_Layer [Nervous System]
        B --> D[RAG Retrieval Node]
        D --> E[Semantic Alignment]
        E --> F[Single LaTeX Template Engine]
    end
    subgraph Validation_Layer [The Immune System]
        F --> G{ATS Match Scorer}
        G -- Match > 85% --> H[Final Production PDF]
        
        G -- Match < 85% --> I[Gap Analysis Report]
        
        I --> J{Diagnosis}
        J -- "Wrong Domain (e.g. AI vs Security)" --> L[Hard Reject + Reason]
        J -- "Skill Gap" --> K[Learning Hub]
        
        K --> M[YouTube Playlists]
        K --> N[Technical Documentation]
    end
    style F fill:#d1e7ff,stroke:#004085
    style G fill:#fff3cd,stroke:#856404
    style K fill:#d4edda,stroke:#155724
    style L fill:#f8d7da,stroke:#721c24
```

## For contributors:(Developer setup)
- If you want to help evolve the organism:
1) Virtual Environment: python -m venv env
2) Activate:
   * Windows: .\env\Scripts\activate
   * Linux/Mac: source env/bin/activate
3) Dependencies: pip install -r requirements.txt
4) Docs: Refer to https://docs.langchain.com/oss/python/langgraph/install | https://docs.trychroma.com/docs/overview/getting-started


## The Biological Components:
- Ecosystem of my project are follows:-
 
|File                 |      Role           |           Description                                               |
|---------------------|---------------------|---------------------------------------------------------------------|
|master_resume.txt    |      Skeleton       |           Private. Your full, raw career DNA.                       |
|brain.py             |      Memory         |           The llm logic that adapts the content to the environment. |
|skeleton.py          |      Joints         |           Vector storage handling semantic search.                  |
|workflow.py          |      Blood          |           Circulates state through the nodes                        |
|main.py              |      Skin           |           The healing logic that cleans LaTex syntax.               |



## Contributors Expectations:~
- I welcome contributors! To keep the organism healthy
1) Issues first: Please open an issue before submitting a pull request.
2) Pull requests: Ensure your PR includes updated documentations if you modify the state.py or nodes.py
3) Code style: Maintain the "Human Body" naming convention where applicable.
