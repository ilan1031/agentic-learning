import streamlit as st
from src.agent.react_loop import react_agent
from fpdf import FPDF

st.title("\ud83d\udcda Book Summary Generator (ReAct Agent)")
book = st.text_input("Enter Book Title")

if st.button("Generate Summary") and book:
    sid, qa_pairs = react_agent(book)
    report_md = f"# Book Summary: {book}\n\n## Key Questions and Answers\n"
    for q, a in qa_pairs:
        report_md += f"- Q: {q}\n  A: {a}\n"

    st.markdown(report_md)
    with open("summary.pdf", "wb") as f:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in report_md.split('\n'):
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(f)
    st.download_button("Download PDF", data=open("summary.pdf", "rb"), file_name="summary.pdf")
