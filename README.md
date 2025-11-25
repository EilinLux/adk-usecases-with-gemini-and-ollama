🤖 Local Product Catalog Agent

This project runs a local AI agent using the Google Agent Development Kit (ADK), Ollama (Llama 3.1), and DuckDuckGo for search. It uses uv for fast package management.

📋 Prerequisites

1. Install Ollama

Download and install Ollama from the official site:
👉 https://ollama.com/

After installing, pull the model you want to use (e.g., Llama 3.1):

ollama pull llama3.1


2. Install uv

If you don't have uv installed yet, install it (it's an extremely fast Python package manager):

Mac/Linux:

curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh


Windows (PowerShell):

powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"


🚀 Installation & Setup

1. Create the Environment

Create a new virtual environment named adk-enviroment using uv:

uv venv adk-enviroment


2. Activate the Environment

Activate the environment so your terminal uses the isolated Python version:

source adk-enviroment/Scripts/activate


(Note: If you are on standard Linux/Mac, the path is likely source adk-enviroment/bin/activate)

3. Install Libraries

Install all required dependencies into your environment using uv:

uv pip install -r requirements.txt


▶️ Running the Agent

Step 1: Start Ollama

Make sure Ollama is running in the background. If it isn't, open a new terminal and run:

ollama serve
