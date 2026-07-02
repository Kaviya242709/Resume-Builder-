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
        s = s.replace("```latex", "").replace("```", "").strip()
        if "\\documentclass" in s:
            s = s.split("\\documentclass")[0].strip()
        s = re.sub(r"^(?:\[[A-Z _\-]+\]\s*)+", "", s, flags=re.IGNORECASE)
        s = re.sub(r"(?mi)^\s*(output[:]|output format[:]).*$", "", s)
        return s.strip()

    def recall_memories(self, state: CareerState):
        """Step 1: Get full history from ChromaDB"""
        full_history = self.skeleton.recall()
        print("History fetched, Whoahh!")
        return {**state, "original_CV": full_history}

    def shaping_thePersona(self, state: CareerState):
        """Step 2: Generate optimized CV fragments and assemble"""
        rules_path = "uk_standards.txt"

        if not state["original_CV"]:
            print("OMG! The Brain has no memories (original_CV is empty)!")

        print("Generating identity, Please wait")
        summary_piece = self._sanitize_fragment(
            self.brain.identity(
                state["job_description"], state["original_CV"], rules_path
            )
        )
        print(
            f"  Summary: {len(summary_piece)} chars {'OK' if summary_piece else 'EMPTY!'}"
        )

        print("Generating toolkit, Almost there - hangOn!")
        skills_piece = self._sanitize_fragment(
            self.brain.toolkit(
                state["job_description"],
                state["original_CV"],
                state["original_CV"],
                rules_path,
            )
        )
        print(
            f"  Skills: {len(skills_piece)} chars {'OK' if skills_piece else 'EMPTY!'}"
        )

        print("Generating journey, Completed, hangOn!")
        exp_piece = self._sanitize_fragment(
            self.brain.journey(
                state["job_description"], state["original_CV"], rules_path
            )
        )
        print(f"  Experience: {len(exp_piece)} chars {'OK' if exp_piece else 'EMPTY!'}")

        print("Picking projects...")
        projects_piece = self._sanitize_fragment(
            self.brain.pick_projects(state["job_description"], state["original_CV"])
        )
        print(
            f"  Projects: {len(projects_piece)} chars {'OK' if projects_piece else 'EMPTY!'}"
        )

        print("Picking certifications...")
        certs_piece = self._sanitize_fragment(
            self.brain.pick_certs(state["job_description"], state["original_CV"])
        )
        print(f"  Certs: {len(certs_piece)} chars {'OK' if certs_piece else 'EMPTY!'}")

        # Check tags
        template = state["laTex_CV_template"]
        for tag in [
            "[SUMMARY]",
            "[SKILLS]",
            "[EXPERIENCE]",
            "[PROJECTS]",
            "[CERTIFICATIONS]",
        ]:
            if tag not in template:
                print(f"WARNING: {tag} not found in template!")

        # Assemble
        final_latex = template.replace("[SUMMARY]", summary_piece)
        final_latex = final_latex.replace("[SKILLS]", skills_piece)
        final_latex = final_latex.replace("[EXPERIENCE]", exp_piece)
        final_latex = final_latex.replace("[PROJECTS]", projects_piece)
        final_latex = final_latex.replace("[CERTIFICATIONS]", certs_piece)

        return {**state, "final_CV": final_latex}

    def orchestrate_the_spirit(self):
        builder = StateGraph(CareerState)
        builder.add_node("fetch", self.recall_memories)
        builder.add_node("optimizing", self.shaping_thePersona)
        builder.add_edge(START, "fetch")
        builder.add_edge("fetch", "optimizing")
        builder.add_edge("optimizing", END)
        return builder.compile()
