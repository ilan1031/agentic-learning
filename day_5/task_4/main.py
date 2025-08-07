import streamlit as st
from src.loader import load_pdf_text
from src.vector_store import store_docs, retrieve_similar_chunks
from src.agent import generate_summary
from src.session_handler import get_session_token
import os

st.set_page_config(page_title="LitReview Compiler", layout="wide")
st.title("📚 LangChain LitReview Compiler")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
session_token = get_session_token()

if uploaded_file:
    pdf_path = os.path.join("data", uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("PDF uploaded and saved.")

    with st.spinner("Processing PDF..."):
        docs = load_pdf_text(pdf_path)
        store_docs(docs)
        chunks = retrieve_similar_chunks(docs)
        summary = generate_summary(chunks, session_token)

    output_path = os.path.join("output", "final_summary.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    st.markdown("### ✅ Summary:")
    st.markdown(summary)
    st.download_button("Download Summary", summary, file_name="final_summary.md")
