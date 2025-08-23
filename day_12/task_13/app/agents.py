import autogen
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_problem_parser_agent():
    """Create Problem Parser Agent"""
    config = {
        "name": "Problem_Parser",
        "system_message": """You are a Math Problem Parser Agent. Your responsibilities:
1. Parse user-input math problems into structured format
2. Identify the problem type (algebra, calculus, geometry, etc.)
3. Extract key components and variables
4. Output structured JSON representation

Output format:
{
  "problem_type": "algebra",
  "components": {
    "equation": "2x + 5 = 15",
    "variables": ["x"],
    "domain": "real numbers"
  },
  "complexity": "intermediate"
}""",
        "llm_config": {
            "config_list": [{"model": "gemini-1.5"}],
            "temperature": 0.1
        }
    }
    return autogen.AssistantAgent(**config)

def create_solver_agent():
    """Create Solver Agent"""
    config = {
        "name": "Solver",
        "system_message": """You are a Math Solver Agent. Your responsibilities:
1. Solve mathematical problems using appropriate methods
2. Show step-by-step solutions
3. Handle various math domains: algebra, calculus, geometry, statistics
4. Ensure solutions are accurate and complete

Provide solutions in this format:
{
  "solution": "x = 5",
  "steps": [
    "Step 1: Subtract 5 from both sides: 2x = 10",
    "Step 2: Divide both sides by 2: x = 5"
  ],
  "method": "linear equation solving"
}""",
        "llm_config": {
            "config_list": [{"model": "gemini-1.5"}],
            "temperature": 0.1
        }
    }
    return autogen.AssistantAgent(**config)

def create_explanation_agent():
    """Create Explanation Agent"""
    config = {
        "name": "Explanation_Generator",
        "system_message": """You are an Explanation Generator Agent. Your responsibilities:
1. Provide detailed, step-by-step explanations of solutions
2. Explain the reasoning behind each step
3. Use clear, educational language
4. Highlight key concepts and techniques

Output format:
{
  "explanation": [
    {
      "step": 1,
      "description": "We start by isolating the variable term",
      "reasoning": "This allows us to focus on the variable we're solving for"
    }
  ],
  "key_concepts": ["linear equations", "isolation of variables"]
}""",
        "llm_config": {
            "config_list": [{"model": "gemini-1.5"}],
            "temperature": 0.1
        }
    }
    return autogen.AssistantAgent(**config)

def create_validator_agent():
    """Create Validator Agent"""
    config = {
        "name": "Validator",
        "system_message": """You are a Validator Agent. Your responsibilities:
1. Verify the correctness of solutions
2. Check for mathematical errors
3. Validate that all steps are logically sound
4. Confirm the solution satisfies the original problem

Output format:
{
  "is_valid": true,
  "validation_method": "substitution",
  "details": "Substituting x=5 back into the original equation confirms the solution",
  "confidence": "high"
}""",
        "llm_config": {
            "config_list": [{"model": "gemini-1.5"}],
            "temperature": 0.1
        }
    }
    return autogen.AssistantAgent(**config)

def create_example_agent():
    """Create Example Agent"""
    config = {
        "name": "Example_Creator",
        "system_message": """You are an Example Creator Agent. Your responsibilities:
1. Generate additional practice problems similar to the solved problem
2. Provide solutions for these examples
3. Vary difficulty levels and approaches
4. Ensure examples are relevant to the original problem

Output format:
{
  "examples": [
    {
      "problem": "3y - 7 = 8",
      "solution": "y = 5",
      "explanation": "Add 7 to both sides, then divide by 3"
    }
  ],
  "count": 2
}""",
        "llm_config": {
            "config_list": [{"model": "gemini-1.5"}],
            "temperature": 0.1
        }
    }
    return autogen.AssistantAgent(**config)

def create_user_proxy_agent():
    """Create User Proxy Agent"""
    config = {
        "name": "User_Proxy",
        "human_input_mode": "NEVER",
        "code_execution_config": False,
        "is_termination_msg": lambda x: "TERMINATE" in x.get("content", ""),
        "system_message": "You are the User Proxy Agent. Your role is to initiate conversations and manage communication."
    }
    return autogen.UserProxyAgent(**config)