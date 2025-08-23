import os
import re
import ast
import streamlit as st
from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Define the state for our graph
class DocGenerationState(TypedDict):
    code_input: str
    analysis: str
    documentation: str
    refined_documentation: str
    needs_refinement: bool
    refinement_feedback: str

# Initialize the Gemini model
def create_gemini_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

# Agent functions
def code_analysis_agent(state: DocGenerationState):
    """Analyze the code structure and identify components"""
    llm = create_gemini_model()
    
    # Simple AST parsing to identify functions, classes, etc.
    try:
        tree = ast.parse(state["code_input"])
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        imports_from = [f"{node.module}.{name.name}" for node in ast.walk(tree) 
                       if isinstance(node, ast.ImportFrom) for name in node.names]
        
        ast_analysis = f"""
        Functions found: {functions}
        Classes found: {classes}
        Imports: {imports + imports_from}
        """
    except Exception as e:
        ast_analysis = f"AST parsing error: {str(e)}"
    
    # Use LLM for deeper analysis
    prompt = f"""
    Analyze the following code and provide a detailed breakdown:
    
    {state['code_input']}
    
    AST Analysis:
    {ast_analysis}
    
    Please provide:
    1. A high-level overview of what the code does
    2. Key functions and their purposes
    3. Important variables and data structures
    4. Any dependencies or external libraries used
    5. Potential edge cases or error handling needs
    
    Be concise but thorough in your analysis.
    """
    
    messages = [
        SystemMessage(content="You are an expert code analyst. Analyze code thoroughly and provide clear insights."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {"analysis": response.content}

def documentation_agent(state: DocGenerationState):
    """Generate comprehensive documentation based on code analysis"""
    llm = create_gemini_model()
    
    prompt = f"""
    Based on this code analysis:
    {state['analysis']}
    
    And the original code:
    {state['code_input']}
    
    Generate comprehensive documentation including:
    
    1. Overview: A brief description of what the code does
    2. Functions/Methods: Detailed documentation for each function including:
       - Purpose
       - Parameters
       - Return values
       - Examples of usage
    3. Classes: Documentation for any classes including:
       - Attributes
       - Methods
       - Inheritance
    4. Usage Examples: How to use the code in practice
    5. Dependencies: Any required libraries or modules
    6. Notes: Any important considerations or limitations
    
    Format the documentation in clear markdown with appropriate headings.
    """
    
    messages = [
        SystemMessage(content="You are an expert technical writer. Create clear, comprehensive documentation for code."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {"documentation": response.content, "needs_refinement": False}

def manager_agent(state: DocGenerationState):
    """Review documentation and determine if refinement is needed"""
    llm = create_gemini_model()
    
    prompt = f"""
    Review this documentation for quality and completeness:
    
    {state['documentation']}
    
    For the original code:
    {state['code_input']}
    
    Evaluate if the documentation:
    1. Covers all important aspects of the code
    2. Is clear and easy to understand
    3. Includes practical examples
    4. Has proper formatting
    
    If the documentation needs improvement, provide specific feedback on what should be refined.
    If it's already high quality, simply state that no refinement is needed.
    """
    
    messages = [
        SystemMessage(content="You are a quality assurance manager. Review documentation thoroughly and provide constructive feedback."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    feedback = response.content
    
    # Check if refinement is needed
    needs_refinement = "no refinement is needed" not in feedback.lower()
    
    return {
        "refinement_feedback": feedback,
        "needs_refinement": needs_refinement
    }

def refinement_agent(state: DocGenerationState):
    """Refine the documentation based on feedback"""
    llm = create_gemini_model()
    
    prompt = f"""
    Original code:
    {state['code_input']}
    
    Initial documentation:
    {state['documentation']}
    
    Feedback for improvement:
    {state['refinement_feedback']}
    
    Please refine the documentation based on the feedback. Ensure it's comprehensive, clear, and well-formatted.
    """
    
    messages = [
        SystemMessage(content="You are an expert technical writer. Refine documentation based on feedback to make it more clear and comprehensive."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {"refined_documentation": response.content, "needs_refinement": False}

# Build the LangGraph workflow
def build_workflow():
    workflow = StateGraph(DocGenerationState)
    
    # Add nodes
    workflow.add_node("code_analysis", code_analysis_agent)
    workflow.add_node("documentation", documentation_agent)
    workflow.add_node("manager_review", manager_agent)
    workflow.add_node("refinement", refinement_agent)
    
    # Add edges
    workflow.set_entry_point("code_analysis")
    workflow.add_edge("code_analysis", "documentation")
    workflow.add_edge("documentation", "manager_review")
    
    # Conditional edge based on whether refinement is needed
    workflow.add_conditional_edges(
        "manager_review",
        lambda x: "refinement" if x["needs_refinement"] else END,
        {"refinement": "refinement", END: END}
    )
    
    workflow.add_edge("refinement", END)
    
    return workflow.compile()

# Save documentation to file
def save_documentation(doc_content, code_snippet):
    """Save documentation to a markdown file"""
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    # Create a filename from timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"docs/documentation_{timestamp}.md"
    
    # Add code reference to documentation
    full_content = f"# Code Documentation\n\n## Original Code\n```python\n{code_snippet}\n```\n\n{documentation}"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return filename

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Code Documentation Generator",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Code Documentation Generator")
    st.markdown("Generate comprehensive documentation for your code using AI")
    
    # Input section
    code_input = st.text_area(
        "Paste your Python code here:",
        height=300,
        placeholder="def example_function(arg1, arg2):\n    \"\"\"This is an example function\"\"\"\n    return arg1 + arg2"
    )
    
    if st.button("Generate Documentation", type="primary"):
        if not code_input.strip():
            st.error("Please enter some code to document")
            return
        
        if not os.getenv("GEMINI_API_KEY"):
            st.error("Please set GEMINI_API_KEY in your .env file")
            return
        
        with st.spinner("Analyzing your code and generating documentation..."):
            try:
                # Build and run the workflow
                workflow = build_workflow()
                initial_state = {"code_input": code_input}
                result = workflow.invoke(initial_state)
                
                # Get the final documentation
                documentation = result.get("refined_documentation", result.get("documentation", ""))
                
                # Display the documentation
                st.subheader("Generated Documentation")
                st.markdown(documentation)
                
                # Save to file
                filename = save_documentation(documentation, code_input)
                st.success(f"Documentation saved to: {filename}")
                
                # Show refinement feedback if applicable
                if "refinement_feedback" in result and result["needs_refinement"]:
                    with st.expander("View Refinement Feedback"):
                        st.write(result["refinement_feedback"])
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Instructions section
    with st.expander("How to use this tool"):
        st.markdown("""
        1. Paste your Python code in the text area
        2. Click the "Generate Documentation" button
        3. The AI will analyze your code and generate comprehensive documentation
        4. The documentation will be displayed and automatically saved as a markdown file
        
        The system uses multiple AI agents to:
        - Analyze your code structure
        - Generate initial documentation
        - Review the documentation for quality
        - Refine it if needed
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center'>"
        "Powered by LangGraph, Gemini 1.5, and Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()