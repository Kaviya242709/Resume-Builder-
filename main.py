import os
import sys
import traceback

sys.path.append("./data")
from data.app.brain import nerves

from data.app.skeleton import Skeleton
from data.app.workflow import CareerState, Workflow
from keyword_matcher import run_keyword_match  # ← ADD 1: import


def main():
    skeleton = Skeleton()
    brain = nerves()
    app_workflow = Workflow(brain, skeleton)
    resume_builder = app_workflow.orchestrate_the_spirit()

    resume_path = "master_resume.txt"
    if not os.path.exists(resume_path):
        print("ERROR: master_resume.txt not found!")
        return
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_content = f.read()
    skeleton.remember(resume_content)
    print("Uploaded your REAL resume into brain, Good go!")

    tex_files = [f for f in os.listdir(".") if f.endswith(".tex")]
    if not tex_files:
        print("Oops! No, File found with .tex extension!")
        return

    template_path = tex_files[0]
    print(f"Using template: {template_path}")
    with open(template_path, "r", encoding="utf-8") as file:
        master_template = file.read()

    print("Paste the Job Description below :")
    jd_lines = []
    try:
        while True:
            line = input()
            jd_lines.append(line)
    except EOFError:
        pass
    job_desc = "\n".join(jd_lines)
    if not job_desc.strip():
        print("No job description provided, Sorry!!")
        return

    initial_state: CareerState = {
        "job_description": job_desc,
        "original_CV": resume_content,
        "laTex_CV_template": master_template,
        "final_CV": "",
    }

    try:
        final_output = resume_builder.invoke(initial_state)
    except Exception:
        print("Error while running the workflow, Try again later!\n")
        traceback.print_exc()
        return

    output_path = "Final_resume.tex"
    final_text = ""
    if isinstance(final_output, dict):
        final_text = final_output.get("final_CV", "") or ""
    else:
        final_text = str(final_output or "")

    # ← ADD 2: keyword match + learning resources BEFORE saving
    final_text = run_keyword_match(job_desc, resume_content, final_text, brain)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    if final_text:
        print(f" Okay cool you made it '{output_path}'")
    else:
        print("Workflow finished but no text was generated.")


if __name__ == "__main__":
    main()
