import streamlit as st
from agent_py.agent import run_agent
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Check for required API keys
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY not found in environment variables")
if not os.getenv("TAVILY_API_KEY"):
    st.error("TAVILY_API_KEY not found in environment variables")

# Configure Streamlit page
st.set_page_config(
    page_title="Academic Literature Review Generator",
    page_icon="📚",
    layout="centered"
)

# UI Elements
st.title("📚 Academic Literature Review Generator")
st.markdown("Generate comprehensive literature reviews using AI-powered academic research")

with st.form("research_form"):
    topic = st.text_area(
        "Research Topic:", 
        placeholder="Enter your research topic or question...",
        height=150
    )
    
    options = st.columns(3)
    with options[0]:
        style = st.selectbox("Citation Style", ["APA", "MLA", "Chicago"])
    with options[1]:
        depth = st.select_slider("Research Depth", ["Brief", "Standard", "Comprehensive"], "Standard")
    with options[2]:
        sources = st.slider("Number of Sources", 5, 20, 10)
    
    submitted = st.form_submit_button("Generate Literature Review")

# Handle form submission
if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Show progress
            status_text.text("🔍 Searching academic sources...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            # Execute agent
            status_text.text("🔍 Filtering academic sources...")
            progress_bar.progress(40)
            time.sleep(0.5)
            
            status_text.text("📝 Generating literature review...")
            progress_bar.progress(70)
            
            report = run_agent(topic)
            
            # Show completion
            progress_bar.progress(100)
            status_text.text("✅ Literature review generated!")
            time.sleep(0.5)
            status_text.empty()
            
            # Display results
            st.success("Literature Review Generated!")
            st.markdown("---")
            st.subheader("Research Report")
            st.markdown(report)
            
            # Add download button
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"literature_review_{topic[:20]}.md".replace(" ", "_"),
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")

# Sidebar with additional info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This AI-powered tool generates comprehensive academic literature reviews by:
    
    - Searching peer-reviewed sources
    - Filtering credible academic publications
    - Structuring findings with proper citations
    
    Powered by:
    - Gemini 1.5 Flash
    - LangGraph Agent
    - Tavily Research API
    """)
    st.markdown("---")
    st.caption("Set API keys in .env file")