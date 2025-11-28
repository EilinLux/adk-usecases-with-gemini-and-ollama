# 💱 Enhanced Currency Converter with Code Execution

This project implements a **Multi-Agent System with Code Execution** using the Google Agent Development Kit (ADK). It advances the previous tool-use concept by delegating arithmetic operations to a specialized coding agent, ensuring mathematical precision.

## 🧠 System Architecture

This system uses a **Delegation Pattern**. The main agent acts as a generalist that gathers information, while a specialist agent handles the computation using actual Python code.

**The Workflow:**

1.  **Data Gathering:** The `enhanced_currency_agent` calls the Python function tools (`get_fee_for_payment_method`, `get_exchange_rate`) to get the raw numbers.
2.  **Delegation:** Instead of calculating the result itself, the main agent calls the `calculation_agent`.
3.  **Code Execution:** The `calculation_agent` generates a Python script to perform the math and runs it using the `BuiltInCodeExecutor`.
4.  **Final Output:** The exact result from the code execution is passed back to the main agent, which presents it to the user.

## 📂 Component Breakdown

### 1\. `calculation_agent` (The Specialist)

  * **Role:** Mathematical Engine.
  * **Capability:** `code_executor=BuiltInCodeExecutor()`.
  * **Instruction:** Strictly prompted to output **only** Python code. It does not chat; it computes.
  * **Why?** It ensures that `100 * (1 - 0.02) * 0.93` is calculated by a Python interpreter, not predicted by a language model.

### 2\. `enhanced_currency_agent` (The Manager)

  * **Role:** Orchestrator.
  * **Tools:**
      * `get_fee_for_payment_method`: Looks up fees.
      * `get_exchange_rate`: Looks up rates.
      * `AgentTool(calculation_agent)`: Access to the specialist.
  * **Instruction:** Explicitly forbidden from doing math ("You are strictly prohibited from performing any arithmetic calculations yourself").

-----

## 🆚 Difference: This Version vs. The Previous Version

The key difference lies in **Reliability vs. Simplicity**.

| Feature | Previous Version (Single Agent) | This Version (Enhanced w/ Code Exec) |
| :--- | :--- | :--- |
| **Math Engine** | **LLM Prediction:** The model "guesses" the next token. For simple math ($100 - 2%), it works. For complex floating-point math, it often hallucinates (e.g., saying 2+2=5). | **Python Interpreter:** The model writes code (`print(100 * 0.98)`). The ADK runs this code. The result is mathematically guaranteed to be correct. |
| **Architecture** | **Flat:** One agent does everything (Tools + Reasoning + Math). | **Hierarchical:** The Root Agent handles the flow; the Sub-Agent handles the specific task of computation. |
| **Complexity** | Lower. Easier to setup. | Higher. Requires managing multiple agents and a safe code execution environment. |
| **Use Case** | Estimations, simple logic, summaries. | Financial calculations, data analysis, scientific computing. |

### Why change it?

In the previous version, if you asked to convert "1,234,567.89 USD to JPY", the LLM might struggle to multiply that large number by `157.50` accurately. In this version, the `calculation_agent` simply writes `print(1234567.89 * 157.50)`, which Python calculates instantly and perfectly.

## 🚀 How to Run

### Using ADK Web (Visual Debugger)

Run `adk web .` to see the hierarchy in action:

1.  You will see `enhanced_currency_agent` call the fee/rate tools.
2.  Then, you will see a distinct step where it calls `CalculationAgent`.
3.  Inside `CalculationAgent`, you will see a **Code Block** appear and execute.
4.  The final result returns to the top for the summary.

### Python Script

Add this to the bottom of your file:

```python
# Test the full delegation flow
query = "Convert 5000 USD to EUR using a Platinum Credit Card."
result = runner.run(query)

print("\n" + "="*50)
print("🤖 FINAL RESPONSE")
print("="*50 + "\n")
print(result.text)
```