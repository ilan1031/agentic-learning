from app.tools import web_search_tool, rag_search_tool, summarize_results
from app.memory import memory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def router_agent(state: dict) -> dict:
    """Determine which agent should handle the query"""
    logger.info("Running router agent")
    query = state["query"].lower()
    
    # Simple keyword-based routing as fallback
    if any(keyword in query for keyword in ["price", "live", "current", "today"]):
        return {"route": "web_research"}
    elif any(keyword in query for keyword in ["spec", "feature", "compare", "difference"]):
        return {"route": "rag"}
    elif any(keyword in query for keyword in ["best", "recommend", "top", "under"]):
        return {"route": "combined"}
    else:
        return {"route": "general"}

def web_research_agent(state: dict) -> dict:
    """Perform web research for live pricing and reviews"""
    logger.info("Running web research agent")
    web_data = web_search_tool(state["query"])
    return {"web_data": web_data}

def rag_agent(state: dict) -> dict:
    """Retrieve product information from database"""
    logger.info("Running RAG agent")
    rag_data = rag_search_tool(state["query"])
    return {"rag_data": rag_data}

def summarization_agent(state: dict) -> dict:
    """Summarize results from multiple sources"""
    logger.info("Running summarization agent")
    summary = summarize_results(
        state.get("web_data", {}),
        state.get("rag_data", {}),
        state["query"]
    )
    
    # Add to memory
    memory.add_entry(state["query"], summary)
    
    return {"summary": summary}

def general_agent(state: dict) -> dict:
    """Handle general queries with LLM"""
    logger.info("Running general agent")
    return {"summary": f"I received your general query: '{state['query']}'. " 
                      "For detailed product recommendations, try asking about specific products."}