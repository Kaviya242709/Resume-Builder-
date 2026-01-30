from data.app.skeleton import Skeleton


def main():
    skeleton = Skeleton()

    # Read your LaTeX resume file (change the path to your actual .tex file)
    with open("laTex_resume.tex", "r") as f:
        resume_content = f.read()

    # Store it in ChromaDB
    skeleton.remember(resume_content)
    print("Resume uploaded successfully!")


if __name__ == "__main__":
    main()
