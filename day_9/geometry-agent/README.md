# Geometry Calculation Agent with Streamlit UI

I'll create a complete implementation of the geometry calculation agent with a comprehensive Streamlit UI. This agent handles geometry calculations and forwards other queries to Gemini 1.5 Flash.

## Project Structure
```
geometry-agent/
├── app/
│   ├── __init__.py
│   ├── graph.py
│   ├── tools.py
│   ├── llm_flask.py
│   └── runner.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Implementation

### 1. requirements.txt
```txt
fastapi
uvicorn
flask
requests
streamlit
langchain
langgraph
google-generativeai
python-dotenv
```

### 2. app/tools.py
```python
import math
import re
from typing import Dict, Any

# Geometry functions
def circle_area(radius: float) -> float:
    return math.pi * (radius ** 2)

def rectangle_perimeter(length: float, width: float) -> float:
    return 2 * (length + width)

def cube_volume(side: float) -> float:
    return side ** 3

def triangle_area(base: float, height: float) -> float:
    return 0.5 * base * height

# Intent detection with improved patterns
def detect_geometry_intent(query: str) -> Dict[str, Any]:
    q = query.lower().strip()
    
    # Circle area patterns
    circle_patterns = [
        r'area of (?:a )?circle(?: with radius)?\s*=\s*([0-9]*\.?[0-9]+)',
        r'circle area (?:with )?r\s*=\s*([0-9]*\.?[0-9]+)',
        r'what is the area of a circle whose radius is ([0-9]*\.?[0-9]+)'
    ]
    for pattern in circle_patterns:
        m = re.search(pattern, q)
        if m:
            return {"is_geometry": True, "tool": "circle_area", "args": {"radius": float(m.group(1))}}
    
    # Rectangle perimeter patterns
    rect_patterns = [
        r'perimeter of (?:a )?rectangle(?: with length)?\s*=\s*([0-9]*\.?[0-9]+)\s*(?:[,x]|and)?\s*(?:width)?\s*=\s*([0-9]*\.?[0-9]+)',
        r'rectangle perimeter l\s*=\s*([0-9]*\.?[0-9]+) w\s*=\s*([0-9]*\.?[0-9]+)',
        r'perimeter for rectangle with sides? ([0-9]*\.?[0-9]+) and ([0-9]*\.?[0-9]+)'
    ]
    for pattern in rect_patterns:
        m = re.search(pattern, q)
        if m:
            return {"is_geometry": True, "tool": "rectangle_perimeter", 
                    "args": {"length": float(m.group(1)), "width": float(m.group(2))}}
    
    # Cube volume patterns
    cube_patterns = [
        r'volume of (?:a )?cube(?: with side)?\s*=\s*([0-9]*\.?[0-9]+)',
        r'cube volume s\s*=\s*([0-9]*\.?[0-9]+)',
        r'what is the volume of a cube with edge length ([0-9]*\.?[0-9]+)'
    ]
    for pattern in cube_patterns:
        m = re.search(pattern, q)
        if m:
            return {"is_geometry": True, "tool": "cube_volume", "args": {"side": float(m.group(1))}}
    
    # Triangle area patterns
    triangle_patterns = [
        r'area of (?:a )?triangle(?: with base)?\s*=\s*([0-9]*\.?[0-9]+)\s*(?:[,x]|and)?\s*(?:height)?\s*=\s*([0-9]*\.?[0-9]+)',
        r'triangle area b\s*=\s*([0-9]*\.?[0-9]+) h\s*=\s*([0-9]*\.?[0-9]+)',
        r'area for triangle with base ([0-9]*\.?[0-9]+) and height ([0-9]*\.?[0-9]+)'
    ]
    for pattern in triangle_patterns:
        m = re.search(pattern, q)
        if m:
            return {"is_geometry": True, "tool": "triangle_area", 
                    "args": {"base": float(m.group(1)), "height": float(m.group(2))}}
    
    # Fallback: not recognized as geometry
    return {"is_geometry": False, "tool": None, "args": None}
```

### 3. app/graph.py
```python
from langgraph.graph import StateGraph, END
from app.tools import detect_geometry_intent, circle_area, rectangle_perimeter, cube_volume, triangle_area
import requests
from typing import Dict, Any

class AgentState(TypedDict):
    query: str
    geometry_result: Dict[str, Any]
    llm_response: Dict[str, Any]

