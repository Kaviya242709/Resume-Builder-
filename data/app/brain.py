import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class nerves:
    def __init__(self, model_name="gemini-flash-lite-latest"):
        self.api_key = os.getenv("AI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model_name

    def think(self, prompt, retries=5):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                if not response or not response.text:
                    return ""
                text = response.text.strip()
                text = text.replace("```latex", "").replace("```", "").strip()
                prefixes = ["Here is", "Here's", "Sure, here", "Certainly"]
                for prefix in prefixes:
                    if text.startswith(prefix):
                        lines = text.split("\n")
                        text = "\n".join(lines[1:]).strip()
                        break
                return text
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    nap_time = 20 + (attempt * 10)
                    print(
                        f"Rate limit hit, waiting {nap_time}s (attempt {attempt + 1}/5)..."
                    )
                    time.sleep(nap_time)
                else:
                    print(f"Error: {e}")
                    return ""
        return ""

    def identity(self, job_desc, history, rules_path):
        prompt = f"""
[HISTORY] {history}
[TARGET JD] {job_desc}

TASK: Rewrite the Professional Summary to align with the JD tone and keywords.
STRICT RULES:
1. Use ONLY facts already present in [HISTORY]. Do NOT add anything new.
2. Do NOT invent degrees, titles, years of experience, or skills not in [HISTORY].
3. Only rephrase/reorder existing facts to mirror JD language.
4. Max 2 lines. Return ONLY plain text. No labels, no bullets.
"""
        return self.think(prompt)

    def toolkit(self, job_desc, skills_data, experience_data, rules_path):
        prompt = f"""
[SKILLS_SOURCE] {skills_data}
[JD] {job_desc}

TASK: Select and reorder skills from [SKILLS_SOURCE] that best match the JD.
STRICT RULES:
1. ONLY use skills EXPLICITLY listed in [SKILLS_SOURCE].
2. Do NOT invent, rename, or add any skill not in the source.
3. Do NOT include job titles, company names, project names, or dates.
4. Return 3-5 categories, one LaTeX macro per line in this EXACT format:
\\resumeSectionType{{Category}}{{:}}{{Skill1, Skill2, Skill3}}
5. Escape ampersands as \\& inside skill names only.
6. Return ONLY the macro lines. No explanation, no intro text.
"""
        return self.think(prompt)

    def journey(self, job_desc, history, rules_path=None):
        prompt = f"""
[HISTORY] {history}
[JD] {job_desc}

TASK: Rewrite work experience bullets to reflect JD keywords using ONLY facts in [HISTORY].
STRICT RULES:
1. Do NOT change job titles, company names, dates, or locations.
2. Do NOT invent tools, technologies, metrics, or responsibilities.
3. Only rephrase existing bullets using JD terminology where it fits naturally.
4. Include ALL roles from [HISTORY]. Do NOT drop any role.
5. Exactly 3 bullet points per role.
6. Output ONLY LaTeX using this EXACT format for every role:

\\entryheader{{Job Title}}{{Start -- End}}
\\entrysubtitle{{Company, Location}}
\\begin{{cvbullets}}
\\item Bullet one.
\\item Bullet two.
\\item Bullet three.
\\end{{cvbullets}}

7. Use \\& for ampersands. No intro text. Output ONLY the LaTeX blocks.
"""
        return self.think(prompt)

    def pick_projects(self, job_desc, history):
        prompt = f"""
[HISTORY] {history}
[JD] {job_desc}

TASK: Pick 3 or 4 projects from the [PROJECTS] section in [HISTORY] most relevant to the [JD].
STRICT RULES:
1. ONLY use projects explicitly listed in [HISTORY] under [PROJECTS].
2. Do NOT invent or modify any project content.
3. Output each project in this EXACT LaTeX format:

\\entryheader{{Project Name}}{{Year}}
\\entrysubtitle{{Tech Stack}}
\\begin{{cvbullets}}
\\item Bullet one exactly as in history.
\\item Bullet two exactly as in history.
\\end{{cvbullets}}

4. Use \\& for ampersands. No intro text. Output ONLY the LaTeX blocks.
"""
        return self.think(prompt)

    def pick_certs(self, job_desc, history):
        prompt = f"""
[HISTORY] {history}
[JD] {job_desc}

TASK: Pick 2-3 certifications from the [CERTIFICATIONS] section in [HISTORY] most relevant to [JD].
STRICT RULES:
1. ONLY pick from certifications explicitly listed in [HISTORY] under [CERTIFICATIONS].
2. Do NOT invent any certification.
3. Return ONLY LaTeX lines in this EXACT format:
\\listentry{{Cert Name}}{{Issuer}}{{Year}}
4. No intro text, no explanation.
"""
        return self.think(prompt)
