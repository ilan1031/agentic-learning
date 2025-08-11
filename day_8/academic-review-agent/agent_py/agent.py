from .graph import academic_agent

def run_agent(topic: str) -> str:
    """Run the academic agent and return the report"""
    # Create initial state with all required keys
    initial_state = {
        "topic": topic,
        "raw_results": [],
        "filtered_results": [],
        "sources": "",
        "report": ""
    }
    
    # Execute the agent
    result = academic_agent.invoke(initial_state)
    return result["report"]