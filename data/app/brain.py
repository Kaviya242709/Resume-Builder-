# now talking with ollama -> using requests library to understand the api's work process

import json

import requests
from urllib3 import request


class nerves:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def think(self, prompt):
        payload = {"model": self.model, "prompt": prompt, "stream": False}

    try:
        response = requests.post(
            self.url, json=payload
        )  # payload - python method which has three major functions : JSON, DICT, Schema for transmitting data like user infor, crendtials.

        response.raise_for_status()
        return response.json().get("response", "Oops it is blank!")

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

    def __forge_latex(self, resume_content, job_description, template_for_laTex):
        """Function to forge the LaTex code"""
        full_prompt = f"""
        You will be the writer.
        Take this resume: {resume_content}
        Optimize it for the job description: {job_description}
        Use the following template exactly: {template_for_laTex}

        Return only the latex code which the user want with talking;)
        """
        return self.think(full_prompt)
