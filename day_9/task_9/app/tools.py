import json
import os
import requests
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load product database
try:
    with open("data/products.json", "r") as f:
        PRODUCTS = json.load(f)
    logger.info("Loaded product database with %d items", len(PRODUCTS))
except Exception as e:
    logger.error("Error loading products.json: %s", str(e))
    PRODUCTS = []

# Initialize Tavily client only if API key is available
tavily = None
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY:
    try:
        from tavily import TavilyClient
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        logger.info("Tavily client initialized")
    except ImportError:
        logger.warning("Tavily package not installed")
else:
    logger.warning("TAVILY_API_KEY not set. Web search will be limited.")

# Initialize text embedding model
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("Text embedding model loaded")
except Exception as e:
    logger.error("Error loading embedding model: %s", str(e))
    model = None

# Create FAISS index for products if possible
index = None
if model and PRODUCTS:
    try:
        product_descriptions = [f"{p['name']} {p['category']} {p['description']}" for p in PRODUCTS]
        embeddings = model.encode(product_descriptions)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings).astype('float32'))
        logger.info("FAISS index created with %d products", len(PRODUCTS))
    except Exception as e:
        logger.error("Error creating FAISS index: %s", str(e))
        index = None

def web_search_tool(query: str) -> dict:
    """Perform web search for live pricing and reviews"""
    if not tavily:
        logger.warning("Web search called without Tavily client")
        return {"results": []}
    
    try:
        results = tavily.search(
            query=query,
            search_depth="advanced",
            include_answer=True,
            max_results=5
        )
        return results
    except Exception as e:
        logger.error("Web search failed: %s", str(e))
        return {"error": str(e), "results": []}

def rag_search_tool(query: str) -> dict:
    """Search product database using RAG"""
    if not index or not model:
        logger.warning("RAG search called without proper setup")
        return {"products": PRODUCTS[:3]}  # Return first 3 products as fallback
    
    try:
        # Encode query
        query_embedding = model.encode([query])[0]
        
        # Search index
        distances, indices = index.search(np.array([query_embedding]).astype('float32'), k=3)
        
        # Get products
        results = [PRODUCTS[i] for i in indices[0]]
        return {"products": results}
    except Exception as e:
        logger.error("RAG search failed: %s", str(e))
        return {"products": PRODUCTS[:3]}  # Return first 3 products as fallback

def summarize_results(web_data: dict, rag_data: dict, query: str) -> str:
    """Summarize results from web and RAG"""
    # Prepare data for LLM
    context = {
        "query": query,
        "web_results": web_data.get("results", []),
        "rag_products": rag_data.get("products", [])
    }
    
    # Send to summarization endpoint
    try:
        response = requests.post(
            "http://localhost:5000/summarize",
            json=context,
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("summary", "Summary not available")
    except Exception as e:
        logger.error("Summarization request failed: %s", str(e))
    
    # Fallback summary
    products = rag_data.get("products", [])
    if products:
        product_names = ", ".join([p["name"] for p in products])
        return f"Based on your query '{query}', I recommend: {product_names}"
    return "Could not generate summary"