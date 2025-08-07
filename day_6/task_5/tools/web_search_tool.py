from langchain.tools import tool
from serpapi import GoogleSearch
import os

@tool
def web_search(query: str) -> str:
    """Use SerpAPI to perform a web search and return top result snippet."""
    params = {
        "q": query,
        "api_key": os.environ.get("SERPAPI_API_KEY"),
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results['organic_results'][0]['snippet'] if 'organic_results' in results else "No results."
