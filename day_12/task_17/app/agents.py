import autogen
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

def create_event_processing_agent():
    """Create Event Processing Agent"""
    config = {
        "name": "Event_Processor",
        "system_message": (
            "You are an Event Processing Agent. Your responsibilities include:\n"
            "1. Parse event details from user input\n"
            "2. Break down event into categorized tasks (Venue, Catering, Entertainment, Décor, Invitations, etc.)\n"
            "3. Assign deadlines and dependencies between tasks\n"
            "4. Identify required resources\n"
            "5. Output structured task list with deadlines"
        ),
        "llm_config": {
            "config_list": [{"model": "gemini-1.5-flash"}],
            "temperature": 0.3
        }
    }
    return autogen.AssistantAgent(**config)

def create_progress_summarization_agent():
    """Create Progress Summarization Agent"""
    config = {
        "name": "Progress_Summarizer",
        "system_message": (
            "You are a Progress Summarization Agent. Your responsibilities include:\n"
            "1. Track task completion status\n"
            "2. Generate progress reports with status indicators (✅ completed, ❌ pending, ⚡ in progress)\n"
            "3. Identify bottlenecks and risks\n"
            "4. Provide recommendations for task prioritization\n"
            "5. Output clear progress summaries"
        ),
        "llm_config": {
            "config_list": [{"model": "gemini-1.5-flash"}],
            "temperature": 0.3
        }
    }
    return autogen.AssistantAgent(**config)

def create_user_proxy_agent():
    """Create User Proxy Agent"""
    config = {
        "name": "User_Proxy",
        "human_input_mode": "NEVER",
        "code_execution_config": False,
        "is_termination_msg": lambda x: "TERMINATE" in x.get("content", ""),
        "system_message": "You are the User Proxy Agent. Your role is to initiate conversations and manage communication with the user."
    }
    return autogen.UserProxyAgent(**config)