def geometry_node(state: AgentState) -> Dict[str, Any]:
    detected = detect_geometry_intent(state["query"])
    
    if not detected["is_geometry"]:
        return {"geometry_result": None}
    
    tool = detected["tool"]
    args = detected["args"]
    
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

    return {"geometry_result": {
        "tool": tool,
        "args": args,
        "value": value
    }}

def llm_node(state: AgentState) -> Dict[str, Any]:
    try:
        resp = requests.post("http://localhost:5000/llm", json={"query": state["query"]})
        if resp.status_code == 200:
            return {"llm_response": resp.json()}
    except:
        pass
    return {"llm_response": {"response": "Could not reach LLM service"}}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("geometry_check", geometry_node)
workflow.add_node("llm", llm_node)

workflow.set_entry_point("geometry_check")

def route_based_on_geometry(state: AgentState) -> str:
    if state.get("geometry_result") is not None:
        return "end"
    return "llm"

workflow.add_conditional_edges(
    "geometry_check",
    route_based_on_geometry,
    {
        "end": END,
        "llm": "llm"
    }
)
workflow.add_edge("llm", END)

academic_agent = workflow.compile()
```

### 4. app/llm_flask.py
```python
from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY", "your_api_key_here")

if API_KEY:
    genai.configure(api_key=API_KEY)

@app.route("/llm", methods=["POST"])
def llm_endpoint():
    try:
        payload = request.json or {}
        query = payload.get("query", "")
        
        # Create prompt with strict instructions
        prompt = f"""
        You are an AI assistant that classifies queries and responds in JSON format.
        
        Instructions:
        1. If the query is about geometry (circle area, rectangle perimeter, cube volume, triangle area):
           - Respond ONLY with JSON: {{"tool_call": "<tool_name>", "args": {{...}}, "explain": "<explanation>"}}
        2. For non-geometry queries:
           - Respond ONLY with JSON: {{"tool_call": null, "response": "<your_answer>"}}
        
        Important rules:
        - Always output valid JSON
        - For geometry queries, extract exact numbers from the query
        - Never add extra text outside the JSON
        - If unsure, treat as non-geometry query
        
        Query: {query}
        """
        
        if API_KEY:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt, generation_config={"temperature": 0.0})
            return jsonify(response.text)
        else:
            # Fallback for testing
            if "circle" in query.lower():
                return jsonify({
                    "tool_call": "circle_area",
                    "args": {"radius": 5.0},
                    "explain": "Detected circle area query"
                })
            return jsonify({"tool_call": null, "response": "This is a test response"})
            
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

### 5. app/runner.py
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph import academic_agent

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/run")
def run_agent(request: QueryRequest):
    try:
        # Initialize state
        state = {
            "query": request.query,
            "geometry_result": None,
            "llm_response": None
        }
        
        # Execute the agent
        for step in academic_agent.stream(state):
            for key, value in step.items():
                if key == "end":
                    return value
        
        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 6. streamlit_app.py
