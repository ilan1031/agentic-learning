import random
from typing import Dict, List

# Mock traffic data for road segments
ROAD_SEGMENTS = {
	"MG Road": {
		"length": 5.2,  # km
		"lanes": 4,
		"speed_limit": 60,  # km/h
		"daily_traffic": 45000,
		"congestion_level": random.choice(["low", "moderate", "high"])
	},
	"Brigade Road": {
		"length": 1.8,
		"lanes": 2,
		"speed_limit": 40,
		"daily_traffic": 38000,
		"congestion_level": random.choice(["low", "moderate", "high"])
	},
	"Anna Salai": {
		"length": 8.5,
		"lanes": 6,
		"speed_limit": 70,
		"daily_traffic": 65000,
		"congestion_level": random.choice(["low", "moderate", "high"])
	},
	"Mount Road": {
		"length": 3.2,
		"lanes": 4,
		"speed_limit": 50,
		"daily_traffic": 42000,
		"congestion_level": random.choice(["low", "moderate", "high"])
	},
	"T Nagar": {
		"length": 2.7,
		"lanes": 2,
		"speed_limit": 30,
		"daily_traffic": 52000,
		"congestion_level": random.choice(["low", "moderate", "high"])
	}
}

def get_traffic_data(locations: List[str]) -> Dict[str, dict]:
	"""Retrieve traffic data for specified locations"""
	return {loc: ROAD_SEGMENTS[loc] for loc in locations if loc in ROAD_SEGMENTS}

def get_all_locations() -> List[str]:
	"""Get all available road segments"""
	return list(ROAD_SEGMENTS.keys())

