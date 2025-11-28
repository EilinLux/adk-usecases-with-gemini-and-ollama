# 💱 Smart Currency Converter Agent

This project implements a **Tool-Using Agent** (Function Calling) using the Google Agent Development Kit (ADK). Unlike previous examples that used other agents as tools, this example demonstrates how to connect **standard Python functions** to an LLM, allowing it to perform precise lookups and calculations.

## 🧠 System Architecture

This system bridges the gap between **Generative AI** (Creative/Reasoning) and **Deterministic Code** (Facts/Math).

**The Workflow:**

1.  **User Query:** "I want to transfer $100 USD to Euros using my platinum credit card."
2.  **Reasoning:** The Agent analyzes the request and realizes it needs two pieces of missing data: the *fee* for the card and the *exchange rate* for the currency.
3.  **Tool Execution:**
      * Calls `get_fee_for_payment_method("platinum credit card")` → Returns `0.02`.
      * Calls `get_exchange_rate("USD", "EUR")` → Returns `0.93`.
4.  **Synthesis & Math:** The Agent uses the retrieved data to calculate the final amount (`$100 * (1 - 0.02) * 0.93`) and generates a natural language explanation.

## 📂 Component Breakdown

### 1\. Custom Tools (Python Functions)

The ADK allows you to pass standard Python functions directly into the `tools` list.

  * **`get_fee_for_payment_method`:** Simulates an internal database lookup. It returns a dictionary with a status and a fee percentage.
  * **`get_exchange_rate`:** Simulates an external API call to a forex provider.
  * **Why use tools?** LLMs are bad at memorizing real-time data (like exchange rates) or specific business rules (like fees). Hard-coding these into functions ensures accuracy.

### 2\. The Brain: `LlmAgent`

  * **Name:** `currency_agent`
  * **Model:** `gemini-2.5-flash-lite`
  * **Instruction:** A strict step-by-step procedure. It explicitly tells the model to:
    1.  Call the tools.
    2.  Check for errors (defensive programming).
    3.  Perform the final calculation itself based on the tool outputs.

### 3\. Reliability: `HttpRetryOptions`

Financial queries often require high availability. The `retry_config` ensures that if the LLM API hiccups (Error 503) or is rate-limited (Error 429), the application retries intelligently with exponential backoff rather than crashing.

## 🗝️ Key Concept: Docstrings as Specifications

Notice how detailed the **Docstrings** (`"""..."""`) are inside the Python functions.

  * The ADK reads these docstrings to generate the **Tool Definition** that is sent to Gemini.
  * If you remove the docstring, the Agent won't know *how* or *when* to use the function.
  * **Best Practice:** Always include `Args:` and `Returns:` descriptions so the LLM knows exactly what data format to send and expect.

## 🚀 How to Run

### Option 1: ADK Web (Visual Debugger)

This is highly recommended for tool-use agents. You will see the agent pause, execute the Python code, receive the JSON result, and then continue generating text.

```bash
adk web .
```

### Option 2: Python Script

Append this to your file to test a complex scenario:

```python
# Test a complex query requiring both tools
query = "I need to convert 500 USD to EUR using a Platinum Credit Card. How much will I get?"
result = runner.run(query)

print("\n" + "="*50)
print("🤖 AGENT RESPONSE")
print("="*50 + "\n")
print(result.text)
```