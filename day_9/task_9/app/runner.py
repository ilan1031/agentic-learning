from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import agent
import uvicorn
import os
from dotenv import load_dotenv
import logging
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/run")
def run_agent(request: QueryRequest):
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Initialize state with all required fields
        state = {
            "query": request.query,
            "route": "",
            "web_data": {"results": []},
            "rag_data": {"products": []},
            "summary": ""
        }
        
        # Execute agent with error handling
        try:
            result = agent.invoke(state)
            
            # Ensure we always have a summary
            if not result.get("summary"):
                products = result.get("rag_data", {}).get("products", [])
                if products:
                    product_names = ", ".join([p["name"] for p in products[:3]])
                    result["summary"] = f"Recommended products: {product_names}"
                else:
                    result["summary"] = "Here are some options to consider"
            
            return result
            
        except Exception as e:
            logger.error(f"Agent execution error: {str(e)}")
            return {
                "error": str(e),
                "summary": "I encountered an error while processing your request",
                "web_data": {"results": []},
                "rag_data": {"products": []}
            }
            
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return {
            "error": str(e),
            "summary": "An error occurred while processing your query",
            "web_data": {"results": []},
            "rag_data": {"products": []}
        }

@app.get("/")
def health_check():
    return {"status": "ok", "service": "product-recommendation-agent"}

if __name__ == "__main__":
    port = int(os.getenv("AGENT_PORT", 8000))
    logger.info(f"Starting agent runner on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)