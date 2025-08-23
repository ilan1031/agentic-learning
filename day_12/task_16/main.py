import os
import re
import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, Any
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Gemini model
def initialize_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel('gemini-1.5-pro-latest')

# CrewAI Agent Definitions
class EssayOutlinerCrew:
    def __init__(self):
        self.gemini_model = initialize_gemini()
    
    def generate_with_gemini(self, prompt, temperature=0.3):
        """Helper function to generate content with Gemini"""
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def create_agents(self):
        """Create the CrewAI agents for essay outlining"""
        
        # Thesis Agent - generates thesis statements
        self.thesis_agent = Agent(
            role='Thesis Statement Specialist',
            goal='Generate clear, compelling thesis statements based on essay topics and requirements',
            backstory='Expert in academic writing with deep knowledge of various essay types and thesis formulation',
            verbose=True,
            allow_delegation=False,
            # Since we're not using CrewAI's built-in LLM, we'll handle execution separately
        )
        
        # Structure Agent - creates outline structure
        self.structure_agent = Agent(
            role='Essay Structure Architect',
            goal='Create logical, well-organized essay outlines with appropriate sections',
            backstory='Experienced in academic writing and structuring essays for maximum impact and clarity',
            verbose=True,
            allow_delegation=False
        )
        
        # Content Agent - suggests content ideas
        self.content_agent = Agent(
            role='Content Development Specialist',
            goal='Suggest key points, arguments, and examples for each section of the essay',
            backstory='Knowledgeable in various subjects with ability to develop compelling content ideas',
            verbose=True,
            allow_delegation=False
        )
        
        # Refinement Agent - reviews and improves the outline
        self.refinement_agent = Agent(
            role='Quality Assurance Editor',
            goal='Review and refine the essay outline for coherence, completeness, and quality',
            backstory='Meticulous editor with expertise in academic writing standards and requirements',
            verbose=True,
            allow_delegation=False
        )
    
    def create_tasks(self, topic, essay_type, word_count, requirements):
        """Create tasks for each agent"""
        
        # Task for Thesis Agent
        self.thesis_task = Task(
            description=f"""Generate a strong thesis statement for an essay with the following details:
            - Topic: {topic}
            - Type: {essay_type}
            - Word Count: {word_count}
            - Additional Requirements: {requirements}
            
            The thesis should be clear, specific, and appropriate for the essay type.""",
            agent=self.thesis_agent,
            expected_output="A single, well-crafted thesis statement"
        )
        
        # Task for Structure Agent
        self.structure_task = Task(
            description=f"""Create a structured outline for an essay with the following details:
            - Topic: {topic}
            - Type: {essay_type}
            - Word Count: {word_count}
            - Additional Requirements: {requirements}
            
            The outline should include:
            1. Introduction section
            2. Body sections (appropriate number based on word count)
            3. Conclusion section
            4. Suggested section headings""",
            agent=self.structure_agent,
            expected_output="A structured outline with sections and headings in markdown format",
            context=[self.thesis_task]
        )
        
        # Task for Content Agent
        self.content_task = Task(
            description=f"""Develop content ideas for the essay outline with the following details:
            - Topic: {topic}
            - Type: {essay_type}
            - Word Count: {word_count}
            - Additional Requirements: {requirements}
            
            For each section of the outline, suggest:
            1. Key points to cover
            2. Supporting arguments
            3. Potential examples or evidence
            4. Transitions between sections""",
            agent=self.content_agent,
            expected_output="Detailed content suggestions for each section of the outline",
            context=[self.thesis_task, self.structure_task]
        )
        
        # Task for Refinement Agent
        self.refinement_task = Task(
            description=f"""Review and refine the complete essay outline with the following details:
            - Topic: {topic}
            - Type: {essay_type}
            - Word Count: {word_count}
            - Additional Requirements: {requirements}
            
            Check for:
            1. Coherence and logical flow
            2. Completeness of arguments
            3. Appropriateness for essay type
            4. Adherence to word count requirements
            5. Overall quality and effectiveness""",
            agent=self.refinement_agent,
            expected_output="A refined, high-quality essay outline in markdown format",
            context=[self.thesis_task, self.structure_task, self.content_task]
        )
    
    def execute_task(self, task, context=None):
        """Execute a task using Gemini"""
        prompt = task.description
        
        # Add context if available
        if context:
            context_text = "\n\nContext from previous tasks:\n"
            for key, value in context.items():
                context_text += f"{key}: {value}\n"
            prompt += context_text
        
        return self.generate_with_gemini(prompt)
    
    def run(self, topic, essay_type, word_count, requirements):
        """Run the complete essay outlining process"""
        self.create_agents()
        self.create_tasks(topic, essay_type, word_count, requirements)
        
        # Execute tasks sequentially
        results = {}
        
        # Execute thesis task
        results['thesis'] = self.execute_task(self.thesis_task)
        
        # Execute structure task with thesis context
        results['structure'] = self.execute_task(
            self.structure_task, 
            {'thesis': results['thesis']}
        )
        
        # Execute content task with previous context
        results['content'] = self.execute_task(
            self.content_task,
            {'thesis': results['thesis'], 'structure': results['structure']}
        )
        
        # Execute refinement task with all context
        results['refined_outline'] = self.execute_task(
            self.refinement_task,
            {
                'thesis': results['thesis'],
                'structure': results['structure'],
                'content': results['content']
            }
        )
        
        return results