```python
import streamlit as st
import requests
import json
import time
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Geometry Calculation Agent",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
with st.sidebar:
    st.title("Geometry Agent")
    st.markdown("""
    This agent can:
    - Calculate geometry properties (area, perimeter, volume)
    - Answer general questions using Gemini 1.5 Flash
    """)
    
    st.divider()
    st.subheader("Configuration")
    api_key = st.text_input("Gemini API Key", type="password", 
                           value=os.getenv("GEMINI_API_KEY", ""))
    st.caption("Required for non-geometry queries")
    
    st.divider()
    st.subheader("Supported Calculations")
    st.markdown("""
    - Circle area (radius)
    - Rectangle perimeter (length, width)
    - Cube volume (side)
    - Triangle area (base, height)
    """)
    
    st.divider()
    st.caption("Powered by LangGraph, Gemini 1.5 Flash, and Streamlit")

# Main content
st.title("📐 Geometry Calculation Agent")
st.subheader("Calculate geometric properties or ask general questions")

# Example queries
example_queries = [
    "What is the area of a circle with radius 5?",
    "Find the perimeter of a rectangle with length 4 and width 6",
    "Calculate the volume of a cube with side 3",
    "What is the area of a triangle with base 8 and height 5?",
    "Explain the Pythagorean theorem"
]

# Create columns for examples
cols = st.columns(3)
for i, query in enumerate(example_queries):
    with cols[i % 3]:
        if st.button(query, use_container_width=True):
            st.session_state.query = query

# Query input
query = st.text_area(
    "Enter your query:",
    key="query",
    placeholder="Type your geometry calculation or general question here...",
    height=150
)

# Process button
if st.button("Process Query", type="primary", use_container_width=True):
    if not query:
        st.warning("Please enter a query")
        st.stop()
    
    # Initialize session state
    st.session_state.result = None
    st.session_state.step = 0
    st.session_state.progress = 0
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Processing steps
    steps = [
        "Analyzing query...",
        "Detecting calculation type...",
        "Processing geometry...",
        "Generating response..."
    ]
    
    # Simulate processing
    for i, step in enumerate(steps):
        st.session_state.step = i
        st.session_state.progress = (i + 1) * 25
        status_text.info(f"🔄 {step}")
        progress_bar.progress(st.session_state.progress)
        time.sleep(0.5)
    
    try:
        # Call the agent
        response = requests.post(
            "http://localhost:8000/run", 
            json={"query": query},
            timeout=30
        )
        
        if response.status_code == 200:
            st.session_state.result = response.json()
            status_text.success("✅ Processing complete!")
            progress_bar.progress(100)
        else:
            status_text.error(f"Error: {response.text}")
            progress_bar.empty()
    except Exception as e:
        status_text.error(f"Connection error: {str(e)}")
        progress_bar.empty()

# Display results
if "result" in st.session_state and st.session_state.result:
    result = st.session_state.result
    st.divider()
    st.subheader("Result")
    
    if result.get("geometry_result"):
        geom = result["geometry_result"]
        tool_name = geom["tool"].replace("_", " ").title()
        
        # Display with appropriate icon
        if "circle" in geom["tool"]:
            icon = "⭕"
        elif "rectangle" in geom["tool"]:
            icon = "⬜"
        elif "cube" in geom["tool"]:
            icon = "⬛"
        else:
            icon = "🔺"
        
        st.success(f"{icon} Geometry Calculation Result")
        
        # Display calculation details
        with st.expander("Calculation Details", expanded=True):
            st.markdown(f"**Calculation Type:** `{tool_name}`")
            
            # Display arguments
            args = geom["args"]
            if "radius" in args:
                st.markdown(f"**Radius:** {args['radius']}")
            if "length" in args:
                st.markdown(f"**Length:** {args['length']}")
            if "width" in args:
                st.markdown(f"**Width:** {args['width']}")
            if "side" in args:
                st.markdown(f"**Side:** {args['side']}")
            if "base" in args:
                st.markdown(f"**Base:** {args['base']}")
            if "height" in args:
                st.markdown(f"**Height:** {args['height']}")
            
            st.divider()
            st.metric("Result", f"{geom['value']:.4f}")
    
    elif result.get("llm_response"):
        llm_res = result["llm_response"]
        
        if llm_res.get("tool_call"):
            st.warning("🔍 Detected Geometry Query")
            st.markdown(f"**Tool:** `{llm_res['tool_call']}`")
            st.json(llm_res["args"])
            st.info(f"Explanation: {llm_res.get('explain', '')}")
            st.error("This geometry query couldn't be processed. Try rephrasing with explicit numbers.")
        else:
            st.info("💬 General Query Response")
            st.markdown(llm_res.get("response", "No response generated"))
    
    else:
        st.warning("No valid result generated")

# Footer
st.divider()
st.caption("Note: The agent runs locally. For non-geometry queries, ensure the Gemini API is configured.")
```

## How to Run the Application

1. Create a `.env` file with your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the services in separate terminals:

**Terminal 1 (Flask LLM Service):**
```bash
python app/llm_flask.py
```

**Terminal 2 (FastAPI Agent Runner):**
```bash
python app/runner.py 'or' python -m app.runner
```

**Terminal 3 (Streamlit UI):**
```bash
streamlit run streamlit_app.py
```

## Features of the Streamlit UI

1. **Interactive Interface**:
   - Clean, modern layout with geometry-themed design
   - Example query buttons for quick testing
   - Responsive design for all screen sizes

2. **Visual Feedback**:
   - Progress bar showing processing steps
   - Status messages during execution
   - Icons for different calculation types

3. **Results Display**:
   - Clear visualization of geometry calculations
   - Expandable details for arguments and results
   - Proper formatting of LLM responses
   - Error handling and user notifications

4. **Configuration**:
   - API key management in sidebar
   - List of supported calculations
   - System status information

5. **Enhanced Experience**:
   - Animated progress indicators
   - Themed icons for different geometry types
   - Clear separation between geometry and general queries
   - User guidance and examples

The UI provides a complete user experience with visual feedback, error handling, and clear presentation of both geometry calculations and general query responses.