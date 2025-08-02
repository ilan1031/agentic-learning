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