# Save essay outline to file
def save_essay_outline(outline_content, topic):
    """Save essay outline to a markdown file"""
    if not os.path.exists('essays'):
        os.makedirs('essays')
    
    # Create a filename from timestamp and topic
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_topic = re.sub(r'[^a-zA-Z0-9 ]', '', topic).replace(' ', '_')[:30]
    filename = f"essays/outline_{timestamp}_{clean_topic}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(outline_content)
    
    return filename

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Automated Essay Outliner",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("📝 Automated Essay Outliner")
    st.markdown("Generate structured essay outlines using AI agents")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "Essay Topic:",
            placeholder="e.g., The Impact of Climate Change on Biodiversity"
        )
        
        essay_type = st.selectbox(
            "Essay Type:",
            ["Argumentative", "Expository", "Narrative", "Descriptive", "Compare and Contrast", "Persuasive"]
        )
    
    with col2:
        word_count = st.slider(
            "Word Count:",
            min_value=500,
            max_value=5000,
            value=1500,
            step=500
        )
        
        requirements = st.text_area(
            "Additional Requirements:",
            placeholder="e.g., Include at least 5 sources, focus on recent developments...",
            height=100
        )
    
    if st.button("Generate Outline", type="primary"):
        if not topic.strip():
            st.error("Please enter an essay topic")
            return
        
        if not os.getenv("GEMINI_API_KEY"):
            st.error("Please set GEMINI_API_KEY in your .env file")
            return
        
        with st.spinner("Generating your essay outline... This may take a minute."):
            try:
                # Initialize and run the essay outliner crew
                essay_crew = EssayOutlinerCrew()
                results = essay_crew.run(topic, essay_type, word_count, requirements)
                
                # Display results
                st.success("Essay outline generated successfully!")
                
                # Create tabs for different parts of the outline
                tab1, tab2, tab3, tab4 = st.tabs([
                    "Final Outline", "Thesis Statement", "Structure", "Content Ideas"
                ])
                
                with tab1:
                    st.subheader("Refined Essay Outline")
                    st.markdown(results['refined_outline'])
                    
                    # Save to file
                    filename = save_essay_outline(results['refined_outline'], topic)
                    st.info(f"Outline saved to: {filename}")
                
                with tab2:
                    st.subheader("Thesis Statement")
                    st.write(results['thesis'])
                
                with tab3:
                    st.subheader("Essay Structure")
                    st.markdown(results['structure'])
                
                with tab4:
                    st.subheader("Content Ideas")
                    st.markdown(results['content'])
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Instructions section
    with st.expander("How to use this tool"):
        st.markdown("""
        1. Enter your essay topic in the text field
        2. Select the type of essay you're writing
        3. Set the desired word count using the slider
        4. Add any additional requirements or instructions
        5. Click the "Generate Outline" button
        
        The system uses multiple AI agents to:
        - Create a strong thesis statement
        - Develop a logical essay structure
        - Suggest content ideas for each section
        - Refine the complete outline for quality
        
        The final outline will be displayed and automatically saved as a markdown file.
        """)
    
    # Example section
    with st.expander("Example Output"):
        st.markdown("""
        ### Thesis
        Climate change represents the most pressing environmental challenge of our time, requiring immediate and coordinated global action through policy reform, technological innovation, and individual behavioral changes.
        
        ### Outline
        1. **Introduction**
           - Hook: Startling statistics about climate change impacts
           - Background context on climate science
           - Thesis statement
        
        2. **Causes of Climate Change**
           - Greenhouse gas emissions from human activities
           - Deforestation and land use changes
           - Industrial processes and energy production
        
        3. **Impacts of Climate Change**
           - Rising global temperatures and extreme weather events
           - Sea-level rise and coastal erosion
           - Biodiversity loss and ecosystem disruption
           - Socioeconomic consequences
        
        4. **Solutions and Mitigation Strategies**
           - Policy interventions and international agreements
           - Renewable energy transition
           - Sustainable agriculture and forestry practices
           - Individual actions and consumer choices
        
        5. **Conclusion**
           - Restate thesis in light of evidence presented
           - Summarize key points
           - Call to action for collective responsibility
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center'>"
        "Powered by CrewAI, Gemini 1.5, and Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()