from langchain_community.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from tools.prompts import SUMMARY_PROMPT
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2, google_api_key=os.getenv("GEMINI_API_KEY"))
prompt = PromptTemplate.from_template(SUMMARY_PROMPT)

def generate_summary(text, session_id):
    formatted = prompt.format(context=text, session=session_id)
    return llm.predict(formatted)
