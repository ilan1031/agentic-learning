
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_search_tool import web_search
from tools.custom_research_tool import ResearchTool
from tools.vector_store_tool import VectorSearchTool
from tools.niche_filter_tool import niche_filter

# Load environment variables from .env
load_dotenv()

# Prefer GEMINI_API_KEY, fallback to GOOGLE_API_KEY
_google_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not _google_api_key:
    raise EnvironmentError(
        "Missing API key: set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file."
    )

# Ensure both env names are populated for underlying libs
os.environ["GOOGLE_API_KEY"] = _google_api_key
os.environ["GEMINI_API_KEY"] = _google_api_key

# Use LangChain's Gemini integration with explicit API key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=_google_api_key,
)

_vector_tool = VectorSearchTool()

def _save_ideas(input: str) -> str:
    # expects JSON array like [{"id":"..","text":"..","meta":{...}}]
    import json
    try:
        ideas = json.loads(input)
        return _vector_tool.save(ideas)
    except Exception as e:
        return f"save_ideas error: {e}"

TOOLS = [
    Tool(name="Web Search", func=web_search, description="Useful for web info"),
    Tool(name="Niche Filter", func=niche_filter, description="Filter and score ideas by niche"),
    Tool(name="Save Ideas", func=_save_ideas, description="Persist ideas with metadata to vector store"),
    Tool(name="Vector Search", func=_vector_tool.run, description="Recall saved memory"),
    Tool(name="Research DB", func=ResearchTool().run, description="Search research context"),
]

agent = initialize_agent(TOOLS, llm, agent="zero-shot-react-description", verbose=True)

def run_agent(prompt):
    return agent.run(prompt)
