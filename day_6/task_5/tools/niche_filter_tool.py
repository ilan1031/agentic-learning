from langchain.tools import tool
import json
import re
from typing import List, Dict


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _compute_relevance(niche: str, idea: str) -> int:
    niche_tokens = set(_tokenize(niche))
    idea_tokens = set(_tokenize(idea))
    if not niche_tokens or not idea_tokens:
        return 0
    overlap = niche_tokens.intersection(idea_tokens)
    # Simple overlap-based score scaled to 100
    score = int(100 * len(overlap) / len(niche_tokens))
    return score


@tool
def niche_filter(input: str) -> str:
    """Filter and score ideas by niche relevance. 
    Input: JSON string {"niche": "<niche>", "ideas": ["idea1", "idea2", ...]}
    Output: Markdown list with relevance scores and a JSON payload for downstream use.
    """
    try:
        payload = json.loads(input)
        niche = payload.get("niche", "").strip()
        ideas: List[str] = payload.get("ideas", [])
        if not niche or not ideas:
            return "No niche or ideas provided. Provide JSON with 'niche' and 'ideas'."

        scored: List[Dict] = []
        for idea in ideas:
            score = _compute_relevance(niche, idea)
            scored.append({"idea": idea, "score": score})
        scored.sort(key=lambda x: x["score"], reverse=True)

        md_lines = [f"- {item['idea']} — {item['score']}% relevance" for item in scored]
        json_blob = json.dumps({"niche": niche, "ideas": scored}, ensure_ascii=False)
        return "\n".join(md_lines) + "\n\nJSON:" + json_blob
    except Exception as e:
        return f"niche_filter error: {e}"