import yaml
import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
from google.genai import types

# 1. Load the YAML Config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), './config/agents.yaml')

with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

# 2. Setup Shared Model Configuration
retry_settings = config['settings']['retry_config']
retry_options = types.HttpRetryOptions(
    attempts=retry_settings['attempts'],
    exp_base=retry_settings['exp_base'],
    initial_delay=retry_settings['initial_delay'],
    http_status_codes=retry_settings['http_status_codes']
)

def get_model():
    """Helper to return a fresh model instance with config applied."""
    return Gemini(
        model=config['settings']['model_name'],
        retry_options=retry_options
    )

# 3. Define a registry of standard tools
# Maps the string name in YAML to the actual Python function
TOOL_REGISTRY = {
    "google_search": google_search
}

# Dictionary to hold created agent instances
created_agents = {}

def build_agent(agent_key):
    """
    Recursively builds an agent from the YAML config.
    """
    if agent_key in created_agents:
        return created_agents[agent_key]

    agent_cfg = config['agents'][agent_key]
    
    # Resolve Tools
    resolved_tools = []
    for tool_name in agent_cfg.get('tools', []):
        if tool_name in TOOL_REGISTRY:
            # It's a standard function tool (like google_search)
            resolved_tools.append(TOOL_REGISTRY[tool_name])
        elif tool_name in config['agents']:
            # It's another AGENT referenced as a tool (Sub-agent)
            # Recursively build that agent first
            sub_agent = build_agent(tool_name)
            # Wrap it in AgentTool so the parent can call it
            resolved_tools.append(AgentTool(sub_agent))
        else:
            print(f"⚠️ Warning: Tool '{tool_name}' not found in registry or agent list.")

    # Create the Agent
    new_agent = Agent(
        name=agent_cfg['name'],
        model=get_model(),
        instruction=agent_cfg['instruction'],
        tools=resolved_tools,
        output_key=agent_cfg.get('output_key', None) # Optional
    )
    
    # Register and return
    created_agents[agent_key] = new_agent
    print(f"✅ Built Agent: {agent_cfg['name']}")
    return new_agent

# 4. Build the Root Agent
# This triggers the chain reaction to build the sub-agents (researcher/summarizer) automatically
root_agent = build_agent('root_agent')

# 5. Initialize Runner
runner = InMemoryRunner(agent=root_agent)

# --- Usage Example ---
if __name__ == "__main__":
    if os.environ.get("GOOGLE_API_KEY"):
        print("\n🤖 Pipeline Ready. Running Query...\n")
        response = runner.run("What are the latest breakthroughs in solid-state batteries?")
        print(response.text)
    else:
        print("❌ Error: GOOGLE_API_KEY not found in environment.")