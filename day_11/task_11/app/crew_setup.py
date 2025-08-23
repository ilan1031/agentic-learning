from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from app.json_validator_tool import JSONValidatorTool
import os
import logging
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Create validator instance
validator = JSONValidatorTool()

# Create proper CrewAI tool wrapper
@tool("JSON Validator Tool")
def validate_json_tool(json_str: str) -> Dict:
    """
    Validates JSON syntax and schema. Returns a dictionary with validation results.
    
    Args:
        json_str: The JSON string to validate
        
    Returns:
        Dict with validation results including:
        - valid: boolean indicating if JSON is valid
        - errors: list of error objects
        - message: summary message
    """
    return validator.validate_json(json_str)

def create_manager_agent():
    return Agent(
        role="Validation Manager",
        goal="Oversee the JSON validation process and coordinate between agents",
        backstory=(
            "You are an experienced data validation manager with expertise in coordinating "
            "validation workflows. Your role is to ensure the validation process runs smoothly "
            "and produces accurate results."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=True
    )

def create_analyzer_agent():
    return Agent(
        role="Data Analyzer",
        goal="Identify and report JSON syntax and schema errors",
        backstory=(
            "You are a meticulous data analyst specializing in JSON validation. "
            "You have a keen eye for spotting syntax errors and schema mismatches."
        ),
        tools=[validate_json_tool],  # Use the tool wrapper
        verbose=True,
        llm=llm
    )

def create_corrector_agent():
    return Agent(
        role="Data Corrector",
        goal="Fix JSON errors while preserving data integrity",
        backstory=(
            "You are a skilled data engineer with expertise in correcting JSON files. "
            "You can fix syntax errors and adjust data to match schemas without losing "
            "the original meaning of the data."
        ),
        verbose=True,
        llm=llm
    )

def create_analysis_task(agent, json_str: str):
    return Task(
        description=f"Analyze the following JSON for syntax and schema errors:\n{json_str}",
        expected_output=(
            "A detailed error report in JSON format containing:\n"
            "- Error type (syntax/schema)\n"
            "- Location/path in JSON\n"
            "- Error description\n"
            "- Suggested fix\n"
            "Format: List of error objects"
        ),
        agent=agent,
        output_file="error_report.json"
    )

def create_correction_task(agent, json_str: str, error_report: str):
    return Task(
        description=(
            f"Correct the following JSON based on the error report:\n"
            f"Original JSON:\n{json_str}\n\n"
            f"Error Report:\n{error_report}"
        ),
        expected_output=(
            "The corrected JSON string that passes all validation checks. "
            "Ensure the output is valid JSON and matches the required schema."
        ),
        context=[error_report],
        agent=agent,
        output_file="corrected.json"
    )

def create_validation_crew(json_str: str):
    # Create agents
    manager = create_manager_agent()
    analyzer = create_analyzer_agent()
    corrector = create_corrector_agent()
    
    # Create tasks
    analysis_task = create_analysis_task(analyzer, json_str)
    correction_task = create_correction_task(corrector, json_str, analysis_task)
    
    # Create crew
    crew = Crew(
        agents=[manager, analyzer, corrector],
        tasks=[analysis_task, correction_task],
        verbose=True,
        manager_llm=llm
    )
    
    # Execute validation process
    result = crew.kickoff()
    
    return {
        "original": json_str,
        "error_report": analysis_task.output.raw_output,
        "corrected_json": correction_task.output.raw_output,
        "validation_result": validator.validate_json(correction_task.output.raw_output)
    }