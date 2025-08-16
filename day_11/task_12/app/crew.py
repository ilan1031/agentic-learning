from crewai import Crew
from app.agents import create_research_agent, create_analysis_agent, create_writing_agent
from app.tasks import create_research_task, create_analysis_task, create_writing_task
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_research_crew(topic):
    """Create and run research crew"""
    # Create agents
    research_agent = create_research_agent()
    analysis_agent = create_analysis_agent()
    writing_agent = create_writing_agent()
    
    # Create tasks
    research_task = create_research_task(research_agent, topic)
    analysis_task = create_analysis_task(analysis_agent, [research_task])
    writing_task = create_writing_task(writing_agent, [analysis_task])
    
    # Create crew
    crew = Crew(
        agents=[research_agent, analysis_agent, writing_agent],
        tasks=[research_task, analysis_task, writing_task],
        verbose=2
    )
    
    # Execute tasks
    result = crew.kickoff()
    return {
        "research": research_task.output.raw_output,
        "analysis": analysis_task.output.raw_output,
        "literature_review": writing_task.output.raw_output
    }