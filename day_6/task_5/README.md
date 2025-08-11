# 📚 AI Assistant with LangChain (Day 6, Task 5)

This project builds a LangChain AI agent for content idea generation with:

- 🔍 Web search (SerpAPI)
- 🎯 Niche filter tool (scores ideas by relevance)
- 💾 Vector store (Chroma) to save and retrieve ideas
- 📄 Markdown export with relevance scores
- 🌐 UI via Streamlit

## Expected Deliverables
- Content ideas in markdown format with relevance scores
- Query responses with implementation details

## Run Instructions
```bash
pip install -r requirements.txt
# Ensure .env contains SERPAPI_API_KEY and GEMINI_API_KEY or GOOGLE_API_KEY
streamlit run main.py
```

## Environment
Create a `.env` file with:
```
GEMINI_API_KEY=your_key_here  # or GOOGLE_API_KEY
SERPAPI_API_KEY=your_serpapi_key
```

---
🛠 Built for LangChain agent development and evaluation under Day 5, Task 4.

---

Let me know if you'd like Docker support, HuggingFace integration, or Gemini Pro support.
