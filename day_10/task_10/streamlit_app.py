import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium

from app.crew import create_traffic_crew
from app.data import get_all_locations, get_traffic_data

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
	page_title="Urban Traffic Management System",
	page_icon="🚦",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
	.header-section {
		background: linear-gradient(135deg, #1a2a6c, #b21f1f, #1a2a6c);
		padding: 25px;
		border-radius: 10px;
		color: white;
		margin-bottom: 25px;
	}
	.card {
		border-radius: 10px;
		padding: 20px;
		margin: 15px 0;
		box-shadow: 0 4px 8px rgba(0,0,0,0.1);
		background-color: #ffffff;
	}
	.traffic-card {
		border-left: 5px solid #3498db;
	}
	.strategy-card {
		border-left: 5px solid #2ecc71;
	}
	.map-card {
		border-left: 5px solid #e74c3c;
	}
	.stButton>button {
		background-color: #3498db;
		color: white;
		font-weight: bold;
		border-radius: 8px;
		padding: 10px 24px;
		width: 100%;
	}
	.stButton>button:hover {
		background-color: #2980b9;
		color: white;
	}
	.tag {
		display: inline-block;
		padding: 4px 12px;
		border-radius: 20px;
		font-size: 0.85em;
		margin: 3px;
	}
	.congestion-low {
		background-color: #2ecc71;
		color: white;
	}
	.congestion-moderate {
		background-color: #f39c12;
		color: white;
	}
	.congestion-high {
		background-color: #e74c3c;
		color: white;
	}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "analysis" not in st.session_state:
	st.session_state.analysis = None
if "strategy" not in st.session_state:
	st.session_state.strategy = None
if "locations" not in st.session_state:
	st.session_state.locations = []
if "traffic_data" not in st.session_state:
	st.session_state.traffic_data = {}

# Header
st.markdown("""
<div class="header-section">
	<h1 style="color:white; margin:0;">🚦 Urban Traffic Management System</h1>
	<p style="color:white; margin:0;">AI-powered traffic analysis and optimization for smarter cities</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

# Sidebar - Location selection
with col1:
	st.sidebar.title("📍 Traffic Analysis Parameters")

	all_locations = get_all_locations()
	selected_locations = st.sidebar.multiselect(
		"Select road segments to analyze:",
		all_locations,
		default=["MG Road", "Brigade Road"]
	)

	st.sidebar.divider()

	st.sidebar.title("⚙️ Analysis Options")
	analysis_depth = st.sidebar.select_slider(
		"Analysis Depth:",
		options=["Quick", "Standard", "Comprehensive"],
		value="Standard"
	)

	time_frame = st.sidebar.radio(
		"Time Frame:",
		["Current", "Peak Hours", "24-hour Cycle"]
	)

	st.sidebar.divider()

	st.sidebar.title("📊 Visualization")
	show_map = st.sidebar.checkbox("Show Traffic Map", True)
	show_stats = st.sidebar.checkbox("Show Traffic Statistics", True)

	st.sidebar.divider()

	if st.sidebar.button("Run Traffic Analysis", type="primary", use_container_width=True):
		if not selected_locations:
			st.warning("Please select at least one road segment")
		else:
			st.session_state.locations = selected_locations
			st.session_state.traffic_data = get_traffic_data(selected_locations)
			st.session_state.processing = True
			st.rerun()

# Main content
with col2:
	# Display traffic data if available
	if st.session_state.traffic_data:
		st.subheader("🚥 Current Traffic Status")

		# Create traffic metrics
		cols = st.columns(len(st.session_state.locations))
		for i, location in enumerate(st.session_state.locations):
			data = st.session_state.traffic_data[location]
			with cols[i]:
				congestion = data["congestion_level"]
				st.metric(
					label=location,
					value=congestion.capitalize(),
					delta=f"{data['daily_traffic']:,} vehicles/day"
				)
				st.progress(
					{"low": 0.3, "moderate": 0.6, "high": 0.9}[congestion],
					text=f"{data['lanes']} lanes | Speed: {data['speed_limit']} km/h"
				)

		# Show map if enabled
		if show_map:
			st.divider()
			st.subheader("🗺️ Traffic Map")

			# Create map centered on first location
			m = folium.Map(location=[12.9716, 77.5946], zoom_start=13)

			# Add markers for each location
			for i, location in enumerate(st.session_state.locations):
				data = st.session_state.traffic_data[location]
				congestion = data["congestion_level"]

				# Different colors based on congestion
				color = {
					"low": "green",
					"moderate": "orange",
					"high": "red"
				}[congestion]

				folium.Marker(
					[12.9716 - (i * 0.01), 77.5946 + (i * 0.01)],
					popup=f"<b>{location}</b><br>Congestion: {congestion.capitalize()}",
					tooltip=location,
					icon=folium.Icon(color=color, icon="car")
				).add_to(m)

			# Display map
			with st.container():
				st_folium(m, width=700, height=400)

		# Show stats if enabled
		if show_stats:
			st.divider()
			st.subheader("📈 Traffic Statistics")

			# Create DataFrame
			data = []
			for loc, stats in st.session_state.traffic_data.items():
				data.append({
					"Location": loc,
					"Length (km)": stats["length"],
					"Lanes": stats["lanes"],
					"Speed Limit (km/h)": stats["speed_limit"],
					"Daily Traffic": stats["daily_traffic"],
					"Congestion Level": stats["congestion_level"].capitalize()
				})

			df = pd.DataFrame(data)
			st.dataframe(
				df,
				column_config={
					"Daily Traffic": st.column_config.NumberColumn(format="%d")
				},
				hide_index=True,
				use_container_width=True
			)

	# Processing state
	if st.session_state.get("processing"):
		with st.status("🚀 Running traffic analysis...", expanded=True) as status:
			st.write("🔍 Gathering traffic data for selected locations...")
			time.sleep(1)

			st.write("📊 Analyzing traffic patterns and congestion points...")
			time.sleep(2)

			st.write("💡 Developing optimization strategies...")
			time.sleep(2)

			st.write("📝 Preparing final recommendations...")
			time.sleep(1)

			try:
				# Execute crew
				result = create_traffic_crew(st.session_state.locations)
				st.session_state.analysis = result.get("analysis")
				st.session_state.strategy = result.get("strategy")
				status.update(label="✅ Analysis complete!", state="complete")
			except Exception as e:
				st.error(f"Error during analysis: {str(e)}")
				status.update(label="❌ Analysis failed", state="error")

			st.session_state.processing = False
			st.rerun()

	# Display analysis results
	if st.session_state.analysis:
		st.divider()
		st.subheader("📊 Traffic Analysis Report")

		with st.container():
			st.markdown(f'<div class="card traffic-card">{st.session_state.analysis}</div>', 
						unsafe_allow_html=True)

	# Display strategy recommendations
	if st.session_state.strategy:
		st.divider()
		st.subheader("💡 Optimization Strategy")

		with st.container():
			st.markdown(f'<div class="card strategy-card">{st.session_state.strategy}</div>', 
						unsafe_allow_html=True)

		st.divider()
		st.subheader("🚀 Implementation Roadmap")

		# Example roadmap - would be generated by AI in real implementation
		roadmap = """
		| Phase | Timeline | Key Activities | Expected Outcome |
		|-------|----------|----------------|------------------|
		| 1. Preparation | Month 1-2 | - Stakeholder engagement<br>- Detailed planning<br>- Resource allocation | Approved implementation plan |
		| 2. Signal Optimization | Month 3-4 | - Install smart traffic signals<br>- Implement adaptive timing | 20% reduction in wait times |
		| 3. Lane Reconfiguration | Month 5-6 | - Add dedicated bus lanes<br>- Optimize lane assignments | Improved traffic flow |
		| 4. Tech Implementation | Month 7-8 | - Deploy IoT sensors<br>- Launch traffic management platform | Real-time traffic monitoring |
		| 5. Evaluation | Month 9-12 | - Performance metrics analysis<br>- Continuous improvement | 30% congestion reduction |
		"""

		st.markdown(roadmap)

	# Example section when no analysis run
	if not st.session_state.traffic_data:
		st.info("💡 Select road segments and click 'Run Traffic Analysis' to get started")

		with st.expander("Example Queries", expanded=True):
			st.write("Try these sample analyses:")
			cols = st.columns(3)
			with cols[0]:
				if st.button("MG Road & Brigade Road", use_container_width=True):
					st.session_state.locations = ["MG Road", "Brigade Road"]
					st.session_state.traffic_data = get_traffic_data(["MG Road", "Brigade Road"])
					st.rerun()
			with cols[1]:
				if st.button("Anna Salai Corridor", use_container_width=True):
					st.session_state.locations = ["Anna Salai", "Mount Road"]
					st.session_state.traffic_data = get_traffic_data(["Anna Salai", "Mount Road"])
					st.rerun()
			with cols[2]:
				if st.button("T Nagar Area", use_container_width=True):
					st.session_state.locations = ["T Nagar"]
					st.session_state.traffic_data = get_traffic_data(["T Nagar"])
					st.rerun()

# Footer
st.divider()
st.caption("© 2024 Urban Traffic Management System | Powered by CrewAI and Gemini 1.5 Flash")

