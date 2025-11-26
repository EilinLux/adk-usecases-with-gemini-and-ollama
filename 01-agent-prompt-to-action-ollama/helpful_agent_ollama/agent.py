import requests
from bs4 import BeautifulSoup
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from duckduckgo_search import DDGS

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
            "content": text[:4000] + "... [content truncated]"
        }
    except Exception as e:
        return {"status": "error", "message": f"Could not read website: {str(e)}"}

# --- Configuration ---
ollama_model = LiteLlm(
    model="ollama_chat/llama3.1:8b", 
    api_base="http://localhost:11434",
    temperature=0.3 # Slightly higher temp for better writing flow
)

# --- The "Journalist" Agent ---
root_agent = Agent(
    name="investigative_journalist",
    model=ollama_model,
    description="A thorough researcher that reads full articles before answering.",
    instruction="""You are a senior investigative researcher. Your goal is to write a comprehensive, professional report.

    YOUR WORKFLOW:
    1.  **Search**: Use `search_web` to find relevant pages.
    2.  **Select**: Pick the 1-2 most promising URLs from the search results (look for reliable sources like gov, edu, or major news).
    3.  **Read**: Use `read_website` on those specific URLs to extract the full content.
    4.  **Synthesize**: Write your final answer based on the *full content* you read, not just the search snippets.
    
    OUTPUT RULES:
    * Do NOT output a numbered list of "Result 1, Result 2".
    * Write in coherent paragraphs.
    * Synthesize the information into a single narrative.
    * If sources disagree, mention the discrepancy.
    * Cite your sources naturally (e.g., "According to the official gov.cn portal...").
    """,
    tools=[search_web, read_website],
)

runner = InMemoryRunner(agent=root_agent)