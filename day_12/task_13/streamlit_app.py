import streamlit as st
from app.math_solver import math_solver
import os
import time
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Math Problem Solver",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-section {
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
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
    .problem-card {
        border-left: 5px solid #2196F3;
    }
    .solution-card {
        border-left: 5px solid #4CAF50;
    }
    .explanation-card {
        border-left: 5px solid #FF9800;
    }
    .validation-card {
        border-left: 5px solid #9C27B0;
    }
    .examples-card {
        border-left: 5px solid #F44336;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2E7D32;
        color: white;
    }
    .math-expression {
        font-family: "Times New Roman", serif;
        font-size: 1.2em;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin: 5px 0;
    }
    .step-container {
        padding: 10px;
        margin: 8px 0;
        border-left: 3px solid #2196F3;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "problem" not in st.session_state:
    st.session_state.problem = ""
if "results" not in st.session_state:
    st.session_state.results = None
if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("""
<div class="header-section">
    <h1 style="color:white; margin:0;">🧮 Math Problem Solver</h1>
    <p style="color:white; margin:0;">AI-powered math solution with Autogen multi-agent system</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

# Sidebar - Math categories
with col1:
    st.sidebar.title("📚 Math Categories")
    math_categories = [
        "Algebra",
        "Calculus",
        "Geometry",
        "Statistics",
        "Trigonometry",
        "Linear Algebra",
        "Differential Equations"
    ]
    selected_category = st.sidebar.selectbox("Select Category", math_categories)
    
    st.sidebar.divider()
    st.sidebar.title("⚙️ Options")
    show_steps = st.sidebar.checkbox("Show Detailed Steps", True)
    generate_examples = st.sidebar.checkbox("Generate Practice Examples", True)
    validate_solution = st.sidebar.checkbox("Validate Solution", True)
    
    st.sidebar.divider()
    st.sidebar.title("📊 Difficulty")
    difficulty = st.sidebar.slider("Problem Difficulty", 1, 5, 3)
    
    st.sidebar.divider()
    if st.sidebar.button("Clear All", type="secondary"):
        st.session_state.problem = ""
        st.session_state.results = None
        st.rerun()

# Main content
with col2:
    # Problem input
    st.subheader("📝 Enter Math Problem")
    problem = st.text_area(
        "Describe or write your math problem:",
        placeholder="Example: 'Solve for x: 2x + 5 = 15' or 'Find the derivative of x^2 + 3x + 2'",
        value=st.session_state.problem,
        height=120,
        key="problem_input"
    )
    st.session_state.problem = problem
    
    # Example problems
    st.write("Try these examples:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Linear Equation", use_container_width=True):
            st.session_state.problem = "Solve for x: 3x - 7 = 8"
            st.rerun()
    with col2:
        if st.button("Quadratic Equation", use_container_width=True):
            st.session_state.problem = "Solve x^2 - 5x + 6 = 0"
            st.rerun()
    with col3:
        if st.button("Calculus Problem", use_container_width=True):
            st.session_state.problem = "Find the derivative of f(x) = 3x^4 - 2x^3 + 5x - 7"
            st.rerun()
    
    # Action button
    if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
        if not problem.strip():
            st.warning("Please enter a math problem")
        else:
            st.session_state.processing = True
            st.rerun()
    
    # Processing state
    if st.session_state.processing:
        with st.status("🤖 Solving problem...", expanded=True) as status:
            steps = [
                "Parsing problem structure...",
                "Identifying solution approach...",
                "Calculating solution...",
                "Generating explanation...",
                "Validating results..."
            ]
            
            for step in steps:
                st.write(step)
                time.sleep(2)
            
            try:
                # Execute math solver
                results = math_solver.solve_problem(problem)
                st.session_state.results = results
                status.update(label="✅ Solution complete!", state="complete")
            except Exception as e:
                logger.error(f"Problem solving failed: {str(e)}")
                st.error(f"Error: {str(e)}")
                status.update(label="❌ Solving failed", state="error")
            
            st.session_state.processing = False
            st.rerun()
    
    # Display results
    if st.session_state.results:
        results = st.session_state.results
        
        # Problem overview
        st.subheader("📋 Problem Overview")
        st.markdown(f'<div class="card problem-card">{results.get("problem", "")}</div>', unsafe_allow_html=True)
        
        # Parsed problem
        if results.get("parsed_problem"):
            st.subheader("🔍 Parsed Problem")
            st.json(results["parsed_problem"])
        
        # Solution
        if results.get("solution"):
            st.subheader("✅ Solution")
            solution = results["solution"]
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Final Answer:**")
                st.markdown(f'<div class="math-expression">{solution.get("solution", "")}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Method:**")
                st.info(solution.get("method", ""))
            
            # Steps
            if show_steps and solution.get("steps"):
                st.subheader("📝 Step-by-Step Solution")
                for i, step in enumerate(solution.get("steps", []), 1):
                    st.markdown(f'<div class="step-container"><strong>Step {i}:</strong> {step}</div>', unsafe_allow_html=True)
        
        # Explanation
        if results.get("explanation") and results["explanation"].get("explanation"):
            st.subheader("💡 Explanation")
            explanation = results["explanation"]
            
            for item in explanation.get("explanation", []):
                st.markdown(f"**Step {item.get('step', '')}:** {item.get('description', '')}")
                st.info(f"Reasoning: {item.get('reasoning', '')}")
            
            if explanation.get("key_concepts"):
                st.markdown("**Key Concepts:**")
                for concept in explanation.get("key_concepts", []):
                    st.markdown(f"- {concept}")
        
        # Validation
        if validate_solution and results.get("validation"):
            st.subheader("✓ Validation")
            validation = results["validation"]
            
            col1, col2 = st.columns(2)
            with col1:
                if validation.get("is_valid", False):
                    st.success("✅ Solution is valid")
                else:
                    st.error("❌ Solution is invalid")
            
            with col2:
                st.markdown(f"**Method:** {validation.get('validation_method', '')}")
                st.markdown(f"**Confidence:** {validation.get('confidence', '')}")
            
            if validation.get("details"):
                st.info(validation.get("details"))
        
        # Examples
        if generate_examples and results.get("examples"):
            st.subheader("📚 Practice Examples")
            for i, example in enumerate(results.get("examples", []), 1):
                with st.expander(f"Example {i}: {example.get('problem', '')}"):
                    st.markdown(f"**Problem:** {example.get('problem', '')}")
                    st.markdown(f"**Solution:** {example.get('solution', '')}")
                    st.markdown(f"**Explanation:** {example.get('explanation', '')}")
    
    # Initial state with no problem solved
    if not st.session_state.results and not st.session_state.processing:
        st.info("💡 Enter a math problem and click 'Solve Problem' to get started")
        
        with st.expander("How It Works", expanded=True):
            st.markdown("""
            **Multi-Agent Process:**
            1. **Problem Parser**: Analyzes and structures your math problem
            2. **Solver Agent**: Computes the solution step-by-step
            3. **Explanation Agent**: Provides detailed reasoning for each step
            4. **Validator Agent**: Verifies the solution is correct
            5. **Example Agent**: Generates practice problems for learning
            
            **Supported Math Areas:**
            - Algebra (equations, inequalities, expressions)
            - Calculus (derivatives, integrals, limits)
            - Geometry (shapes, angles, measurements)
            - Statistics (probability, distributions)
            - And more!
            """)

# Footer
st.divider()
st.caption("© 2024 Math Problem Solver | Powered by Autogen and Gemini 1.5")