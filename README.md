# agentic-learning

# 📅 Day 1 / Task 1 — AI Contextual Legal Case Summary Tool

## 🧠 Objective
Build an AI-powered tool that summarizes legal cases in a structured, context-aware format for use by legal professionals and IP consultants.

---

## ✅ What This Tool Does
- Accepts **case facts**, **ruling**, and a **specific context**
- Uses a custom Gemini-powered prompt:
  - Persona: 42-year-old IP consultant mentoring a junior
- Returns a **3-part legal summary**:
  1. **Background** – Facts and applicable laws
  2. **Ruling** – Decision and rationale with legal references
  3. **Relevance to Context** – How the ruling applies to the user’s case

---

## 🛠️ Tech Stack
- 🧠 **Google Gemini Pro (gemini-1.5-flash)** via `google-generativeai`
- 🔗 Prompt engineering + guardrails
- 🧪 Validated using token count (300–480 tokens) and format checks
- 💡 Re-generates output if format is invalid (up to 3 retries)

---

## 🧩 How It Works
1. Define prompt template with legal sections and persona tone.
2. Pass input into Gemini model with:
   - Temperature = 0.2
   - Max tokens = 400
3. Apply guardrails to ensure format and token limits.
4. Print result or retry if validation fails.

---

## ⚙️ Setup Instructions

```bash
pip install -U google-generativeai tiktoken
```

---
# 📁 Day 2 - Task 2: HR Policy AI Chatbot (PDF-based)

This task implements an AI-powered HR chatbot using **Google Gemini 1.5 Flash**, capable of answering queries based only on uploaded **PDF HR documents**. It uses **FAISS** for vector retrieval and a **Streamlit UI**.

---

## ✅ Features

- Upload HR policy documents (PDF only)
- Extracts and chunks content
- Embeds using `all-MiniLM-L6-v2`
- Stores vectors in FAISS
- Retrieves top-k relevant sections
- Gemini 1.5 answers with context
- Displays source for every answer

---

## 🔧 How to Run

1. Install dependencies  
   `pip install -r requirements.txt`

2. Add your Gemini key in `.env`  
   `GOOGLE_API_KEY=your_api_key`

3. Launch app  
   `streamlit run app.py`

---

## 🧪 Test Questions

- What is the maternity leave policy?
- How many sick leaves are allowed?
- What is the notice period?

---



```
---

## 📘 Day 4 / Task 3: ReAct Agent – Book Summary Generator

### 🧠 What It Does

This AI agent takes a **book title** and creates a structured summary by:

* Generating **smart questions** about the plot, themes, and characters
* **Scraping free online sources** (Wikipedia, SparkNotes, Goodreads)
* Using **Gemini 1.5 Flash** to process the content
* Writing a final **Markdown report** with key insights

---

### 🔧 Tech Stack

* **Gemini 1.5 Flash** (via API key)
* **Python** with ReAct agent pattern
* **BeautifulSoup** for web scraping
* **MongoDB Atlas** for session/token storage
* **.env** file for API keys and DB URI

---

### 📦 Output

* A clean, structured **Markdown summary**
* Includes: Plot, Themes, Character Analysis, Q\&A
* All session data and token count saved to MongoDB

---

### 📂 Folder: `day_4/task_3/src/`

Add all Python source files and configs inside this folder.
Secrets like your Gemini API key and MongoDB URI go in `.env`.

---
```


---

## 📘 Day 5 – Task 4: LangChain Literature Review Compiler

A smart AI agent that **automatically summarizes academic research papers** using PDF input. Designed for students, researchers, and consultants to **compile literature reviews** with minimal effort.

---

### 🔍 What It Does

* 📂 Upload one or more PDF research papers.
* 🧠 Extracts key points using **Google Gemini** + **LangChain**.
* 🧾 Produces a **clean summary** with:

  * Background
  * Methods
  * Key Findings
  * Citations
* 📝 Saves everything in `output/final_summary.md`.

---

### 🛠️ Tech Stack

* **LangChain** + **ReAct** Agent pattern
* **ChromaDB** (for local vector memory)
* **Google Gemini Pro API**
* **Streamlit** UI (`main.py`)
* `.env` for secret key config
* Fully local processing (no cloud storage)

---

### 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Gemini API key in .env
echo "GEMINI_API_KEY=your_key" > .env

# 3. Launch the UI
streamlit run main.py
```

---

### 🙋 Who Is This For?

* Students doing thesis or review writing
* Researchers handling multiple papers
* Non-tech users who want AI help with studies



---

# 📄 Day 6 – Task 5: AI Session Agent

## 🧠 What This Agent Is

An AI-powered session-based assistant that helps you brainstorm, process, and organize ideas interactively. It keeps track of your conversation history, generates structured markdown outputs, and saves each session for later use.

## 🎯 What It’s Used For

* Capturing and organizing brainstorming sessions.
* Turning free-flowing chats into clean, well-structured markdown notes.
* Keeping context across multiple prompts without losing important details.

## ⚙️ How It Works

1. **Session Management** – `session_handler.py` creates and tracks session history.
2. **Input Processing** – The agent receives your prompts and enriches them with AI-generated insights.
3. **Markdown Output** – `markdown_writer.py` formats results into readable markdown.
4. **Data Storage** – Sessions are saved in `/sessions/` as JSON; markdown exports go to `/output/`.
5. **Utility Tools** – `utils.py` handles token counting, cleaning text, and performance checks.

---



