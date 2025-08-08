# 📚 AI Assistant with LangChain (Day 5, Task 4)

This project builds a full-featured LangChain AI agent integrated with:

- 🔍 Web search (SerpAPI)
- ➕ Custom calculator tool
- 💾 Session history save/load
- 📄 Markdown export
- 🌐 UI via Streamlit

## 💡 Features
- Modular agent using LangChain tools
- Tools in `/tools/`, loaded dynamically
- Saved sessions in `/sessions/`
- Markdown logs in `/output/`

## 🧠 Agent Criteria
| Criteria                     | Description                                                                 | Marks |
|-----------------------------|-----------------------------------------------------------------------------|-------|
| Git Structure               | Modular, project-ready layout                                               | 2     |
| LangChain Framework         | Correct and effective LangChain usage                                      | 1     |
| Web Search Tool             | Integrated and working web search tool                                     | 1     |
| Custom Tool                 | Built-in custom calculator                                                 | 1     |
| Vector Store                | N/A (not used here)                                                        | 0     |
| Agent Workflow              | Complete agent interaction with tools and Streamlit                        | 3     |
| Output Accuracy             | Exported markdown and session history retained accurately                  | 1     |
| **Total**                   |                                                                             | **9** |

## � Run Instructions
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## � Environment
Create a `.env` file with:
```
GEMINI_API_KEY=your_key_here
SERPAPI_API_KEY=your_serpapi_key
```

---
🛠 Built for LangChain agent development and evaluation under Day 5, Task 4.

---

Let me know if you'd like Docker support, HuggingFace integration, or Gemini Pro support.
