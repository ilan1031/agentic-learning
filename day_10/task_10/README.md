# Urban Traffic Management System

AI-powered traffic analysis and optimization platform using CrewAI multi-agent systems.

## Features

- **Multi-agent Architecture**:
  - Traffic Analyst Agent: Identifies congestion patterns
  - Traffic Strategist Agent: Develops optimization strategies
- **Real-time Visualization**:
  - Interactive traffic map
  - Traffic metrics dashboard
  - Statistical analysis
- **AI-powered Insights**:
  - Bottleneck identification
  - Optimization strategies
  - Implementation roadmap
- **User-friendly Interface**:
  - Location selection
  - Analysis customization
  - Clear results presentation

## How It Works

1. **User Input**: Select road segments to analyze
2. **Data Collection**: Retrieve traffic data (mock data in this implementation)
3. **Traffic Analysis**: 
   - Identify congestion patterns
   - Analyze peak traffic times
   - Detect bottlenecks
4. **Strategy Development**:
   - Propose traffic optimization solutions
   - Create implementation roadmap
   - Predict outcomes
5. **Results Presentation**: Display analysis and strategies in user-friendly format

## Setup Instructions

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
Create a `.env` file with:
```env
GOOGLE_API_KEY=your_google_api_key
```

3. **Run the application**:
```bash
streamlit run streamlit_app.py
```

4. **Access the UI**:
Open `http://localhost:8501` in your browser

## Usage

1. Select road segments to analyze
2. Configure analysis options
3. Click "Run Traffic Analysis"
4. View:
   - Current traffic status
   - Traffic map
   - Detailed analysis report
   - Optimization strategies
   - Implementation roadmap

## How to Run the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Google API key:
```env
GOOGLE_API_KEY=your_google_api_key
```

3. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

## Features of the Streamlit UI

1. **Professional Dashboard**:
   - Modern header with gradient background
   - Card-based layout for content sections
   - Consistent color scheme with traffic-themed colors

2. **Location Selection**:
   - Multi-select for choosing road segments
   - Example queries for quick start
   - Traffic metrics display

3. **Analysis Configuration**:
   - Analysis depth selection (Quick/Standard/Comprehensive)
   - Time frame options (Current/Peak Hours/24-hour Cycle)
   - Visualization toggles (Map/Statistics)

4. **Visualization Tools**:
   - Interactive traffic map with color-coded markers
   - Progress bars for congestion levels
   - Data tables with traffic statistics

5. **Results Presentation**:
   - Traffic analysis report in formatted card
   - Optimization strategy with clear recommendations
   - Implementation roadmap table
   - Error handling and loading states

6. **Responsive Design**:
   - Sidebar for controls and configuration
   - Main content area for results
   - Mobile-friendly layout

The UI provides a complete traffic management solution with all necessary elements for analyzing urban traffic patterns and developing optimization strategies. The design is professional, intuitive, and focused on the needs of urban planners and traffic engineers.

