import streamlit as st
from app.event_planner import event_planner
import os
import time
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import json

# Load environment variables
load_dotenv()

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Event Planning Coordinator",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-section {
        background: linear-gradient(135deg, #9C27B0, #673AB7);
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
    .task-card {
        border-left: 5px solid #4CAF50;
    }
    .progress-card {
        border-left: 5px solid #2196F3;
    }
    .timeline-card {
        border-left: 5px solid #FF9800;
    }
    .stButton>button {
        background-color: #673AB7;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #512DA8;
        color: white;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin: 3px;
    }
    .status-completed {
        background-color: #4CAF50;
        color: white;
    }
    .status-pending {
        background-color: #F44336;
        color: white;
    }
    .status-in-progress {
        background-color: #FFC107;
        color: black;
    }
    .category-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin: 3px;
        background-color: #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "event_details" not in st.session_state:
    st.session_state.event_details = ""
if "results" not in st.session_state:
    st.session_state.results = None
if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("""
<div class="header-section">
    <h1 style="color:white; margin:0;">🎉 Event Planning Coordinator</h1>
    <p style="color:white; margin:0;">AI-powered event planning with Autogen multi-agent system</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

# Sidebar - Event types
with col1:
    st.sidebar.title("🎯 Event Types")
    event_types = [
        "Corporate Seminar",
        "Wedding",
        "Conference",
        "Birthday Party",
        "Product Launch",
        "Networking Event"
    ]
    selected_event_type = st.sidebar.selectbox("Select Event Type", event_types)
    
    st.sidebar.divider()
    st.sidebar.title("⚙️ Planning Options")
    budget_range = st.sidebar.slider("Budget Range ($)", 1000, 50000, (5000, 15000))
    priority_focus = st.sidebar.multiselect(
        "Priority Focus", 
        ["Venue", "Catering", "Entertainment", "Decorations", "Marketing"],
        default=["Venue", "Catering"]
    )
    
    st.sidebar.divider()
    st.sidebar.title("📅 Timeline")
    event_date = st.sidebar.date_input("Event Date")
    planning_deadline = st.sidebar.date_input("Planning Deadline", event_date)
    
    st.sidebar.divider()
    if st.sidebar.button("Clear All", type="secondary"):
        st.session_state.event_details = ""
        st.session_state.results = None
        st.rerun()

# Main content
with col2:
    # Event details input
    st.subheader("📝 Event Details")
    event_details = st.text_area(
        "Describe your event:",
        placeholder="Example: 'Plan a corporate seminar for 100 people in Bangalore with catering and keynote speakers by October'",
        value=st.session_state.event_details,
        height=150,
        key="event_input"
    )
    st.session_state.event_details = event_details
    
    # Action button
    if st.button("🚀 Plan My Event", type="primary", use_container_width=True):
        if not event_details.strip():
            st.warning("Please enter event details")
        else:
            st.session_state.processing = True
            st.rerun()
    
    # Processing state
    if st.session_state.processing:
        with st.status("🤖 Coordinating event planning...", expanded=True) as status:
            steps = [
                "Initializing planning agents...",
                "Processing event details...",
                "Creating task breakdown...",
                "Developing timeline...",
                "Generating progress report..."
            ]
            
            for step in steps:
                st.write(step)
                time.sleep(2)
            
            try:
                # Execute event planning
                results = event_planner.plan_event(event_details)
                st.session_state.results = results
                status.update(label="✅ Event planning complete!", state="complete")
            except Exception as e:
                logger.error(f"Event planning failed: {str(e)}")
                st.error(f"Error: {str(e)}")
                status.update(label="❌ Planning failed", state="error")
            
            st.session_state.processing = False
            st.rerun()
    
    # Display results
    if st.session_state.results:
        results = st.session_state.results
        
        # Event overview
        st.subheader("📋 Event Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Event Type", results["event_details"].get("event_type", "Unknown"))
        col2.metric("Location", results["event_details"].get("location", "Unknown"))
        col3.metric("Attendees", results["event_details"].get("attendees", 0))
        col4.metric("Date", results["event_details"].get("date", "TBD"))
        
        # Task list
        st.subheader("📋 Task Breakdown")
        if results.get("task_list"):
            df_tasks = pd.DataFrame(results["task_list"])
            
            # Add status badges
            df_tasks["status_badge"] = df_tasks["status"].apply(
                lambda s: f'<span class="status-badge status-{"completed" if s=="completed" else "in-progress" if s=="in progress" else "pending"}">{s}</span>'
            )
            
            # Add category tags
            df_tasks["category_tag"] = df_tasks["category"].apply(
                lambda c: f'<span class="category-tag">{c}</span>'
            )
            
            # Display as HTML table
            st.markdown(df_tasks[["name", "category_tag", "deadline", "status_badge"]].to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No tasks generated")
        
        # Progress report
        st.subheader("📈 Progress Report")
        if results.get("progress_report"):
            st.markdown(f'<div class="card progress-card">{results["progress_report"]}</div>', unsafe_allow_html=True)
        else:
            st.info("No progress report available")
        
        # Timeline visualization
        st.subheader("⏱️ Event Timeline")
        if results.get("timeline"):
            timeline_df = pd.DataFrame(results["timeline"])
            
            # Create Gantt chart
            fig = px.timeline(
                timeline_df,
                x_start="deadline",
                x_end="deadline",
                y="task",
                color="category",
                title="Event Planning Timeline",
                labels={"task": "Task", "deadline": "Deadline", "category": "Category"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            # Update layout
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(
                height=500,
                xaxis_title="Deadline",
                yaxis_title="Task",
                legend_title="Category",
                hovermode="closest"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No timeline available")
    
    # Initial state with no event planned
    if not st.session_state.results and not st.session_state.processing:
        st.info("💡 Enter event details and click 'Plan My Event' to get started")
        
        with st.expander("Example Events", expanded=True):
            st.markdown("""
            **Try these examples:**
            - "Plan a wedding for 200 guests in Chennai with catering, music, and decorations by September 2025"
            - "Organize a corporate seminar for 100 people in Bangalore with catering and keynote speakers by October"
            - "Coordinate a product launch event for 150 attendees in Mumbai with AV setup and press coverage in November"
            """)
            
            st.markdown("""
            **How It Works:**
            1. **Event Processing Agent**: Breaks down your event into tasks
            2. **Progress Summarization Agent**: Tracks progress and generates reports
            3. **Autogen Group Chat**: Coordinates multi-agent collaboration
            """)

# Footer
st.divider()
st.caption("© 2024 Event Planning Coordinator | Powered by Autogen and Gemini 1.5 Flash")