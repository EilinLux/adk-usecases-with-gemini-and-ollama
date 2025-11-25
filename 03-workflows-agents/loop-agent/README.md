# 🔄 Iterative Story Refinement Agent

This project implements an advanced **Agentic Workflow** using the Google Agent Development Kit (ADK). It mimics a professional editorial process where a writer, a critic, and an editor work together in a loop to refine a story until it meets a specific quality standard.

## 🧠 System Architecture

The workflow is orchestrated using a `SequentialAgent` that manages a linear pipeline containing a `LoopAgent`.

**The Flow:**

1.  **Drafting Phase:** The `InitialWriterAgent` creates the raw story.
2.  **Refinement Loop:** The system enters a cycle (managed by `LoopAgent`) where:
      * The **Critic** evaluates the draft.
      * The **Refiner** improves the draft *or* decides to stop.
3.  **Completion:** The loop exits when the story is "APPROVED" or the max iterations are reached.

## 📂 Agent & Component Breakdown

### 1\. `InitialWriterAgent` (The Creator)

  * **Role:** Generates the first draft.
  * **Output:** Saves the text to the session state key `current_story`.
  * **Why:** This runs only once outside the loop to establish the baseline content.

### 2\. `StoryRefinementLoop` (The Engine)

  * **Type:** `LoopAgent`
  * **Role:** repeatedly executes the `Critic` and `Refiner` in that specific order.
  * **Safety Net:** `max_iterations=2` is set to prevent infinite loops (and infinite costs) if the agents can't agree.

### 3\. `CriticAgent` (The Judge)

  * **Role:** Reads `{current_story}` and produces feedback.
  * **Output:** Saves feedback to the session state key `critique`.
  * **Logic:** It is strictly instructed to output the exact string `"APPROVED"` if the story is good. This specific string is the trigger for the next agent.

### 4\. `RefinerAgent` (The Editor)

  * **Role:** Reads both `{current_story}` and `{critique}`.
  * **Tools:** Equipped with the `exit_loop` tool.
  * **Logic:**
      * If `critique == "APPROVED"` → Calls `exit_loop()`.
      * Otherwise → Rewrites the story and **overwrites** the `current_story` key. This "in-place" editing is crucial for the loop to work on the updated version in the next round.

## 🛠️ Setup & Usage

### Prerequisites

You must have a Google GenAI API key. Set it in your environment:

```bash
export GOOGLE_API_KEY="your_key_here"
```

### Running the Code

Since this script uses `InMemoryRunner`, you can run it directly with Python or use the ADK CLI.

**Option 1: Python Script**
Add this to the bottom of your file to trigger the interaction:

```python
user_input = "Write a suspenseful story about a lost watch."
result = runner.run(user_input)
print(result.text)
```

**Option 2: ADK Web UI**
Run the built-in visual debugger to see the loop in action:

```bash
adk web .
```

## ⚠️ Important Configuration Details

  * **State Keys:** The workflow relies on `output_key`. If you change `current_story` in the Writer but forget to update it in the Critic's prompt, the Critic will hallucinate or fail.
  * **Exit Condition:** The `RefinerAgent` is the **only** agent capable of stopping the loop early. It must be explicitly told (via instructions) when to call the `exit_loop` tool.