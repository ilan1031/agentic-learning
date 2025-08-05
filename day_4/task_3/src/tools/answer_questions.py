from langchain_core.prompts import PromptTemplate

def answer_questions(text_chunk, question):
    prompt = PromptTemplate.from_template("""
    Context:
    {text_chunk}

    Question:
    {question}

    Provide a clear and concise answer.
    """)
    chain = prompt | ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    return chain.invoke({"text_chunk": text_chunk, "question": question})
