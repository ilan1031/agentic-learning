import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class PolicyAssistant:
    def __init__(self):
        # Initialize models
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.llm = genai.GenerativeModel("gemini-1.5-flash")
        
        # Initialize vector store
        self.index = None
        self.sections = []
        self.metadata = []
        
    def load_policy(self, file_path):
        """Load and index policy document"""
        from .loader import load_document
        from .processor import chunk_policy
        
        # Load and chunk document
        text = load_document(file_path)
        self.sections = chunk_policy(text)
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(self.sections)
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))
        
        # Store metadata
        policy_name = os.path.basename(file_path)
        self.metadata = [{
            "policy": policy_name, 
            "section": f"Section {i+1}"
        } for i in range(len(self.sections))]
    
    def search(self, query, k=3):
        """Find relevant policy sections"""
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "content": self.sections[idx],
                "source": f"{self.metadata[idx]['policy']} - {self.metadata[idx]['section']}",
                "distance": float(distances[0][i])
            })
        return results
    
    def generate_response(self, query, context):
        """Generate policy-compliant answer"""
        prompt = f"""
        You are an HR policy expert. Answer the user's question using ONLY the 
        provided policy context. Always cite your source using the exact format: [Source: ...]
        
        Policy Context:
        {context}
        
        Question: {query}
        Answer:
        """
        
        response = self.llm.generate_content(prompt)
        return response.text