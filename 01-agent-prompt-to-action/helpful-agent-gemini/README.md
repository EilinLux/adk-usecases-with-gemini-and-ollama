# Google ADK Agent: Helpful Assistant

This project implements a lightweight, search-enabled AI agent using the **Google Agent Development Kit (ADK)**. The agent is powered by Gemini, configured for robust network handling, and capable of retrieving real-time information via Google Search.


## 📂 Code Overview

The code initializes a conversational agent (`root_agent`) and wraps it in a runner (`InMemoryRunner`) to manage the execution loop. It follows a modular architecture where the **Model**, **Tools**, and **Agent** definitions are decoupled.

### Key Features

  * **Model:** Uses `gemini-2.5-flash-lite` for low latency and efficiency.
  * **Reliability:** Implements a custom exponential backoff retry strategy for API stability.
  * **Capabilities:** Equipped with `Google Search` to answer current-event questions.


### Dependencies

Ensure you have the Google ADK and GenAI libraries installed:

```bash
pip install google-adk google-genai
```

-----

## 🛠️ Class & Component Breakdown

Here is a detailed explanation of the classes used in this script and the reasoning behind their selection.

### 1\. Configuration: `types.HttpRetryOptions`

  * **Library:** `google.genai`
  * **Purpose:** Defines how the application handles API failures (e.g., rate limits or server timeouts).
  * **Why use it?** LLM applications often face transient network issues (HTTP 429/503). This configuration ensures the agent doesn't crash immediately but retries intelligently.
      * `attempts=5`: Tries the request up to 5 times.
      * `exp_base=7`: Uses **exponential backoff**, increasing the wait time significantly between retries to avoid overwhelming the server.

### 2\. The Model: `Gemini`

  * **Library:** `google.adk.models.google_llm`
  * **Purpose:** Acts as the interface between the agent and the underlying Large Language Model API.
  * **Why use it?**
      * It abstracts the API calls to the Google GenAI service.
      * **Model Selection:** `gemini-2.5-flash-lite` suggests a choice optimized for speed and cost-effectiveness, ideal for simple, high-frequency tasks.
      * **Integration:** It accepts the `retry_config` directly, applying the robustness defined above to every generation call.

### 3\. The Tool: `Google Search`

  * **Library:** `google.adk.tools`
  * **Purpose:** A pre-built function that allows the LLM to query the Google Search engine.
  * **Why use it?** LLMs have a training data cutoff. This tool provides **Grounding**, allowing the agent to fetch up-to-date information (news, weather, stock prices) that isn't in its internal memory.

### 4\. The Orchestrator: `Agent`

  * **Library:** `google.adk.agents`
  * **Purpose:** The core entity that holds the "persona" and logic.
  * **Why use it?** The `Agent` class binds the *brain* (Model) with the *hands* (Tools) and the *rules* (Instruction).
      * `instruction`: The system prompt ("You are a helpful assistant...") that governs behavior.
      * `tools`: The list of capabilities the agent is allowed to access.

### 5\. The Executor: `InMemoryRunner`

  * **Library:** `google.adk.runners`
  * **Purpose:** Manages the conversation state and execution flow.
  * **Why use it?**
      * **State Management:** It keeps track of the conversation history (context window) in the application's RAM (`InMemory`).
      * **Simplicity:** It requires no external database setup, making it perfect for testing, scripts, or stateless containerized applications.

-----

## 🚀 Usage

To run this agent, you would typically run `adk web .` at the `01-agent-prompt-to-action` level.

```bash
adk web .
```
Or to run this agent, you would invoke the `run` method on the runner instance (assuming standard ADK patterns):

```python
# Example of how to trigger the runner
user_input = "What is the stock price of Google today?"
response = runner.run(user_input)
print(response)
```