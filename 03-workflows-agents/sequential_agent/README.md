
# 📝 Automated Blog Post Pipeline

This project builds a linear Content Generation Factory using the **Google Agent Development Kit (ADK)**. It utilizes the `SequentialAgent` class to enforce a strict, step-by-step workflow that mimics a real-world publishing process: Plan → Write → Edit.

## 🏗️ System Architecture

Unlike a Chatbot that reacts to users, this is a **Pipeline**. Once triggered, the data flows automatically from one agent to the next without human intervention until the final result is ready.

**The Pipeline Flow:**

1.  **Input:** User provides a topic (e.g., "Benefits of Green Tea").
2.  **Step 1 (Outline):** Generates the structure.
3.  **Step 2 (Draft):** Expands structure into paragraphs.
4.  **Step 3 (Edit):** Polishes the text for publication.

## 📂 Component Breakdown

### 1\. The Manager: `SequentialAgent`

  * **Name:** `root_agent` / `BlogPipeline`
  * **Role:** The Conveyor Belt.
  * **Why use it?** You typically use a standard `Agent` when the AI needs to decide *what* to do next. You use a `SequentialAgent` when **YOU** know exactly what order the steps must happen in. It guarantees `Outline` finishes before `Writer` starts.

### 2\. The Planner: `OutlineAgent`

  * **Input:** User prompt.
  * **Instruction:** Focuses purely on structure (headlines, bullet points).
  * **Output:** Saves to state key `blog_outline`.

### 3\. The Author: `WriterAgent`

  * **Input:** Reads `{blog_outline}` from memory.
  * **Instruction:** Focuses on tone, expansion, and word count (200-300 words).
  * **Output:** Saves to state key `blog_draft`.

### 4\. The Critic: `EditorAgent`

  * **Input:** Reads `{blog_draft}` from memory.
  * **Instruction:** Focuses on grammar, flow, and clarity.
  * **Output:** Saves to state key `final_blog`.

## 🗝️ Key Concept: State Injection

The magic of this code lies in how the agents talk to each other without direct function calls. This is done via **Prompt Template Injection**.

  * **Agent 1** saves data: `output_key="blog_outline"`
  * **Agent 2** reads data: `instruction="... strictly: {blog_outline} ..."`

The ADK automatically finds the variable `blog_outline` in the session's memory and replaces `{blog_outline}` in the Writer's instruction before sending it to the LLM. If you make a typo in the key name, the pipeline will break because the Writer won't know what to write about.

## 🚀 How to Run

### Option 1: Terminal (ADK Web)

The easiest way to visualize the pipeline steps.

1.  Save the file as `agent.py`.
2.  Run `adk web .` in your terminal.
3.  Open `http://localhost:8000`.
4.  Type a topic like "The history of coffee" and watch the agents hand off the task.

### Option 2: Python Script

Add this snippet to the bottom of your file to run it immediately:

```python
# Trigger the pipeline
topic = "The importance of daily exercise"
result = runner.run(topic)

# The result contains the output of the LAST agent in the chain
print("\n--- Final Blog Post ---\n")
print(result.text)
```