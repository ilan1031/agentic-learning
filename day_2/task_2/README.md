# 🤖 HR Policy AI Chatbot (RAG-Powered with Gemini 1.5 Flash)

A fully functional AI-powered HR assistant that answers employee questions by retrieving relevant content from HR policy documents (PDFs). Uses **Google Gemini 1.5 Flash**, **FAISS vector store**, and **Streamlit** for a beautiful interactive UI.

---

## 📌 Features

✅ Upload HR policy documents (PDF only)  
✅ Automatically extract and semantically chunk text  
✅ Embed and index chunks using SentenceTransformers  
✅ Retrieve top-k relevant chunks using FAISS  
✅ Prompt Gemini 1.5 Flash with retrieved context (RAG)  
✅ Stream answers with source citations  
✅ User-friendly Streamlit chat interface  
✅ Modular and clean architecture

---

## 🚀 Demo Use Case

> ❓ *"What is the maternity leave policy?"*  
> ✅ Answered using relevant paragraphs from uploaded PDFs  
> 🧾 Citations: `[Source: Employee_Handbook.pdf - Section 3]`

---

## 🧠 Tech Stack

| Component      | Tech Used                    |
|----------------|------------------------------|
| LLM            | Google Gemini 1.5 Flash      |
| Embedding      | all-MiniLM-L6-v2 (HF)        |
| Vector Store   | FAISS                        |
| PDF Parsing    | PyMuPDF                      |
| Framework      | Streamlit                    |
| Prompting      | LangChain Prompt Templates   |

---

## 📁 Project Structure

hr-policy-chatbot/
├── app.py # Main Streamlit chat app
├── .env # Google API key
├── requirements.txt # Python dependencies
└── utils/
├── loader.py # PDF file loader
├── processor.py # Chunking and preprocessing
└── rag.py # Embedding, retrieval, and Gemini response


---

## 📄 Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/hr-policy-chatbot.git
cd hr-policy-chatbot

2. Create Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt
4. Add API Key
Create a .env file:

env

GOOGLE_API_KEY=your_gemini_api_key
✅ Running the App

streamlit run app.py
Then open: http://localhost:8501

📌 Usage Flow
Upload PDF HR policy document via sidebar

System:

Extracts and chunks the document

Embeds chunks and builds FAISS index

Ask your HR policy questions in the chat

Gemini answers using only the retrieved policy content

See explanations and sources for transparency

🔐 LLM Safety Instructions
The prompt instructs Gemini to:

Use only retrieved policy content

Refuse answers if content is missing

Cite file and section for every answer

📦 Sample Prompt Template

You are a professional HR consultant. Use ONLY the provided HR policy content to answer.

{context}

Question: {question}

Instructions:
- Answer in 2-3 short paragraphs.
- Do not include content not found in the context.
- Cite source using [Source: filename - Section #].
🧪 Example Questions
What is the leave encashment rule?

How do I report workplace harassment?

What are the rules for casual leave?

🔧 Future Enhancements (Suggestions)
Add DOCX and XLSX support

Enable multi-PDF memory and search

Track question logs (MongoDB or SQLite)

Deploy to HuggingFace Spaces or Streamlit Cloud

Add user authentication for HR-only access

🤝 License
MIT License

🧑‍💼 Built For
HR teams automating policy queries

Employees understanding benefits and rules

Compliance and legal documentation assistance

📬 Contact
Made with ❤️ by ilan
