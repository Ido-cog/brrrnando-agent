from duckduckgo_search import DDGS
from typing import List, Dict

def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search the web for text results.
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        return [{"title": r["title"], "href": r["href"], "body": r["body"]} for r in results]
    except Exception as e:
        print(f"Error searching web: {e}")
        return []

def search_videos(query: str, max_results: int = 3, timelimit: str = None) -> List[Dict[str, str]]:
    """
    Search for videos with optional time limit ('d', 'w', 'm').
    """
    try:
        results = DDGS().videos(query, max_results=max_results, timelimit=timelimit)
        return [{"title": r["title"], "content": r["content"], "description": r.get("description", "")} for r in results]
    except Exception as e:
        print(f"Error searching videos: {e}")
        return []
