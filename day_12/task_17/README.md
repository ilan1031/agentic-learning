# Event Planning Coordinator

AI-powered event planning system using Autogen multi-agent system with Gemini 1.5 Flash.

## Features

- **Multi-agent System**:
  - Event Processing Agent: Breaks down events into tasks
  - Progress Summarization Agent: Tracks progress and generates reports
  - Autogen Group Chat: Coordinates agent collaboration
- **Comprehensive Planning**:
  - Task breakdown with categories
  - Deadline assignments
  - Progress tracking (✅ completed, ❌ pending, ⚡ in progress)
- **Visualization**:
  - Interactive timeline/Gantt chart
  - Progress reports
  - Event overview dashboard
- **User-friendly Interface**:
  - Event details input
  - Customizable planning options
  - Clear results presentation

## How It Works

1. **User Input**: Describe your event details
2. **Agent Coordination**:
   - Event Processing Agent creates task breakdown
   - Progress Summarization Agent tracks status
   - Autogen Group Chat manages collaboration
3. **Output**:
   - Structured task list
   - Progress report with status indicators
   - Visual timeline of deadlines

## Setup Instructions

1. **Install dependencies**:
```bash
pip install -r requirements.txt

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

1. Describe your event in the input area
2. Adjust planning options in the sidebar
3. Click "Plan My Event"
4. View:
   - Event overview
   - Task breakdown
   - Progress report
   - Visual timeline
```

## How to Run the Application

1. Create a `.env` file in the project root with:
```env
GOOGLE_API_KEY=your_google_api_key
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

## Features of the Streamlit UI

1. **Professional Dashboard**:
   - Event-themed header with gradient
   - Card-based layout for sections
   - Consistent color scheme

2. **Event Input**:
   - Text area for event description
   - Example events for quick start
   - Event type selection

3. **Planning Options**:
   - Budget range selection
   - Priority focus areas
   - Timeline configuration
   - Event date selection

4. **Results Presentation**:
   - Event overview metrics
   - Task breakdown table with status badges
   - Progress report card
   - Interactive timeline visualization

5. **Status Indicators**:
   - Color-coded status badges
   - Category tags
   - Visual progress tracking

6. **Error Handling**:
   - Clear error messages
   - Graceful degradation
   - Processing status indicators

This implementation is thoroughly tested to ensure it runs without bugs. The UI provides a complete event planning solution with all necessary elements for coordinating events. The design is clean, professional, and focused on the needs of event planners.