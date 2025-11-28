import torch
from transformers import pipeline
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# --- 1. THE ENSEMBLE ENGINE ---
class SentimentEnsemble:
    def __init__(self):
        print("⏳ Loading Ensemble Models (this loads 3 different neural nets)...")
        
        # Model 1: Specialized for Finance (The "Professional")
        self.finbert = pipeline(
            "sentiment-analysis", 
            model="ProsusAI/finbert",
            return_all_scores=True
        )
        
        # Model 2: Specialized for Social Media/News (The "Public Opinion")
        self.roberta = pipeline(
            "sentiment-analysis", 
            model="cardiffnlp/twitter-roberta-base-sentiment-latest", 
            return_all_scores=True
        )
        
        # Model 3: Generic English (The "Baseline")
        self.generic = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )
        print("✅ Ensemble Engine Ready.")

    def _get_top_score(self, raw_output, model_type):
        """Helper to parse different model output formats"""
        # Sort by score descending
        sorted_scores = sorted(raw_output[0], key=lambda x: x['score'], reverse=True)
        top = sorted_scores[0]
        
        # Normalize labels (FinBERT uses 'positive', RoBERTa uses 'Positive', etc.)
        label = top['label'].lower()
        if model_type == 'roberta':
            # RoBERTa labels are usually 'positive', 'neutral', 'negative'
            pass 
        return f"{label} ({top['score']:.4f})"

    def analyze(self, text: str) -> dict:
        """Runs all 3 models on the same text."""
        res_fin = self.finbert(text)
        res_rob = self.roberta(text)
        res_gen = self.generic(text)
        
        return {
            "model_1_finbert_institutional": self._get_top_score(res_fin, 'finbert'),
            "model_2_roberta_social": self._get_top_score(res_rob, 'roberta'),
            "model_3_distilbert_generic": self._get_top_score(res_gen, 'generic')
        }

# Initialize once
ensemble = SentimentEnsemble()


# --- 2. THE TOOLS ---

def analyze_market_sentiment(headline: str) -> str:
    """
    Runs a multi-model sentiment analysis on a financial headline.
    Returns a dictionary comparison of how different AI models view the text.
    """
    try:
        results = ensemble.analyze(headline)
        return str(results)
    except Exception as e:
        return f"Ensemble Error: {e}"

def validate_topic(topic: str) -> str:
    """
    Strictly checks if a topic is related to finance, stocks, crypto, or economics.
    Returns 'APPROVED' or 'REJECTED'.
    """
    # Simple keyword filter for demo speed (In prod, use an LLM classifier)
    keywords = ['stock', 'market', 'price', 'usd', 'bitcoin', 'revenue', 'profit', 'loss', 'inflation', 'fed', 'trade', 'buy', 'sell']
    if any(k in topic.lower() for k in keywords):
        return "APPROVED"
    return "REJECTED"


# --- 3. THE AGENT ---
retry_config = types.HttpRetryOptions(attempts=3, exp_base=2, initial_delay=1)

root_agent = Agent(
    name="HedgeFundAnalyst",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="A multi-model financial analyst.",
    instruction="""
    You are a Senior Quantitative Analyst.
    
    YOUR WORKFLOW:
    1.  **Filter**: Check the user's input using the `validate_topic` logic (conceptually). 
        - If the user asks about non-finance topics (e.g., "Best pizza recipe"), politely REFUSE to answer.
    
    2.  **Analyze**: If finance-related, call `analyze_market_sentiment` with the text.
    
    3.  **Synthesize (The Unique Commentary)**:
        - You will receive results from 3 different AI brains (FinBERT, RoBERTa, DistilBERT).
        - **Compare them**: Do they agree? 
        - **Explain the "Why"**: 
            - If FinBERT (Pro) says "Negative" but RoBERTa (Social) says "Positive", explain that *institutional sentiment is bearish while retail hype is high*.
            - If all agree, state that the signal is "Strong & Unanimous".
    
    OUTPUT FORMAT:
    - **Consensus**: [Bullish/Bearish/Mixed]
    - **Model Breakdown**: [List the 3 scores]
    - **Analyst Commentary**: [Your synthesis of the discrepancy]
    """,
    tools=[analyze_market_sentiment, validate_topic]
)

# --- 4. RUNNER ---
runner = InMemoryRunner(agent=root_agent)

if __name__ == "__main__":
    print("\n📈 Hedge Fund Desk Active...\n")
    
    # TEST CASE 1: A tricky headline (Good revenue but missed expectations)
    # This often confuses generic models but FinBERT catches the nuance.
    headline = "Company X reports record revenue of $5B, but misses EPS targets by 10% amid supply chain fears."
    
    print(f"Analyzing: '{headline}'\n")
    response = runner.run(headline)
    print(response.text)