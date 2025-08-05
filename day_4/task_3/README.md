# Documentation for day_4_react_agent

This folder contains the ReAct agent for book summary generation.

- See `app.py` for the Streamlit app.
- See `src/` for agent and tools code.
- See `requirements.txt` for dependencies.

---

# 📚 Book Summary Generator (ReAct Agent)

### 🤖 What is this?

This is an **AI-powered book summary generator** that reads and understands books for you — like a smart assistant! You give it a **book title**, and it will:

1. **Search the internet** (on Wikipedia, SparkNotes, Goodreads)
2. **Read and collect summaries**
3. **Ask intelligent questions** about the book’s plot, themes, and characters
4. **Find answers** from what it read
5. **Write a full book report** in a nice clean format, with sections like:

   * Plot Summary
   * Themes
   * Character Analysis
   * Key Questions and Answers

At the end, you get a **PDF report** you can read or share.

---

### 🎯 Why was this built?

* For students and readers who want a **quick understanding** of any book
* To help with **literary analysis**
* As a learning project to show how AI can **reason and act** (ReAct pattern)

---

### 💡 What makes this tool smart?

* It **generates questions** the way a literature teacher might.
* It **searches real websites** (not just AI hallucination).
* It uses Google Gemini (an advanced AI) to **understand and summarize** content.
* It even **tracks how much it’s reading** to stay within limits and store your session data.

---

### 🖥️ How do I use it?

Just enter the **title of any book** into the app (via a simple interface). The AI will do all the work and give you a complete report.

---

### 🔒 Does it store anything?

Yes, for each session, it stores:

* The total token usage (how much the AI read)
* A copy of the summary it scraped from online
* Your final report

All this is stored securely in a database (MongoDB), just for tracking and learning.

---

### ⏱️ How fast is it?

It usually finishes within **1 minute**. If a website fails, it will try again (up to 3 times).

---

### 📄 Example Output Format

```
# Book Summary: The Alchemist

## Plot Summary
A young shepherd named Santiago dreams of finding treasure...

## Themes
- Personal Legend
- Faith and Destiny
- Self-Discovery

## Character Analysis
- Santiago: Dreamer, explorer, grows through journey
- The Alchemist: Mentor figure...

## Key Questions and Answers
Q: What is the main lesson of the book?  
A: That one must follow their Personal Legend to find true happiness...

...
```

---

### 🤓 Built Using:

* **Python** with a custom-built AI agent
* **ReAct pattern** (Reason + Act)
* **Google Gemini 1.5 Flash** for intelligence
* **BeautifulSoup + Requests** for smart web reading
* **MongoDB** for secure session storage
* **Streamlit UI** for a simple user interface

---


