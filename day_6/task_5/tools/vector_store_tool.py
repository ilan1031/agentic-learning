import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict


class VectorSearchTool:
    def __init__(self):
        self.client = chromadb.Client()
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection("agent_memory")

    def save(self, ideas: List[Dict]):
        # ideas: [{"id": str, "text": str, "meta": {..}}]
        if not ideas:
            return "No ideas to save."
        ids = [i["id"] for i in ideas]
        docs = [i["text"] for i in ideas]
        metas = [i.get("meta", {}) for i in ideas]
        self.collection.add(ids=ids, documents=docs, metadatas=metas)
        return f"Saved {len(ids)} ideas to vector store."

    def run(self, query: str):
        results = self.collection.query(query_texts=[query], n_results=5)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0] or results.get("embeddings", [[]])[0]
        if not docs:
            return "No match in vector memory."

        # Convert distances to a simple relevance (if distances exist)
        md_lines = []
        for idx, doc in enumerate(docs):
            meta = metas[idx] if idx < len(metas) else {}
            # Chroma returns smaller distance = closer; map to 0..100
            dist = distances[idx] if idx < len(distances) else None
            if dist is not None:
                rel = max(0, int(100 * (1 - min(1.0, float(dist)))))
            else:
                rel = 0
            tag = meta.get("niche") or meta.get("source") or "memory"
            md_lines.append(f"- {doc} — {rel}% relevance ({tag})")
        return "\n".join(md_lines)
