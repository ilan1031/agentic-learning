from typing import Dict, List
import time

class MemoryStore:
    def __init__(self):
        self.history = []
    
    def add_entry(self, query: str, response: str) -> None:
        """Add a conversation entry to memory"""
        self.history.append({
            "query": query,
            "response": response,
            "timestamp": time.time()
        })
    
    def get_history(self, max_entries: int = 5) -> List[Dict]:
        """Get conversation history"""
        return self.history[-max_entries:]
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.history = []

# Initialize memory store
memory = MemoryStore()
