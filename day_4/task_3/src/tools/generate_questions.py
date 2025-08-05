from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

def generate_questions(book_title):
    prompt = PromptTemplate.from_template("""
        You are a literature expert. Generate 5 insightful questions to understand the book: {book_title}
        Include questions on plot, characters, and themes.
    """)
    chain = prompt | llm
    return chain.invoke({"book_title": book_title})
