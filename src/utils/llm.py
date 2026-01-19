import os

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub

# Load environment variables
load_dotenv()


def get_llm():
    """
    Initialize and return the LLM model.

    Returns:
        HuggingFaceHub: Initialized Hugging Face model
    """
    return HuggingFaceHub(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
        temperature=0.7,
        max_new_tokens=1024,
    )
