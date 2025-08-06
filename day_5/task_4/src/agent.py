from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from tools.prompts import SUMMARY_PROMPT
import os
from dotenv import load_dotenv
load_dotenv()

# Check if API key is available
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_api_key_here":
    raise ValueError(
        "GEMINI_API_KEY not found or not set properly. "
        "Please set your Gemini API key in the .env file. "
        "Get your API key from: https://makersuite.google.com/app/apikey"
    )

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2, google_api_key=api_key)
prompt = PromptTemplate.from_template(SUMMARY_PROMPT)

def generate_summary(text, session_id):
    formatted = prompt.format(context=text, session=session_id)
    return llm.predict(formatted)
