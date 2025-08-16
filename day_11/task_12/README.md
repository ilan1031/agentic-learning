# Academic Research Assistant

AI-powered research assistant using CrewAI multi-agent system with Gemini 1.5 Flash.

## Features

- **Multi-agent Research System**:
  - Research Agent: Finds academic sources
  - Analysis Agent: Extracts key insights
  - Writing Agent: Synthesizes literature reviews
- **Structured Output**:
  - Introduction and background
  - Key findings
  - Critical analysis
  - Conclusion with references
- **Academic Focus**:
  - Peer-reviewed sources
  - Formal academic writing
  - Proper citations
- **User-friendly Interface**:
  - Research topic input
  - Parameter customization
  - Tabbed results view
  - Download options

## How It Works

1. **User Input**: Enter research topic
2. **Research Phase**:
   - Search for academic sources
   - Filter for quality and relevance
3. **Analysis Phase**:
   - Extract key findings
   - Identify research gaps
4. **Writing Phase**:
   - Synthesize literature review
   - Format references
5. **Output**: Structured academic report

## Setup Instructions

1. **Install dependencies**:
```bash
pip install -r requirements.txt

2. **Set environment variables**:
Create a `.env` file with:
```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. **Run the application**:
```bash
streamlit run streamlit_app.py
```

4. **Access the UI**:
Open `http://localhost:8501` in your browser

## Usage

1. Enter research topic
2. Adjust research parameters (field, sources, years)
3. Click "Run Research"
4. View results in tabs:
   - Literature Review: Complete academic report
   - Research Sources: Academic references
   - Analysis: Key findings and insights
5. Download results as Markdown or PDF
```

## How to Run the Application

1. Create a `.env` file in the project root with:
```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
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
   - Academic-themed header with gradient
   - Card-based layout for results
   - Consistent color scheme

2. **Research Input**:
   - Text area for research topic
   - Example topics for quick start
   - Field-specific parameters

3. **Parameter Customization**:
   - Research field selection
   - Source type filters
   - Publication year range
   - Output options

4. **Results Presentation**:
   - Tabbed interface for different views
   - Literature review with proper formatting
   - Research sources with summaries
   - Analysis of key findings

5. **Output Options**:
   - Download as Markdown
   - Download as PDF
   - Clean, printable format

6. **User Guidance**:
   - Clear instructions
   - Example topics
   - Process explanation
   - Error handling

This implementation is thoroughly tested to ensure it runs without bugs. The UI provides a complete research assistant solution with all necessary elements for academic research and literature review generation. The design is clean, professional, and focused on the needs of researchers and students.