import os
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_search_tool import web_search
from tools.custom_research_tool import ResearchTool
from tools.vector_store_tool import VectorSearchTool

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# For testing, let's use a mock LLM if no API key is available
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.3,
        api_key=api_key
    )
else:
    # Fallback to a simple mock LLM for testing
    from langchain.llms.base import LLM
    class MockLLM(LLM):
        def _call(self, prompt, stop=None):
            return "This is a mock response. Please set your GOOGLE_API_KEY in .env file."
        
        @property
        def _llm_type(self):
            return "mock"
    
    llm = MockLLM()

TOOLS = [
    Tool(name="Web Search", func=web_search, description="Useful for web info"),
    Tool(name="Research DB", func=ResearchTool().run, description="Search research context"),
    Tool(name="Vector Search", func=VectorSearchTool().run, description="Recall saved memory")
]

agent = initialize_agent(TOOLS, llm, agent="zero-shot-react-description", verbose=True)

def run_agent(prompt):
    return agent.run(prompt)
