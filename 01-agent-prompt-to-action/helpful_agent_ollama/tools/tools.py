from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

# --- Tool 1: The Searcher ---
def search_web(query: str) -> dict:
    """
    Searches the web and returns a list of relevant URLs.
    Use this to find WHERE to look for information.
    """
    try:
        # Get top 5 results to have a good pool of sources
        results = list(DDGS().text(query, max_results=5))
        
        if not results:
            return {"status": "error", "message": "No results found."}

        # Return a clean list of sources for the LLM to choose from
        formatted_results = []
        for i, res in enumerate(results, 1):
            formatted_results.append(f"Source {i}: {res['title']} - {res['href']}")
            
        return {
            "status": "success",
            "sources": "\n".join(formatted_results),
            "raw_results": results # Keep raw data for the next tool if needed
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Tool 2: The Reader (The "Deep Dive") ---
def read_website(url: str) -> dict:
    """
    Visits a specific URL and scrapes its textual content.
    Use this to read the full details of a source found by search_web.
    """
    try:
        # Fake a browser user-agent to avoid being blocked by some sites
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse text with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Kill all script and style elements (removes javascript code/css)
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Truncate if too long (Ollama has limits, keep it under ~4000 chars of context per site)
        return {
            "status": "success",
            "content": text[:10000] + "... [content truncated]"
        }
    except Exception as e:
        return {"status": "error", "message": f"Could not read website: {str(e)}"}
