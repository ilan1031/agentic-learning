from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from . import tools, prompts
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

class GraphState(TypedDict):
    topic: str
    raw_results: List[Dict[str, Any]]
    filtered_results: List[Dict[str, Any]]
    sources: str
    report: str

def search_node(state: GraphState) -> dict:
    """Node to search academic sources"""
    results = tools.search_academic_sources(state["topic"])
    return {"raw_results": results}

def filter_node(state: GraphState) -> dict:
    """Node to filter academic sources"""
    filtered = tools.filter_academic_sources(state["raw_results"])
    return {"filtered_results": filtered}

def format_sources_node(state: GraphState) -> dict:
    """Node to format sources for LLM"""
    sources = "\n\n".join([
        f"**{res['title']}**\n{res['content']}\nSource: {res['url']}" 
        for res in state["filtered_results"]
    ])
    return {"sources": sources}

def generate_report_node(state: GraphState) -> dict:
    """Node to generate academic report"""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    chain = prompts.ACADEMIC_REVIEW_PROMPT | llm | StrOutputParser()
    
    report = chain.invoke({
        "topic": state["topic"],
        "sources": state["sources"]
    })
    return {"report": report}

# Create the graph
workflow = StateGraph(GraphState)

# Define nodes
workflow.add_node("search", search_node)
workflow.add_node("filter", filter_node)
workflow.add_node("format_sources", format_sources_node)
workflow.add_node("generate_report", generate_report_node)

# Set edges
workflow.set_entry_point("search")
workflow.add_edge("search", "filter")
workflow.add_edge("filter", "format_sources")
workflow.add_edge("format_sources", "generate_report")
workflow.add_edge("generate_report", END)

# Compile the graph
academic_agent = workflow.compile()