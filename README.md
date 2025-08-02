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


