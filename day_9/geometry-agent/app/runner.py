from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph import academic_agent
import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "geometry-agent"}

@app.post("/run")
def run_agent(request: QueryRequest):
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Initialize state
        state = {
            "query": request.query,
            "geometry_result": None,
            "llm_response": None
        }
        
        # Execute the agent
        final_state = academic_agent.invoke(state)
        logger.info(f"Agent result: {final_state}")
        
        # Ensure we always return a response
        if not final_state.get("geometry_result") and not final_state.get("llm_response"):
            final_state["llm_response"] = {"response": "No result generated. Please try again."}
        
        return final_state
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        return {
            "error": str(e),
            "llm_response": {"response": "An error occurred while processing your query."}
        }

if __name__ == "__main__":
    port = int(os.getenv("AGENT_PORT", 8000))
    logger.info(f"Starting agent runner on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)