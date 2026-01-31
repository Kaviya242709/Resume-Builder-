import re
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class CareerState(TypedDict):
    job_description: str
    original_CV: str
    laTex_CV_template: str
    final_CV: str


class Workflow:
    def __init__(self, brain, skeleton):
        self.brain = brain
        self.skeleton = skeleton

    def _sanitize_fragment(self, text: str) -> str:
        """Remove common wrapper text that the model might echo back."""
        if not text:
            return ""
        s = text.strip()

        # Remove fenced code markers
        s = s.replace("```latex", "").replace("```", "").strip()

        # If the model echoed entire template or LaTeX preamble, cut that out
        if "\\documentclass" in s:
            s = s.split("\\documentclass")[0].strip()

        # Remove leading bracketed section headers like [SKILLS], [SUMMARY], [ACTUAL HISTORY]
        s = re.sub(r"^(?:\[[A-Z _\-]+\]\s*)+", "", s, flags=re.IGNORECASE)

        # Remove any accidental "OUTPUT:" or "OUTPUT FORMAT" blocks that LLM may add
        s = re.sub(r"(?mi)^\s*(output[:]|output format[:]).*$", "", s)

        return s.strip()

    def _escape_fragment_for_latex(self, text: str) -> str:
        """
        Escape LaTeX-sensitive characters inside a user-generated fragment.
        We intentionally DO NOT touch LaTeX macro lines (skills should be macros).
        Use this only for summary and experience plain-text bullets.
        """
        if not text:
            return ""
        # Escape backslashes first (rare), then &, #, %
        text = text.replace("\\", r"\\")
        text = text.replace("&", r"\&")
        text = text.replace("#", r"\#")
        # Escape raw percent signs (%% in templates or comments should not be present here)
        text = text.replace("%", r"\%")
        return text

    # fetch data -> node
    def recall_memories(self, state: CareerState):
        """Step 1: Get full history from ChromaDB"""
        full_history = self.skeleton.recall()
        print("History fetched, Whoahh!")

        # MUST merge with existing state
        return {
            **state,
            "original_CV": full_history,
        }

    # optimize the cv - > node
    def shaping_thePersona(self, state: CareerState):
        """Step 2: Generate optimized CV fragments"""
        rules_path = "uk_standards.txt"
        if not state["original_CV"]:
            print("OMG! The Brain has no memories (original_CV is empty)!")
        print("Generating identity, Please wait")
        summary_piece = self.brain.identity(
            state["job_description"], state["original_CV"], rules_path
        )

        print("Generating toolkit, Almost there - hangOn!")
        skills_piece = self.brain.toolkit(
            state["job_description"],
            state["original_CV"],
            state["original_CV"],
            rules_path,
        )

        print("Generating journey, Completed, hangOn!")
        exp_piece = self.brain.journey(
            state["job_description"], state["original_CV"], rules_path
        )
        print(f"Journey generated: {len(exp_piece)} chars")

        # assemble final CV
        template = state["laTex_CV_template"]

        #  do the template have the tags?
        if "[SUMMARY]" not in template:
            print("Tag nammed [SUMMARY] not found in the template!")
        # Assemble final CV
        template = state["laTex_CV_template"]
        final_latex = template.replace("[SUMMARY]", summary_piece)
        final_latex = final_latex.replace("[SKILLS]", skills_piece)
        final_latex = final_latex.replace("[EXPERIENCE]", exp_piece)

        # Must merge with existing state
        return {
            **state,
            "final_CV": final_latex,
        }

    def orchestrate_the_spirit(self):  # this is where the life flow is defined
        builder = StateGraph(CareerState)
        # adding steps of life flow
        builder.add_node("fetch", self.recall_memories)
        builder.add_node("optimizing", self.shaping_thePersona)
        # defining the natrual progression between
        builder.add_edge(START, "fetch")
        builder.add_edge("fetch", "optimizing")
        builder.add_edge("optimizing", END)

        return builder.compile()
