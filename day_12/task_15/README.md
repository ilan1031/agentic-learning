
# Code Documentation Generator

An AI-powered tool that automatically generates comprehensive documentation for Python code using LangGraph for orchestration and Gemini 1.5 as the LLM.

## Features

- Analyzes Python code structure using AST parsing and AI
- Generates comprehensive documentation including:
  - Function/method descriptions
  - Parameter explanations
  - Usage examples
  - Dependency information
- Quality assurance with refinement loop
- Saves documentation as Markdown files
- Clean Streamlit-based UI

## Setup Instructions

1. **Create a project directory**
   ```bash
   mkdir code-documentation-generator
   cd code-documentation-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```
   - Get an API key from [Google AI Studio](https://aistudio.google.com/)

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Access the application**
   - Open your browser to http://localhost:8501
   - Paste your Python code and click "Generate Documentation"

## How It Works

1. **Code Analysis Agent**: Parses the code structure and identifies key components
2. **Documentation Agent**: Generates initial documentation based on the analysis
3. **Manager Agent**: Reviews the documentation for quality and completeness
4. **Refinement Agent**: Improves the documentation if needed based on feedback

The workflow is orchestrated using LangGraph, which manages the sequential execution and conditional refinement loop.

## Project Structure

- `main.py` - Streamlit app with LangGraph workflow
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not in version control)
- `docs/` - Directory where generated documentation is saved

## Troubleshooting

- **API key errors**: Verify your Gemini API key is correctly set in the `.env` file
- **Module not found errors**: Ensure all dependencies are installed from requirements.txt
- **Timeout errors**: Very large code files may take longer to process

## Dependencies

- langgraph==0.0.40
- langchain-google-genai==0.0.11
- streamlit==1.28.1
- python-dotenv==1.0.0
- google-generativeai==0.3.2
```

## How to Run the Application

1. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Gemini API key in the `.env` file:**
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser to http://localhost:8501**

This implementation provides a complete code documentation generator using LangGraph for agent orchestration, Gemini 1.5 as the LLM, and Streamlit for the UI - all without using Flask or FastAPI. The system includes multiple specialized agents that work together to analyze code and generate comprehensive documentation with a quality assurance refinement loop.