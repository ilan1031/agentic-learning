import os
from typing import Dict
from crewai import Crew
from app.agents import create_traffic_analyst, create_traffic_strategist
from app.tasks import create_analysis_task, create_strategy_task

def _read_file_safely(path: str) -> str:
	if not os.path.exists(path):
		return ""
	try:
		with open(path, "r", encoding="utf-8") as f:
			return f.read()
	except Exception:
		return ""

def create_traffic_crew(locations) -> Dict[str, str]:
	"""Create and run traffic management crew"""
	# Create agents
	analyst = create_traffic_analyst()
	strategist = create_traffic_strategist()

	# Create tasks
	analysis_task = create_analysis_task(analyst, locations)
	strategy_task = create_strategy_task(strategist, locations, [analysis_task])

	# Create crew
	crew = Crew(
		agents=[analyst, strategist],
		tasks=[analysis_task, strategy_task],
		verbose=2
	)

	# Execute tasks
	crew.kickoff()

	# Prefer reading from output files if produced by Crew
	analysis_text = _read_file_safely("analysis_report.md")
	strategy_text = _read_file_safely("strategy_proposal.md")

	# Fallback to in-memory outputs if available
	if not analysis_text:
		analysis_text = getattr(getattr(analysis_task, "output", None), "raw_output", "") or ""
	if not strategy_text:
		strategy_text = getattr(getattr(strategy_task, "output", None), "raw_output", "") or ""

	return {
		"analysis": analysis_text,
		"strategy": strategy_text
	}

