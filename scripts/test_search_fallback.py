import sys
import os
from unittest.mock import patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.integrations.search import search_web

def test_search_fallback():
    print("--- 🧪 Testing Search Fallback ---")
    
    # Check if TAVILY_API_KEY is available (even if dummy for this test logic)
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️ TAVILY_API_KEY not set. Setting a dummy key for logic testing.")
        os.environ["TAVILY_API_KEY"] = "dummy_key"

    # Mock DDGS.text to raise an exception (simulating 202 Ratelimit)
    with patch('src.integrations.search.DDGS.text') as mock_ddg:
        mock_ddg.side_effect = Exception("202 Ratelimit")
        
        # Mock _tavily_search to avoid real API call if we don't have a real key
        with patch('src.integrations.search._tavily_search') as mock_tavily:
            mock_tavily.return_value = [{"title": "Tavily Result", "href": "http://tavily.com", "body": "Success!"}]
            
            print("Running search_web('test query')...")
            results = search_web("test query")
            
            if results and results[0]["title"] == "Tavily Result":
                print("✅ Fallback to Tavily triggered correctly on DDG error.")
            else:
                print("❌ Fallback failed.")

if __name__ == "__main__":
    test_search_fallback()
