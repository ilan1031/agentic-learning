from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def create_research_agent():
    """Create Research Agent"""
    return Agent(
        role="Academic Research Specialist",
        goal="Find and retrieve relevant academic sources for research topics",
        backstory=(
            "You are an expert researcher with extensive experience in academic literature search. "
            "You specialize in finding high-quality peer-reviewed sources from reputable databases."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=False
    )

def create_analysis_agent():
    """Create Analysis Agent"""
    return Agent(
        role="Research Analyst",
        goal="Analyze and extract key information from academic sources",
        backstory=(
            "You are a skilled analyst with a PhD in research methodology. "
            "You excel at critically evaluating academic papers and extracting key findings."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=False
    )

def create_writing_agent():
    """Create Writing Agent"""
    return Agent(
        role="Academic Writer",
        goal="Synthesize research findings into structured literature reviews",
        backstory=(
            "You are an experienced academic writer with numerous publications in top journals. "
            "You specialize in creating well-structured, formal academic content."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=False
    )