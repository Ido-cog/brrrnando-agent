import os
from duckduckgo_search import DDGS
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

def _tavily_search(query: str, max_results: int = 3, search_depth: str = "basic") -> List[Dict[str, str]]:
    """
    Fallback search using Tavily API.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("⚠️ Tavily API key not found. Skipping fallback.")
        return []

    print(f"🔄 DDG failed. Calling Tavily fallback for: {query}...")
    try:
        from tavily import TavilyClient
        tavily = TavilyClient(api_key=api_key)
        response = tavily.search(query=query, search_depth=search_depth, max_results=max_results)
        
        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "href": r.get("url", ""),
                "body": r.get("content", "")
            })
        print(f"✅ Tavily search successful. Found {len(results)} results.")
        return results
    except Exception as e:
        print(f"❌ Error searching Tavily: {e}")
        return []

def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search the web for text results using DDG, fallback to Tavily on error.
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return _tavily_search(query, max_results=max_results)
        return [{"title": r["title"], "href": r["href"], "body": r["body"]} for r in results]
    except Exception as e:
        print(f"Error searching web (DDG): {e}")
        # Only fallback to 202 Ratelimit or similar connection errors
        return _tavily_search(query, max_results=max_results)

def search_videos(query: str, max_results: int = 3, timelimit: str = None) -> List[Dict[str, str]]:
    """
    Search for videos using DDG, fallback to Tavily web search on error.
    """
    try:
        results = DDGS().videos(query, max_results=max_results, timelimit=timelimit)
        if not results:
             return _tavily_search(query + " video", max_results=max_results)
        return [{"title": r["title"], "content": r["content"], "description": r.get("description", "")} for r in results]
    except Exception as e:
        print(f"Error searching videos (DDG): {e}")
        return _tavily_search(query + " video", max_results=max_results)
