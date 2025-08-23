# Automated Essay Outliner

An AI-powered tool that generates structured essay outlines using CrewAI agents and Gemini 1.5 as the LLM.

## Features

- Generates thesis statements based on essay topics and requirements
- Creates logical essay structures with appropriate sections
- Suggests content ideas, arguments, and examples
- Refines outlines for quality and coherence
- Saves outlines as Markdown files
- Clean Streamlit-based UI

## Setup Instructions

1. **Create a project directory**
   ```bash
   mkdir essay-outliner
   cd essay-outliner
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
   - Enter your essay details and click "Generate Outline"

## How It Works

1. **Thesis Agent**: Creates a strong thesis statement based on your topic and requirements
2. **Structure Agent**: Develops a logical essay structure with appropriate sections
3. **Content Agent**: Suggests key points, arguments, and examples for each section
4. **Refinement Agent**: Reviews and improves the outline for quality and coherence

The workflow is orchestrated using CrewAI, which manages the sequential execution of these specialized agents.

## Project Structure

- `main.py` - Streamlit app with CrewAI workflow
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not in version control)
- `essays/` - Directory where generated outlines are saved

## Essay Types Supported

- Argumentative
- Expository
- Narrative
- Descriptive
- Compare and Contrast
- Persuasive

## Troubleshooting

- **API key errors**: Verify your Gemini API key is correctly set in the `.env` file
- **Module not found errors**: Ensure all dependencies are installed from requirements.txt
- **Timeout errors**: Very complex outlines may take longer to generate

## Dependencies

- crewai==0.28.8
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

This implementation provides a complete essay outliner using CrewAI for agent orchestration, Gemini 1.5 as the LLM, and Streamlit for the UI - without using Flask or FastAPI. The system includes multiple specialized agents that work together to create comprehensive essay outlines with thesis statements, structured sections, and content ideas.