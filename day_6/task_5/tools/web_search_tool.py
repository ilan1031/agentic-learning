from langchain.tools import tool
from serpapi import GoogleSearch
import os

@tool
def web_search(query: str) -> str:
    """Use SerpAPI to perform a web search and return top result snippets (title + link).
    Returns markdown with up to 5 results.
    """
    params = {
        "q": query,
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "num": 5,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    items = results.get("organic_results", [])
    if not items:
        return "No results."
    lines = []
    for it in items[:5]:
        title = it.get("title") or "Result"
        link = it.get("link") or ""
        snippet = it.get("snippet") or ""
        if link:
            lines.append(f"- [{title}]({link}) — {snippet}")
        else:
            lines.append(f"- {title} — {snippet}")
    return "\n".join(lines)
