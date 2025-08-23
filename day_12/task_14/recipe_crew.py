import os
from crewai import Agent, Task, Crew
from crewai_google_llm import GoogleLLM
from dotenv import load_dotenv

load_dotenv()

class RecipeCrew:
    def __init__(self):
        self.gemini_llm = GoogleLLM(
            model="gemini-1.5-pro-latest",
            temperature=0.7
        )
    
    def create_agents(self):
        # Primary Chef Agent - Generates recipes
        self.primary_chef = Agent(
            role='Primary Chef',
            goal='Generate creative and delicious recipes based on available ingredients',
            backstory='An experienced chef with expertise in creating innovative recipes from various cuisines.',
            verbose=True,
            llm=self.gemini_llm,
            allow_delegation=False
        )
        
        # Feedback & Revision Agent - Refines recipes
        self.feedback_chef = Agent(
            role='Feedback Chef',
            goal='Review and refine recipes for clarity, feasibility, and cooking instructions',
            backstory='A meticulous chef who ensures recipes are practical, well-structured, and easy to follow.',
            verbose=True,
            llm=self.gemini_llm,
            allow_delegation=False
        )
    
    def create_tasks(self, ingredients):
        # Task for Primary Chef
        self.generate_recipe_task = Task(
            description=f"""Generate a detailed recipe using these ingredients: {ingredients}.
            Include:
            1. A creative recipe name
            2. Complete ingredient list with measurements
            3. Step-by-step cooking instructions
            4. Estimated preparation and cooking time
            5. Serving suggestions""",
            agent=self.primary_chef,
            expected_output="A complete recipe in markdown format"
        )
        
        # Task for Feedback Chef
        self.refine_recipe_task = Task(
            description="""Review the generated recipe and refine it for:
            1. Clarity and organization
            2. Feasibility of cooking instructions
            3. Accurate measurements and timing
            4. Overall cooking experience
            5. Make sure it's in proper markdown format""",
            agent=self.feedback_chef,
            expected_output="A refined, well-structured recipe in markdown format",
            context=[self.generate_recipe_task]
        )
    
    def run(self, ingredients):
        self.create_agents()
        self.create_tasks(ingredients)
        
        crew = Crew(
            agents=[self.primary_chef, self.feedback_chef],
            tasks=[self.generate_recipe_task, self.refine_recipe_task],
            verbose=2
        )
        
        result = crew.kickoff()
        return result