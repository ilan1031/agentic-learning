from crewai import Task
import os
import logging
from tavily import TavilyClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Tavily client
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

def create_research_task(agent, topic):
    """Create research task"""
    return Task(
        description=f"Conduct academic research on: {topic}",
        expected_output=(
            "A list of 5-10 high-quality academic sources (peer-reviewed journals, conference papers) "
            "with titles, authors, and URLs. Include a brief summary of each source's relevance."
        ),
        agent=agent,
        async_execution=False
    )

def create_analysis_task(agent, context):
    """Create analysis task"""
    return Task(
        description="Analyze the collected academic sources",
        expected_output=(
            "A structured analysis of key findings from the sources, including:\n"
            "- Main arguments and conclusions\n"
            "- Methodologies used\n"
            "- Gaps in the research\n"
            "- Connections between different studies"
        ),
        agent=agent,
        context=context,
        async_execution=False
    )

def create_writing_task(agent, context):
    """Create writing task"""
    return Task(
        description="Write a structured literature review",
        expected_output=(
            "A comprehensive literature review in Markdown format with sections:\n"
            "1. Introduction\n"
            "2. Background\n"
            "3. Key Findings\n"
            "4. Critical Analysis\n"
            "5. Conclusion\n"
            "6. References\n"
            "Formal academic writing style with proper citations."
        ),
        agent=agent,
        context=context,
        output_file="literature_review.md"
    )