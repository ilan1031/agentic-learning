import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Initialize Gemini 1.5 Flash via LangChain's Google GenAI chat model
_google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
	model="gemini-1.5-flash",
	temperature=0.3,
	google_api_key=_google_api_key
)

def create_traffic_analyst():
	"""Create Traffic Analyst Agent"""
	return Agent(
		role="Senior Traffic Analyst",
		goal="Identify traffic bottlenecks and congestion patterns in urban areas",
		backstory=(
			"You are an expert in urban traffic analysis with over 10 years of experience "
			"in identifying congestion patterns and traffic flow inefficiencies. "
			"You specialize in analyzing traffic data to pinpoint problem areas in city road networks."
		),
		verbose=True,
		llm=llm,
		allow_delegation=False
	)

def create_traffic_strategist():
	"""Create Traffic Strategist Agent"""
	return Agent(
		role="Urban Traffic Strategist",
		goal="Develop effective strategies to optimize traffic flow and reduce congestion",
		backstory=(
			"You are a renowned urban planner specializing in traffic optimization strategies. "
			"With a background in civil engineering and smart city planning, you create innovative "
			"solutions to improve traffic flow based on analytical findings."
		),
		verbose=True,
		llm=llm,
		allow_delegation=False
	)

