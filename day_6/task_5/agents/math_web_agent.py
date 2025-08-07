from langchain.tools import Tool
from tools.web_search_tool import web_search
from tools.custom_calculator import custom_addition
import os
import requests

class GeminiFlaskLLM:
    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url or "http://localhost:5000/generate"
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def __call__(self, prompt, **kwargs):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"prompt": prompt}
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json().get("text", "")
        return f"Error: {response.text}"

llm = GeminiFlaskLLM()

tools = [
    Tool.from_function(web_search),
    Tool.from_function(custom_addition)
]

def run_agent(user_query: str):
    # Directly call GeminiFlaskLLM for now, bypassing LangChain agent logic
    return llm(user_query)
