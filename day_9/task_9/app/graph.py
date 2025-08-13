from langgraph.graph import StateGraph, END
from app.agents import router_agent, web_research_agent, rag_agent, summarization_agent, general_agent
import logging
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(Dict):
    query: str
    route: str
    web_data: Dict
    rag_data: Dict
    summary: str

# Create workflow
workflow = StateGraph(AgentState)

# Define nodes
workflow.add_node("router", router_agent)
workflow.add_node("web_research", web_research_agent)
workflow.add_node("rag", rag_agent)
workflow.add_node("summarize", summarization_agent)
workflow.add_node("general", general_agent)

# Set entry point
workflow.set_entry_point("router")

# Define routing logic
def route_decision(state: AgentState) -> str:
    route = state.get("route", "general")
    logger.info(f"Routing to: {route}")
    
    if route == "web_research":
        return "web_research"
    elif route == "rag":
        return "rag"
    elif route == "combined":
        return "parallel"
    elif route == "general":
        return "general"
    else:
        return "general"

# Add conditional edges
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "web_research": "web_research",
        "rag": "rag",
        "parallel": "parallel",
        "general": "general"
    }
)

# Add edges
workflow.add_edge("web_research", "summarize")
workflow.add_edge("rag", "summarize")
workflow.add_edge("summarize", END)
workflow.add_edge("general", END)

# Add parallel processing for combined route
def run_parallel(state: AgentState) -> Dict:
    logger.info("Running parallel agents")
    web_data = web_research_agent(state)
    rag_data = rag_agent(state)
    return {"web_data": web_data["web_data"], "rag_data": rag_data["rag_data"]}

workflow.add_node("parallel", run_parallel)
workflow.add_edge("parallel", "summarize")

# Compile the graph
agent = workflow.compile()