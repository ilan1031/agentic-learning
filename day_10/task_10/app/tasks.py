from crewai import Task
from app.data import get_traffic_data

def create_analysis_task(agent, locations):
	"""Create traffic analysis task"""
	location_str = ", ".join(locations)
	return Task(
		description=(
			f"Conduct a comprehensive traffic analysis for the following locations: {location_str}. "
			"Identify current congestion levels, peak traffic times, and key bottlenecks. "
			"Consider factors like road capacity, traffic volume, and existing infrastructure."
		),
		expected_output=(
			"A detailed traffic analysis report in Markdown format with sections: "
			"1. Overall congestion assessment "
			"2. Location-specific bottlenecks "
			"3. Peak traffic patterns "
			"4. Primary causes of congestion"
		),
		agent=agent,
		context=[],
		output_file="analysis_report.md"
	)

def create_strategy_task(agent, locations, context):
	"""Create traffic strategy task"""
	location_str = ", ".join(locations)
	return Task(
		description=(
			f"Develop innovative traffic optimization strategies for: {location_str}. "
			"Based on the traffic analysis report, propose solutions to improve flow and reduce congestion. "
			"Consider options like traffic signal optimization, lane reconfiguration, public transit enhancements, "
			"and smart traffic management technologies."
		),
		expected_output=(
			"A comprehensive strategy proposal in Markdown format with sections: "
			"1. Key findings summary "
			"2. Proposed solutions for each location "
			"3. Implementation roadmap "
			"4. Expected outcomes and benefits"
		),
		agent=agent,
		context=context,
		output_file="strategy_proposal.md"
	)

