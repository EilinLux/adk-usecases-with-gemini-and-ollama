# 🤖 Google ADK Agent Collection

This repository contains a collection of AI agents built with the **Google Agent Development Kit (ADK)**. It showcases various agent architectures ranging from simple chatbots to complex, multi-agent workflows including loops, parallel processing, and code execution.

## 📦 Directory Overview

### 🖥️ Local Product Catalog Agent (Ollama + Llama 3.1)

This project runs a local AI agent using the Google Agent Development Kit (ADK), Ollama (Llama 3.1), and DuckDuckGo for search. It uses `uv` for fast package management.

#### 📋 Prerequisites

**1. Install Ollama**
Download and install Ollama from the official site:
👉 [https://ollama.com/](https://ollama.com/)

After installing, pull the model you want to use (e.g., Llama 3.1):

```bash
ollama pull llama3.1
```

**2. Install uv**
If you don't have `uv` installed yet, install it (it's an extremely fast Python package manager):

*Mac/Linux:*

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

*Windows (PowerShell):*

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 🚀 Installation & Setup

**1. Create the Environment**
Create a new virtual environment named `adk-enviroment` using `uv`:

```bash
uv venv adk-enviroment
```

**2. Activate the Environment**
Activate the environment so your terminal uses the isolated Python version:

*Windows:*

```bash
source adk-enviroment/Scripts/activate
```

*Mac/Linux:*

```bash
source adk-enviroment/bin/activate
```

**3. Install Libraries**
Install all required dependencies into your environment using `uv`:

```bash
uv pip install -r requirements.txt
```

#### ▶️ Running the Agent

**Step 1: Start Ollama**
Make sure Ollama is running in the background. If it isn't, open a new terminal and run:

```bash
ollama serve
```

**Step 2: Run the Agent**

```bash
# Assuming your file is named agent.py
python agent.py
```

-----

### ☁️ Cloud-Based Gemini Agents (Google ADK)

The following agents utilize Google's **Gemini 2.5 Flash** models. To run these, you must set your API key in .env file :

```bash
GOOGLE_API_KEY="your_api_key_here"
```

You can run any of these using the ADK Web UI:

```bash
adk web .
```

#### 1\. Helpful Assistant (Basic)

  * **Architecture:** Single Agent.
  * **Features:** Google Search tool.
  * **Description:** The "Hello World" of ADK. A simple conversational agent wrapped in an `InMemoryRunner` that can answer general questions and search the web.

#### 2\. Research & Summarization System

  * **Architecture:** Hierarchical (Coordinator → Workers).
  * **Features:** `AgentTool`, Context Injection.
  * **Description:** A `ResearchCoordinator` manages two sub-agents: a `ResearchAgent` (that fetches data) and a `SummarizerAgent` (that processes it). Demonstrates how to pass data between agents using session state keys.

#### 3\. Iterative Story Refinement

  * **Architecture:** Loop (`LoopAgent`).
  * **Features:** Feedback Cycles, Exit Conditions.
  * **Description:** A creative writing workflow where a `CriticAgent` and `RefinerAgent` work in a loop. The loop continues until the Critic explicitly approves the story or the maximum iteration count is reached.

#### 4\. Automated Blog Pipeline

  * **Architecture:** Sequential (`SequentialAgent`).
  * **Features:** Linear Workflow.
  * **Description:** A strict manufacturing line for content: `OutlineAgent` → `WriterAgent` → `EditorAgent`. Guarantees a specific order of operations for high-quality content generation.

#### 5\. Parallel Research System

  * **Architecture:** Fan-Out / Fan-In (`ParallelAgent`).
  * **Features:** Concurrency.
  * **Description:** Drastically reduces wait times by running three specialized agents (`Tech`, `Health`, `Finance`) simultaneously. An `AggregatorAgent` waits for all three to finish before synthesizing a final report.

#### 6\. Smart Currency Converter

  * **Architecture:** Tool Use (Function Calling).
  * **Features:** Python Functions as Tools.
  * **Description:** Connects the LLM to standard Python functions (`get_fee`, `get_exchange_rate`) to retrieve specific data, then uses the LLM to explain the result.

#### 7\. Enhanced Currency Converter

  * **Architecture:** Delegation & Code Execution.
  * **Features:** `BuiltInCodeExecutor`.
  * **Description:** An advanced version of the currency converter. Instead of the LLM doing the math (which can be error-prone), it delegates the calculation to a `CalculationAgent` which writes and executes real Python code to ensure mathematical precision.



-----

### ☁️ Cloud-Based Ollama Agents (Google ADK)