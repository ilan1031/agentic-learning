from langchain.tools import tool

@tool
def custom_addition(numbers: str) -> str:
    """Adds a comma-separated string of numbers."""
    try:
        nums = list(map(float, numbers.split(',')))
        return f"Sum: {sum(nums)}"
    except:
        return "Invalid input. Provide comma-separated numbers."
