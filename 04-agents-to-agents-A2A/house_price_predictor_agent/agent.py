import numpy as np
from sklearn.linear_model import LinearRegression
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# --- 1. THE ML MODEL ENGINE ---
class PricePredictor:
    def __init__(self):
        print("⏳ Training ML Price Model (Simulation)...")
        # Synthetic Training Data
        # Features: [SqFt, Bedrooms, Location_Score(1-10)]
        X_train = np.array([
            [800, 1, 3],   # Small, bad location
            [1200, 2, 5],  # Average
            [1500, 3, 6],  # Family home
            [2500, 4, 8],  # Luxury
            [3500, 5, 10], # Mansion, prime location
        ])
        # Target: Price in $
        y_train = np.array([150_000, 280_000, 350_000, 650_000, 1_200_000])

        # Train a Linear Regression model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        print("✅ ML Model Trained and Ready.")

    def predict(self, sqft: int, beds: int, location_score: int) -> float:
        # Prepare input vector
        features = np.array([[sqft, beds, location_score]])
        # Run inference
        predicted_price = self.model.predict(features)[0]
        return round(predicted_price, 2)

# Initialize the model instance
ml_engine = PricePredictor()


# --- 2. THE TOOL ---
def estimate_house_value(sq_ft: int, bedrooms: int, location_rating: int) -> str:
    """
    Calculates the estimated market value of a property using a trained Linear Regression model.

    Args:
        sq_ft: Total square footage of the house (e.g., 1500).
        bedrooms: Number of bedrooms (e.g., 3).
        location_rating: A score from 1 (Rural/Bad) to 10 (Prime City Center).
    """
    try:
        price = ml_engine.predict(sq_ft, bedrooms, location_rating)
        return f"ML Model Output: ${price:,.2f}"
    except Exception as e:
        return f"Prediction Error: {str(e)}"


# --- 3. THE AGENT ---
retry_config = types.HttpRetryOptions(attempts=3, exp_base=2, initial_delay=1, http_status_codes=[429, 500])

root_agent = Agent(
    name="RealEstateAnalyst",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Analyzes property descriptions and predicts value.",
    instruction="""
    You are a Real Estate Valuation Expert.
    
    YOUR GOAL:
    Estimate property prices based on user descriptions.

    WORKFLOW:
    1.  **Extract Data**: Read the user's message and identify:
        - Square Footage (approximate if not exact)
        - Number of Bedrooms
        - Location Quality (Infer this on a scale of 1-10. e.g., "Downtown/Luxury" = 9-10, "Suburbs" = 5-6, "Remote" = 1-3).
    
    2.  **Missing Info**: If any of these 3 are missing, ASK the user for them. Do not guess.
    
    3.  **Predict**: Once you have all 3, call the `estimate_house_value` tool.
    
    4.  **Explain**: Present the price to the user and explain *why* the location rating you chose affected the price.
    """,
    tools=[estimate_house_value]
)

# --- 4. RUNNER ---
runner = InMemoryRunner(agent=root_agent)

if __name__ == "__main__":
    print("\n🏡 Real Estate Agent Running...\n")
    
    # Scenario 1: The user gives all info naturally
    user_input = "I have a large 4-bedroom house, about 2800 sq ft, located in a very exclusive, prime neighborhood."
    
    print(f"User: {user_input}")
    response = runner.run(user_input)
    print(f"Agent:\n{response.text}")