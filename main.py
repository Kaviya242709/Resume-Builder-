from src.orchestrator.supervisor import kickoff


def main():
    """Main function to run CV builder"""

    print("Stay closer...\n")

    # Example CV details
    cv_details = """
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

    try:
        print("Hold on as this may take upto 30-60 seconds...\n")
        result = kickoff(cv_details)

        print("=" * 80)
        print("CV GENERATED SUCCESSFULLY!")
        print("=" * 80 + "\n")
        print(result)
        print("\n" + "=" * 80)

    except Exception as e:
        print(f"❌ Error generating CV: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
