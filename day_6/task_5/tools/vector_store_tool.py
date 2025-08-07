import chromadb
from chromadb.utils import embedding_functions

class VectorSearchTool:
    def __init__(self):
        self.client = chromadb.Client()
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection("agent_memory")

    def run(self, query):
        results = self.collection.query(query_texts=[query], n_results=1)
        if results["documents"]:
            return results["documents"][0][0]
        return "No match in vector memory."
