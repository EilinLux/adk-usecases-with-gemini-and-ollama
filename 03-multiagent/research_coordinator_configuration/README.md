# Multi-Agent Research & Summarization System

This project implements a **Hierarchical Multi-Agent System** using the Google Agent Development Kit (ADK). It demonstrates how to orchestrate specialized agents ("workers") under a central coordinator to perform complex workflows.

## 📋 System Overview

Instead of a single agent trying to do everything, this system splits responsibilities into three distinct roles. The **ResearchCoordinator** acts as the manager, dispatching tasks to the **ResearchAgent** and **SummarizerAgent** strictly via tool calls.

### The Workflow

1.  **User** asks a question.
2.  **Coordinator** calls the *Researcher* to fetch live data.
3.  **Researcher** saves findings to the shared state.
4.  **Coordinator** calls the *Summarizer* to process those findings.
5.  **Summarizer** reads the state and generates a bulleted list.
6.  **Coordinator** delivers the final result to the user.

-----

## 🏗️ Agent Architecture

### 1\. The Manager: `ResearchCoordinator` (Root Agent)

  * **Role:** Orchestrator. It does not perform research or summarization itself.
  * **Tools:** It uses `AgentTool` to access the other two agents.
  * **Logic:** Its system instruction acts as a strict Standard Operating Procedure (SOP), forcing it to call the Researcher first, then the Summarizer.

### 2\. The Worker: `ResearchAgent`

  * **Role:** Data Retrieval.
  * **Tools:** `Google Search`.
  * **Key Feature:** `output_key="research_findings"`.
      * When this agent finishes, it doesn't just return text to the coordinator; it injects its result into the global session state under the variable `research_findings`.

### 3\. The Processor: `SummarizerAgent`

  * **Role:** Data Synthesis.
  * **Tools:** None (Pure LLM).
  * **Key Feature:** Context Injection.
      * The instruction `"... provided research findings: {research_findings}"` automatically pulls the data saved by the ResearchAgent from the session state.

-----

## 🛠️ Key ADK Concepts Used

### `AgentTool`

This wrapper turns an entire `Agent` into a `Tool`. This allows the Root Agent to call "ResearchAgent" just like it would call a calculator or a search bar. This is the foundation of **Agentic Orchestration**.

### `output_key` & State Sharing

This allows for implicit data passing.

  * Instead of the Coordinator manually passing the text from Agent A to Agent B, Agent A saves it to memory (`output_key`), and Agent B reads it from memory in its prompt (`{variable}`).

### `types.HttpRetryOptions`

Configured with exponential backoff (`exp_base=7`) to handle potential API rate limits (`429`) or server errors (`503`) gracefully, ensuring the workflow doesn't break in the middle of a multi-step process.

-----

## 🚀 How to Run

### Using the ADK Web UI (Recommended)

This is the best way to visualize the orchestration. You will see the Coordinator "thinking" and choosing to trigger the sub-agents.

1.  Save the code as `agent.py`.
2.  Run in your terminal:
    ```bash
    adk web .
    ```
3.  Open `http://localhost:8000`.
4.  **Try this prompt:** "Find the latest developments in solid-state batteries."

### Using the Python Runner

To run it as a script without a UI:

```python
# Add this to the bottom of your script
user_query = "What are the latest updates on the James Webb Space Telescope?"
response = runner.run(user_query)

print("Final Response:", response.text)
```
