# agentic-learning

**AI\_legal\_case\_summary\_tool.ipynb**. It explains the purpose, setup, usage, and technical details of your AI tool for summarizing legal case files:

---

```markdown
# 🧠 AI Legal Case Summary Tool

This project is a Jupyter Notebook–based AI tool that reads legal case documents and generates intelligent summaries using Gemini Pro via LangChain. It enables lawyers, law students, and legal professionals to automate the tedious process of reading and distilling long legal case files into digestible summaries.

---

## 🚀 Features

- 📄 Accepts uploaded legal documents (PDF, DOCX, TXT)
- 🔍 Extracts and parses text automatically
- ✨ Summarizes legal cases using Gemini-Pro LLM
- 🛠️ Built with LangChain for modularity
- 🧪 Interactive Streamlit-based interface
- 🧠 Optionally supports multi-part summarization (context-aware)

---

## 📂 Project Structure

```

AI\_legal\_case\_summary\_tool.ipynb      # Main Jupyter Notebook with code

```

If extended to production:
```

/app/
├── main.py                         # Streamlit or Flask interface
├── summarizer.py                  # LLM call + text handling
└── utils.py                       # File parsers and helper functions
requirements.txt                     # Python dependencies
README.md                            # Project documentation

````

---

## 🧰 Technologies Used

- [LangChain](https://www.langchain.com/)
- [Google Gemini Pro API](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/) *(optional UI)*
- Python standard libraries (`os`, `io`, `PyPDF2`, `docx`, etc.)

---

## 📦 Installation

```bash
# Clone the repo (if applicable)
git clone https://github.com/yourusername/legal-case-summarizer.git
cd legal-case-summarizer

# Create a virtual environment
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
````

---

## 🔑 Environment Setup

Create a `.env` file in the root directory with:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Or configure it directly inside the notebook using:

```python
import os
os.environ["GEMINI_API_KEY"] = "your_gemini_api_key"
```

---

## 🧪 How to Use

1. Launch Jupyter:

   ```bash
   jupyter notebook
   ```
2. Open `AI_legal_case_summary_tool.ipynb`
3. Upload a legal document.
4. Run all cells.
5. Get a structured summary output from the Gemini Pro model.

---

## ✅ Output Example

```
Case Title: ABC vs XYZ
Date: Jan 2021
Summary: The plaintiff alleged breach of contract due to delivery failure...
Legal Issues:
  - Was there a valid contract?
  - Did the defendant fulfill obligations?
Decision: Court ruled in favor of the plaintiff.
```

---

## 📈 Future Enhancements

* Export summary to PDF/Word
* Chain of Thought (CoT) reasoning for judgment prediction
* Multi-document cross-referencing
* Support for scanned PDFs using OCR

---

## 📄 License

MIT License. See `LICENSE` for details.

---

## 👨‍⚖️ Author

Developed by \ilanthalir S
For legal research, automation, and summarization tasks.

---

