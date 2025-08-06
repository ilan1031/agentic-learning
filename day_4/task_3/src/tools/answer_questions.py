from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

def answer_questions(text_chunk, question):
    prompt = PromptTemplate.from_template("""
    Context:
    {text_chunk}

    Question:
    {question}

    Provide a clear and concise answer.
    """)
    chain = prompt | ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=os.getenv("GEMINI_API_KEY"))
    return chain.invoke({"text_chunk": text_chunk, "question": question})
