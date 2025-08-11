import os
from typing import List
from tavily import TavilyClient


def search_academic_sources(query: str) -> list:
    """Search academic sources using Tavily API"""
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = tavily.search(
        query=query,
        search_depth="advanced",
        include_domains=[
            "scholar.google.com",
            "pubmed.ncbi.nlm.nih.gov",
            "arxiv.org",
            "jstor.org",
            "sciencedirect.com",
        ],
    )
    return results.get("results", [])[:10]


def filter_academic_sources(results: list) -> list:
    """Filter results to include only academic sources"""
    academic_domains = [
        ".edu",
        ".ac.",
        ".gov",
        "arxiv.org",
        "jstor.org",
        "springer.com",
        "sciencedirect.com",
        "nature.com",
        "science.org",
    ]

    return [
        result
        for result in results
        if any(domain in result.get("url", "") for domain in academic_domains)
    ]

