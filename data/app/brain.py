import time

from google import genai


class nerves:
    def __init__(self, model_name="models/gemma-3-4b-it"):
        self.api_key = "AIzaSyDGozwcOMI0b-muREZpMC08WbE11sbL5BA"
        self.client = genai.Client(api_key=self.api_key)
        self.model = model_name

    def think(self, prompt, retries=5):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )  # asking gemini the model for text using prompt
                if (
                    not response or not response.text
                ):  # if the api returned nothing then bail out , if there is no reply it return empty string so the rest of teh code doesnt try to work with missing data ;)
                    return ""

                text = response.text.strip()
                # remove code that models often add which leaves with just usual text
                text = text.replace("```latex", "").replace("```", "").strip()

                prefixes = ["Here is", "Here's", "Sure, here", "Certainly"]
                for prefix in prefixes:
                    if text.startswith(prefix):
                        lines = text.split("\n")
                        text = "\n".join(lines[1:]).strip()
                        break
                return text

            except Exception as e:  # since i reach a rate-limit wait or retry
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    nap_time = 20 + (attempt * 10)
                    time.sleep(nap_time)
                else:
                    return ""
        return ""

    def identity(self, job_desc, history, rules_path):
        """Generates summary based strictly on history and JD."""
        prompt = f"""
        [HISTORY] {history}
        [TARGET JD] {job_desc}
        TASK: Write a 2-line Professional Summary.
        RULES:
        1. Use ONLY facts from history (Degrees, SDET exp, Python/Azure).
        2. DO NOT invent information.
        3. Match the JD tone.
        4. Return ONLY plain text.
        """
        return self.think(prompt)

    def toolkit(self, job_desc, skills_data, experience_data, rules_path):
        prompt = f"""
        [SKILLS] {skills_data}
        [JD] {job_desc}

        TASK:
        Pick 3-5 skill categories from SKILLS and return one LaTeX macro invocation per line.
        Each line must match this literal format (no extra text):

        \\resumeSectionType{{Category}}{{:}}{{Skill1, Skill2, Skill3}}

        If a skill name contains an ampersand (e.g., "Power BI & Excel"), the ampersand
        should be escaped inside the skill as '\\&'. Do not put '\\&' between macro arguments.
        """
        return self.think(prompt)

    def journey(self, job_desc, history, rules_path=None):
        prompt = f"""
        [HISTORY] {history}
        [JD] {job_desc}

        TASK: Refine the bullet points for the roles in HISTORY to match the JD.

        STRICT RULES:
        1. OUTPUT ONLY the LaTeX code starting with \\resumeQuadHeading.
        2. DO NOT include intros like "Okay, here's..." or labels like "[ACTUAL HISTORY]".
        3. You MUST provide exactly 5 bullet points for every job.
        4. Use \\& for ampersands.
        """
        return self.think(prompt)
