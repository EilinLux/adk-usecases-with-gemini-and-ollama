from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from duckduckgo_search import DDGS

# 1. Define the custom search tool
def web_search(query: str) -> str:
    """
    Searches the web for the given query and returns the top result.
    Use this tool when you need current information or facts.
    """
    try:
        results = DDGS().text(query, max_results=1)
        if results:
            return f"Title: {results[0]['title']}\nLink: {results[0]['href']}\nSnippet: {results[0]['body']}"
        return "No results found."
    except Exception as e:
        return f"Search failed: {e}"

# 2. Configure Ollama
ollama_model = LiteLlm(
    model="ollama_chat/llama3", 
    api_base="http://localhost:11434",
    temperature=0
)

# 3. Create the Agent with the NEW tool
root_agent = Agent(
    name="helpful_assistant",
    model=ollama_model,
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use the 'web_search' tool for current info.",
    tools=[web_search],  # Pass your custom function here
)

runner = InMemoryRunner(agent=root_agent)