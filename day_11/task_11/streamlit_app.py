import streamlit as st
import requests
import json
import time
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="JSON Validation System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-section {
        background: linear-gradient(135deg, #2c3e50, #4a6491);
        padding: 25px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: #ffffff;
    }
    .error-card {
        border-left: 5px solid #e74c3c;
    }
    .success-card {
        border-left: 5px solid #2ecc71;
    }
    .json-container {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        font-family: monospace;
        max-height: 400px;
        overflow: auto;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        color: white;
    }
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin: 3px;
    }
    .syntax-error {
        background-color: #e74c3c;
        color: white;
    }
    .schema-error {
        background-color: #f39c12;
        color: white;
    }
    .success-tag {
        background-color: #2ecc71;
        color: white;
    }
    .tab-container {
        padding: 15px;
        border: 1px solid #e3e6f0;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "original_json" not in st.session_state:
    st.session_state.original_json = ""
if "validation_result" not in st.session_state:
    st.session_state.validation_result = None
if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("""
<div class="header-section">
    <h1 style="color:white; margin:0;">🔍 JSON Data Validation System</h1>
    <p style="color:white; margin:0;">AI-powered JSON validation with CrewAI multi-agent system</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 1])

# Sidebar - JSON templates
with col1:
    st.sidebar.title("📋 JSON Templates")
    
    templates = {
        "Simple Object": json.dumps({"name": "John", "age": 30, "city": "New York"}, indent=2),
        "Array of Objects": json.dumps([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], indent=2),
        "Nested Structure": json.dumps({
            "company": "TechCorp",
            "employees": [
                {"name": "John", "skills": ["Python", "Java"]},
                {"name": "Sarah", "skills": ["JavaScript", "SQL"]}
            ]
        }, indent=2),
        "Invalid JSON": '{\n  "name": "John"\n  "age": 30,\n  "city": "New York"\n}',
        "Schema Mismatch": json.dumps({"name": "John", "age": "thirty", "city": "New York"}, indent=2)
    }
    
    selected_template = st.sidebar.selectbox("Load Template", list(templates.keys()))
    
    if st.sidebar.button(f"Load {selected_template}", use_container_width=True):
        st.session_state.original_json = templates[selected_template]
        st.rerun()
    
    st.sidebar.divider()
    st.sidebar.title("⚙️ Options")
    auto_validate = st.sidebar.checkbox("Auto-validate on change", False)
    show_raw = st.sidebar.checkbox("Show raw JSON", True)
    
    st.sidebar.divider()
    st.sidebar.title("📚 Documentation")
    with st.sidebar.expander("Validation Rules"):
        st.markdown("""
        - **Syntax Validation**: Checks for valid JSON structure
        - **Schema Validation**: Ensures data matches expected format
        - **Common Errors**:
          - Missing commas
          - Trailing commas
          - Incorrect quotes
          - Type mismatches
        """)
    
    if st.sidebar.button("Clear All", type="secondary"):
        st.session_state.original_json = ""
        st.session_state.validation_result = None
        st.rerun()

# Main content
with col2:
    # JSON input
    st.subheader("📥 Input JSON")
    json_input = st.text_area(
        "Enter JSON to validate:",
        value=st.session_state.original_json,
        height=300,
        key="json_input"
    )
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("🔍 Analyze Only", use_container_width=True)
    with col2:
        validate_btn = st.button("✅ Analyze & Correct", type="primary", use_container_width=True)
    
    # Set original JSON in session state
    st.session_state.original_json = json_input
    
    # Start processing if button clicked
    if analyze_btn or validate_btn or (auto_validate and json_input):
        if not json_input.strip():
            st.warning("Please enter JSON to validate")
        else:
            st.session_state.processing = True
            st.session_state.full_validation = validate_btn
            st.rerun()
    
    # Processing state
    if st.session_state.processing:
        with st.status("🔍 Validating JSON...", expanded=True) as status:
            steps = [
                "Initializing validation agents...",
                "Analyzing JSON syntax...",
                "Checking schema compliance...",
                "Generating error report...",
                "Correcting issues..."
            ]
            
            for i, step in enumerate(steps):
                # Skip correction step for analyze-only
                if i == 4 and not st.session_state.full_validation:
                    continue
                    
                st.write(step)
                time.sleep(0.8)
                
                # On last step, call the API
                if i == (3 if not st.session_state.full_validation else 4):
                    try:
                        response = requests.post(
                            "http://localhost:5000/validate",
                            json={"json_str": st.session_state.original_json},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.validation_result = result
                            status.update(label="✅ Validation complete!", state="complete")
                        else:
                            st.error(f"Error: {response.text}")
                            status.update(label="❌ Validation failed", state="error")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        status.update(label="❌ Validation failed", state="error")
            
            st.session_state.processing = False
            st.rerun()
    
    # Display results
    if st.session_state.validation_result:
        result = st.session_state.validation_result
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Validation Report", "Corrected JSON", "Raw Output"])
        
        with tab1:
            # Validation status
            if result.get("validation_result", {}).get("valid"):
                st.markdown(f"""
                <div class="card success-card">
                    <h3>✅ Validation Successful</h3>
                    <p>{result["validation_result"].get("message", "JSON is valid")}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card error-card">
                    <h3>❌ Validation Failed</h3>
                    <p>{result["validation_result"].get("message", "JSON contains errors")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Error report
            if result.get("error_report"):
                try:
                    errors = json.loads(result["error_report"])
                    if errors:
                        st.subheader("🚨 Error Details")
                        
                        for error in errors:
                            error_type = error.get("type", "unknown")
                            st.markdown(f"""
                            <div class="card {'error-card' if error_type != 'info' else ''}">
                                <h4>
                                    <span class="tag {'syntax-error' if error_type == 'syntax' else 'schema-error'}">
                                        {error_type.upper()}
                                    </span>
                                    {error.get("path", "")}
                                </h4>
                                <p><strong>Message:</strong> {error.get("message", "No message")}</p>
                                <p><strong>Location:</strong> Line {error.get("line", "N/A")}, Column {error.get("column", "N/A")}</p>
                                {f'<p><strong>Suggested Fix:</strong> {error.get("suggested_fix", "")}</p>' if error.get("suggested_fix") else ""}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No errors found in JSON")
                except:
                    st.warning("Could not parse error report")
        
        with tab2:
            if result.get("corrected_json"):
                try:
                    # Format JSON with syntax highlighting
                    formatted_json = json.dumps(json.loads(result["corrected_json"]), indent=2)
                    st.subheader("✨ Corrected JSON")
                    
                    # Create HTML with syntax highlighting
                    formatter = HtmlFormatter(style="colorful")
                    highlighted = highlight(formatted_json, JsonLexer(), formatter)
                    
                    # Display with scrollable container
                    st.markdown(f"""
                    <div class="json-container">
                        {highlighted}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add download button
                    st.download_button(
                        label="Download Corrected JSON",
                        data=formatted_json,
                        file_name="corrected.json",
                        mime="application/json"
                    )
                except:
                    st.warning("Corrected JSON is not valid")
            else:
                st.info("No corrected JSON available")
        
        with tab3:
            st.subheader("📋 Raw Validation Output")
            st.json(result)
    
    # Example section when no validation run
    if not st.session_state.validation_result and not st.session_state.processing:
        st.info("💡 Enter JSON and click 'Analyze & Correct' to validate and fix your JSON")
        
        with st.expander("Example JSON", expanded=True):
            st.code("""{
  "name": "John",
  "age": 30
  "city": "New York"
}""", language="json")
            st.caption("Try this example to see syntax error detection")

# Footer
st.divider()
st.caption("© 2024 JSON Validation System | Powered by CrewAI and Gemini 1.5 Flash")