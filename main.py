import os
import sys
import traceback

# Keep local package imports working when running from the repo root
sys.path.append("./data")

from data.app.brain import nerves
from data.app.skeleton import Skeleton
from data.app.workflow import CareerState, Workflow


def main():
    # Initialize core pieces
    skeleton = Skeleton()
    brain = nerves()
    app_workflow = Workflow(brain, skeleton)
    resume_builder = app_workflow.orchestrate_the_spirit()

    # loading all data into chroma db - vdb
    resume_path = "master_resume.txt"
    if not os.path.exists(resume_path):
        print("ERROR: master_resume.txt not found!")
        return

    with open(resume_path, "r", encoding="utf-8") as f:
        resume_content = f.read()

    skeleton.remember(resume_content)
    print("Uploaded your REAL resume into brain, Good go!")

    # finding the template to drop all your datas
    tex_files = [f for f in os.listdir(".") if f.endswith(".tex")]
    if not tex_files:
        print("Oops! No, File found with .tex extension!")
        return

    # Use the first .tex file found as the blueprint,
    template_path = tex_files[0]
    print(
        f"Using template: {template_path}"
    )  # should show your template file where you want in what structure

    with open(template_path, "r", encoding="utf-8") as file:
        master_template = file.read()

    # get the jd first
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

    # initialize the initial state - Graph
    initial_state: CareerState = {
        "job_description": job_desc,
        "original_CV": resume_content,
        "laTex_CV_template": master_template,
        "final_CV": "",
    }

    # if it fails in your workflow
    try:
        final_output = resume_builder.invoke(initial_state)
    except Exception:
        print("Error while running the workflow, Try again later!\n")
        traceback.print_exc()
        return

    # save the op in a diff file with a unique name
    output_path = "Final_resume.tex"
    final_text = ""

    if isinstance(final_output, dict):
        final_text = final_output.get("final_CV", "") or ""
    else:
        final_text = str(final_output or "")

    # Write the assembled LaTeX template as-is, do not run global escaping here.
    # Any escaping should be applied only to the AI-generated fragments before they
    # were inserted into the template (we do that in workflow.py).
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    if final_text:
        print(f" Okay cool you made it '{output_path}'")
    else:
        print("Workflow finished but no text was generated.")


if __name__ == "__main__":
    main()
