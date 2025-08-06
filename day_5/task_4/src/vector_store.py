import chromadb
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="lit_papers")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def store_docs(text):
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = embedder.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def retrieve_similar_chunks(text):
    query_emb = embedder.encode([text]).tolist()[0]
    results = collection.query(query_embeddings=[query_emb], n_results=5)
    return "\n".join(results["documents"][0])
