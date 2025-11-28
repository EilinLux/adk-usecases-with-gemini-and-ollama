from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from .tools.tools import search_web, read_website

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