import streamlit as st
from app.crew import create_research_crew
import os
import time
from dotenv import load_dotenv
import logging
import markdown
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Academic Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-section {
        background: linear-gradient(135deg, #1a2a6c, #2c3e50);
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
    .research-card {
        border-left: 5px solid #3498db;
    }
    .analysis-card {
        border-left: 5px solid #2ecc71;
    }
    .writing-card {
        border-left: 5px solid #9b59b6;
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
    .tab-container {
        padding: 15px;
        border: 1px solid #e3e6f0;
        border-radius: 8px;
        margin-top: 10px;
    }
    .source-item {
        padding: 10px;
        margin: 8px 0;
        border-left: 3px solid #3498db;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    .stTextArea textarea {
        min-height: 120px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "results" not in st.session_state:
    st.session_state.results = None
if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("""
<div class="header-section">
    <h1 style="color:white; margin:0;">📚 Academic Research Assistant</h1>
    <p style="color:white; margin:0;">AI-powered literature review generation with CrewAI</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

# Sidebar - Research parameters
with col1:
    st.sidebar.title("🔍 Research Parameters")
    
    research_fields = [
        "Computer Science", "Medicine", "Engineering", 
        "Social Sciences", "Business", "Education"
    ]
    selected_field = st.sidebar.selectbox("Research Field", research_fields)
    
    source_types = st.sidebar.multiselect(
        "Source Types",
        ["Journal Articles", "Conference Papers", "Books", "Theses"],
        default=["Journal Articles", "Conference Papers"]
    )
    
    publication_range = st.sidebar.slider(
        "Publication Year Range",
        1990, 2025, (2015, 2023)
    )
    
    st.sidebar.divider()
    
    st.sidebar.title("⚙️ Options")
    include_citations = st.sidebar.checkbox("Include Citations", True)
    include_abstracts = st.sidebar.checkbox("Include Abstracts", True)
    
    st.sidebar.divider()
    
    if st.sidebar.button("Run Research", type="primary", use_container_width=True):
        if not st.session_state.topic.strip():
            st.warning("Please enter a research topic")
        else:
            st.session_state.processing = True
            st.rerun()

# Main content
with col2:
    # Research topic input
    st.subheader("🔬 Research Topic")
    topic = st.text_area(
        "Enter your research topic:",
        placeholder="Example: 'Impact of AI on education outcomes'",
        key="topic_input",
        height=120
    )
    st.session_state.topic = topic
    
    # Example topics
    st.write("Try these examples:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("AI in Healthcare", use_container_width=True):
            st.session_state.topic = "Applications of artificial intelligence in healthcare diagnostics"
            st.rerun()
    with col2:
        if st.button("Climate Policy", use_container_width=True):
            st.session_state.topic = "Effectiveness of carbon pricing policies in reducing emissions"
            st.rerun()
    with col3:
        if st.button("Remote Learning", use_container_width=True):
            st.session_state.topic = "Impact of remote learning on student engagement and outcomes"
            st.rerun()
    
    # Processing state
    if st.session_state.processing:
        with st.status("🔍 Conducting research...", expanded=True) as status:
            steps = [
                "Gathering academic sources...",
                "Analyzing research findings...",
                "Synthesizing literature review...",
                "Formatting references..."
            ]
            
            for step in steps:
                st.write(step)
                time.sleep(2)
            
            try:
                # Execute crew
                result = create_research_crew(st.session_state.topic)
                st.session_state.results = result
                status.update(label="✅ Research complete!", state="complete")
            except Exception as e:
                logger.error(f"Research failed: {str(e)}")
                st.error(f"Error: {str(e)}")
                status.update(label="❌ Research failed", state="error")
            
            st.session_state.processing = False
            st.rerun()
    
    # Display results
    if st.session_state.results:
        results = st.session_state.results
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Literature Review", "Research Sources", "Analysis"])
        
        with tab1:
            st.subheader("📝 Literature Review")
            if results.get("literature_review"):
                st.markdown(f'<div class="card writing-card">{results["literature_review"]}</div>', 
                            unsafe_allow_html=True)
                
                # Add download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download as Markdown",
                        data=results["literature_review"],
                        file_name="literature_review.md",
                        mime="text/markdown"
                    )
                with col2:
                    st.download_button(
                        label="Download as PDF",
                        data=results["literature_review"],
                        file_name="literature_review.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("No literature review generated")
        
        with tab2:
            st.subheader("🔍 Research Sources")
            if results.get("research"):
                # Parse sources (simple parsing for demonstration)
                sources = results["research"].split("\n\n")
                for source in sources[:10]:  # Show up to 10 sources
                    st.markdown(f'<div class="source-item">{source}</div>', 
                                unsafe_allow_html=True)
            else:
                st.info("No research sources found")
        
        with tab3:
            st.subheader("📊 Research Analysis")
            if results.get("analysis"):
                st.markdown(f'<div class="card analysis-card">{results["analysis"]}</div>', 
                            unsafe_allow_html=True)
            else:
                st.info("No analysis available")
    
    # Initial state with no research
    if not st.session_state.results and not st.session_state.processing:
        st.info("💡 Enter a research topic and click 'Run Research' to get started")
        
        with st.expander("How It Works", expanded=True):
            st.markdown("""
            **Research Process:**
            1. **Research Agent**: Finds relevant academic sources
            2. **Analysis Agent**: Extracts key findings and insights
            3. **Writing Agent**: Synthesizes a structured literature review
            
            **Features:**
            - Peer-reviewed academic sources
            - Formal academic writing style
            - Complete references with citations
            - Customizable research parameters
            """)

# Footer
st.divider()
st.caption("© 2024 Academic Research Assistant | Powered by CrewAI and Gemini 1.5 Flash")