from app.agents import (
    create_user_proxy_agent, create_problem_parser_agent, 
    create_solver_agent, create_explanation_agent, 
    create_validator_agent, create_example_agent
)
import autogen
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MathProblemSolver:
    def __init__(self):
        self.user_proxy = create_user_proxy_agent()
        self.problem_parser = create_problem_parser_agent()
        self.solver = create_solver_agent()
        self.explanation = create_explanation_agent()
        self.validator = create_validator_agent()
        self.example = create_example_agent()
        
        # Create group chat
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.problem_parser, self.solver, 
                   self.explanation, self.validator, self.example],
            messages=[],
            max_round=12
        )
        
        # Create group chat manager
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config={"config_list": [{"model": "gemini-1.5"}]}
        )
        
        # Initialize state
        self.problem = ""
        self.results = {}
    
    def solve_problem(self, problem: str):
        """Solve a math problem using the multi-agent system"""
        try:
            self.problem = problem
            
            # Initiate conversation
            self.user_proxy.initiate_chat(
                self.manager,
                message=f"Solve this math problem: {problem}"
            )
            
            # Extract results from conversation
            self._extract_results()
            
            # Save results to file
            self._save_results()
            
            return self.results
        except Exception as e:
            logger.error(f"Problem solving failed: {str(e)}")
            return {
                "error": str(e),
                "problem": problem,
                "parsed_problem": {},
                "solution": {},
                "explanation": {},
                "validation": {},
                "examples": []
            }
    
    def _extract_results(self):
        """Extract results from group chat messages"""
        self.results = {
            "problem": self.problem,
            "parsed_problem": {},
            "solution": {},
            "explanation": {},
            "validation": {},
            "examples": []
        }
        
        # Extract parsed problem
        for msg in reversed(self.groupchat.messages):
            if "problem_type" in msg.get("content", ""):
                try:
                    content = msg["content"]
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        self.results["parsed_problem"] = json.loads(content[start:end])
                        break
                except:
                    pass
        
        # Extract solution
        for msg in reversed(self.groupchat.messages):
            if "solution" in msg.get("content", "") and "steps" in msg.get("content", ""):
                try:
                    content = msg["content"]
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        self.results["solution"] = json.loads(content[start:end])
                        break
                except:
                    pass
        
        # Extract explanation
        for msg in reversed(self.groupchat.messages):
            if "explanation" in msg.get("content", "") and "key_concepts" in msg.get("content", ""):
                try:
                    content = msg["content"]
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        self.results["explanation"] = json.loads(content[start:end])
                        break
                except:
                    pass
        
        # Extract validation
        for msg in reversed(self.groupchat.messages):
            if "is_valid" in msg.get("content", ""):
                try:
                    content = msg["content"]
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        self.results["validation"] = json.loads(content[start:end])
                        break
                except:
                    pass
        
        # Extract examples
        for msg in reversed(self.groupchat.messages):
            if "examples" in msg.get("content", ""):
                try:
                    content = msg["content"]
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        examples_data = json.loads(content[start:end])
                        self.results["examples"] = examples_data.get("examples", [])
                        break
                except:
                    pass
    
    def _save_results(self):
        """Save results to a text file"""
        try:
            # Create results directory if it doesn't exist
            os.makedirs("app/results", exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"app/results/solution_{timestamp}.txt"
            
            # Write results to file
            with open(filename, "w") as f:
                f.write("MATH PROBLEM SOLVER RESULTS\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Problem: {self.results.get('problem', '')}\n\n")
                
                f.write("Parsed Problem:\n")
                f.write(json.dumps(self.results.get('parsed_problem', {}), indent=2) + "\n\n")
                
                f.write("Solution:\n")
                f.write(json.dumps(self.results.get('solution', {}), indent=2) + "\n\n")
                
                f.write("Explanation:\n")
                f.write(json.dumps(self.results.get('explanation', {}), indent=2) + "\n\n")
                
                f.write("Validation:\n")
                f.write(json.dumps(self.results.get('validation', {}), indent=2) + "\n\n")
                
                f.write("Examples:\n")
                f.write(json.dumps(self.results.get('examples', []), indent=2) + "\n")
            
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")

# Create singleton instance
math_solver = MathProblemSolver()