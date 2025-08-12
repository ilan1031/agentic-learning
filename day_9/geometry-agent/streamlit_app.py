import streamlit as st
import requests
import json
import time
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

# Custom CSS for better alignment
st.markdown("""
<style>
    .stButton button {
        width: 100%;
    }
    .stTextArea textarea {
        min-height: 150px;
    }
    .result-card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .geometry-result {
        background-color: #e6f7ff;
        border-left: 4px solid #1890ff;
    }
    .llm-result {
        background-color: #f6ffed;
        border-left: 4px solid #52c41a;
    }
    .error-result {
        background-color: #fff2f0;
        border-left: 4px solid #ff4d4f;
    }
    .debug-panel {
        font-size: 0.85em;
        padding: 10px;
        background-color: #fafafa;
        border-radius: 5px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("📐 Geometry Agent")
    st.markdown("""
    This agent can:
    - Calculate geometry properties (area, perimeter, volume)
    - Answer general questions using Gemini 1.5 Flash
    """)
    
    st.divider()
    st.subheader("Configuration")
    api_key = st.text_input("Gemini API Key", type="password", 
                           value=os.getenv("GEMINI_API_KEY", ""))
    os.environ["GEMINI_API_KEY"] = api_key
    st.caption("Required for non-geometry queries")
    
    st.divider()
    st.subheader("Supported Calculations")
    st.markdown("""
    - **Circle area**: radius
    - **Rectangle perimeter**: length, width
    - **Cube volume**: side
    - **Triangle area**: base, height
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
st.write("### Try these examples:")
cols = st.columns(3)
for i, query in enumerate(example_queries):
    with cols[i % 3]:
        if st.button(query, use_container_width=True, key=f"example_{i}"):
            st.session_state.query = query

# Query input
st.divider()
st.write("### Enter your query")
query = st.text_area(
    "Type your geometry calculation or question:",
    key="query",
    placeholder="Example: 'What is the area of a circle with radius 5?'",
    height=150,
    label_visibility="collapsed"
)

# Process button
col1, col2 = st.columns([1, 3])
with col1:
    process_btn = st.button("Process Query", type="primary", use_container_width=True)

# Initialize session state
if "result" not in st.session_state:
    st.session_state.result = None
if "processing" not in st.session_state:
    st.session_state.processing = False

if process_btn and query:
    st.session_state.processing = True
    st.session_state.result = None

# Processing UI
if st.session_state.processing:
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
        status_text.info(f"🔄 {step}")
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.8)
    
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
            time.sleep(0.5)
        else:
            st.session_state.result = {"error": response.text}
            status_text.error(f"Error: {response.text}")
            progress_bar.empty()
    except Exception as e:
        st.session_state.result = {"error": str(e)}
        status_text.error(f"Connection error: {str(e)}")
        progress_bar.empty()
    
    st.session_state.processing = False
    st.rerun()

# Display results
if st.session_state.result:
    result = st.session_state.result
    st.divider()
    st.write("## Result")
    
    if result.get("geometry_result"):
        geom = result["geometry_result"]
        tool_name = geom["tool"].replace("_", " ").title()
        source = geom.get("source", "direct")
        
        # Get display details based on tool
        tool_details = {
            "circle_area": {
                "name": "Circle Area",
                "formula": "π × r²",
                "icon": "⭕",
                "args": [{"name": "Radius", "key": "radius", "symbol": "r"}]
            },
            "rectangle_perimeter": {
                "name": "Rectangle Perimeter",
                "formula": "2 × (l + w)",
                "icon": "⬜",
                "args": [
                    {"name": "Length", "key": "length", "symbol": "l"},
                    {"name": "Width", "key": "width", "symbol": "w"}
                ]
            },
            "cube_volume": {
                "name": "Cube Volume",
                "formula": "s³",
                "icon": "⬛",
                "args": [{"name": "Side", "key": "side", "symbol": "s"}]
            },
            "triangle_area": {
                "name": "Triangle Area",
                "formula": "½ × b × h",
                "icon": "🔺",
                "args": [
                    {"name": "Base", "key": "base", "symbol": "b"},
                    {"name": "Height", "key": "height", "symbol": "h"}
                ]
            }
        }
        
        details = tool_details.get(geom["tool"], {})
        
        # Display result card
        with st.container():
            st.markdown(f"<div class='result-card geometry-result'>", unsafe_allow_html=True)
            
            st.markdown(f"### {details.get('icon', '📐')} {details.get('name', tool_name)}")
            
            # Display arguments
            args = geom["args"]
            if args:
                st.write("**Parameters:**")
                arg_cols = st.columns(len(details["args"]))
                for i, arg_spec in enumerate(details["args"]):
                    with arg_cols[i]:
                        st.metric(
                            f"{arg_spec['symbol']} ({arg_spec['name']})", 
                            args[arg_spec["key"]]
                        )
            
            # Display calculation
            st.divider()
            st.write(f"**Calculation:** {details.get('formula', '')}")
            
            # Display result
            st.metric("Result", f"{geom['value']:.4f}")
            
            # Source indicator
            if source == "llm":
                st.caption("Detected and calculated using Gemini 1.5 Flash")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif result.get("llm_response"):
        llm_res = result["llm_response"]
        
        # Display result card
        with st.container():
            st.markdown(f"<div class='result-card llm-result'>", unsafe_allow_html=True)
            
            if llm_res.get("tool_call"):
                st.markdown("### 🔍 Detected Geometry Query")
                st.write(f"**Tool:** `{llm_res['tool_call']}`")
                
                # Display arguments
                if llm_res.get("args"):
                    st.write("**Arguments:**")
                    for key, value in llm_res["args"].items():
                        st.write(f"- **{key.capitalize()}:** {value}")
                
                if llm_res.get("explain"):
                    st.info(f"**Explanation:** {llm_res['explain']}")
                
                st.warning("This geometry query couldn't be processed directly. Try using explicit numbers like 'radius 5' instead of 'radius five'.")
            else:
                st.markdown("### 💬 Response")
                st.write(llm_res.get("response", "No response generated"))
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif result.get("error"):
        with st.container():
            st.markdown(f"<div class='result-card error-result'>", unsafe_allow_html=True)
            st.error("### ⚠️ Processing Error")
            st.write(result["error"])
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"<div class='result-card error-result'>", unsafe_allow_html=True)
            st.warning("### ❓ No Result Generated")
            st.write("The agent didn't return a valid result. This could be because:")
            st.markdown("""
            - The query couldn't be recognized as a geometry calculation
            - The LLM service might not be running
            - There was an error in processing
            """)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Debug panel
    with st.expander("Debug Information"):
        st.write("### Agent State")
        st.json(result)
        
        st.write("### Service Status")
        try:
            # Check LLM service
            llm_status = requests.get("http://localhost:5000", timeout=2).status_code
            st.write(f"LLM Service (localhost:5000): {'✅ Running' if llm_status == 404 else '⚠️ Unexpected status'}")
        except:
            st.write("LLM Service (localhost:5000): 🔴 Not reachable")
        
        try:
            # Check Agent service
            agent_status = requests.get("http://localhost:8000", timeout=2).status_code
            st.write(f"Agent Service (localhost:8000): {'✅ Running' if agent_status == 404 else '⚠️ Unexpected status'}")
        except:
            st.write("Agent Service (localhost:8000): 🔴 Not reachable")

# Footer
st.divider()
st.caption("Note: For non-geometry queries, ensure the Gemini API key is set in the sidebar. Services must be running locally.")

# Start instructions
if not st.session_state.result and not st.session_state.processing:
    st.info("💡 Enter a query above or click an example to get started")