# LangChain-LitReview-Compiler

AI-powered assistant to extract literature summaries from academic papers (PDFs). Built using:

- 🔗 LangChain
- 🧠 Google Gemini 1.5
- 📦 ChromaDB (for vector storage)
- 🌐 Streamlit (for UI)

## How to Use
1. Put your PDF in the `data/` folder.
2. Run the app:
```bash
streamlit run main.py
```
3. Get your literature summary in the `output/final_summary.md`.

---

## Developer Info
- Input: Academic research PDFs
- Output: Clean, markdown-based literature summaries
- Uses LangChain agent with prompt templates + embeddings
- Stores vectors in ChromaDB for reuse and efficiency
