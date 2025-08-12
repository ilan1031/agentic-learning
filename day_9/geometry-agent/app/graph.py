from langgraph.graph import StateGraph, END
from app.tools import detect_geometry_intent, circle_area, rectangle_perimeter, cube_volume, triangle_area
import requests
from typing import Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

def geometry_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Running geometry node")
    try:
        detected = detect_geometry_intent(state["query"])
        logger.debug(f"Detected intent: {detected}")
        
        if detected["is_geometry"]:
            tool = detected["tool"]
            args = detected["args"]
            
            logger.info(f"Detected geometry: {tool} with args {args}")
            
            if tool == "circle_area":
                value = circle_area(args["radius"])
            elif tool == "rectangle_perimeter":
                value = rectangle_perimeter(args["length"], args["width"])
            elif tool == "cube_volume":
                value = cube_volume(args["side"])
            elif tool == "triangle_area":
                value = triangle_area(args["base"], args["height"])
            else:
                value = None

            return {
                "geometry_result": {
                    "tool": tool,
                    "args": args,
                    "value": value,
                    "source": "direct"
                }
            }
    except Exception as e:
        logger.error(f"Geometry node error: {str(e)}")
    
    return {"geometry_result": None}

def llm_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Running LLM node")
    try:
        resp = requests.post(
            "http://localhost:5000/llm", 
            json={"query": state["query"]},
            timeout=10
        )
        
        if resp.status_code == 200:
            response_data = resp.json()
            logger.debug(f"LLM response: {response_data}")
            
            # Check if LLM detected a geometry tool call
            if response_data.get("tool_call") and response_data.get("args"):
                tool = response_data["tool_call"]
                args = response_data["args"]
                
                logger.info(f"LLM detected geometry: {tool} with args {args}")
                
                if tool == "circle_area" and "radius" in args:
                    value = circle_area(args["radius"])
                elif tool == "rectangle_perimeter" and "length" in args and "width" in args:
                    value = rectangle_perimeter(args["length"], args["width"])
                elif tool == "cube_volume" and "side" in args:
                    value = cube_volume(args["side"])
                elif tool == "triangle_area" and "base" in args and "height" in args:
                    value = triangle_area(args["base"], args["height"])
                else:
                    value = None
                
                if value is not None:
                    return {
                        "geometry_result": {
                            "tool": tool,
                            "args": args,
                            "value": value,
                            "source": "llm"
                        },
                        "llm_response": response_data
                    }
            
            # If we didn't process geometry, return LLM response
            return {"llm_response": response_data}
    except Exception as e:
        logger.error(f"LLM node error: {str(e)}")
    
    return {"llm_response": {"response": "Could not process query"}}

# Build graph
workflow = StateGraph(dict)

workflow.add_node("geometry_check", geometry_node)
workflow.add_node("llm", llm_node)

workflow.set_entry_point("geometry_check")

def route_based_on_geometry(state):
    # If we have a valid geometry result, end
    if state.get("geometry_result") and state["geometry_result"].get("value") is not None:
        return END
    # Otherwise, go to LLM
    return "llm"

workflow.add_conditional_edges(
    "geometry_check",
    route_based_on_geometry,
    {
        END: END,
        "llm": "llm"
    }
)
workflow.add_edge("llm", END)

academic_agent = workflow.compile()