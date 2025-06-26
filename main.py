from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
import json
from guitar_agent import GuitarRecommendationAgent

app = FastAPI()

class GuitarPreferences(BaseModel):
    budget: Optional[float] = None
    style: Optional[str] = None  # e.g., acoustic, electric, classical
    brand_preference: Optional[str] = None
    features: List[str] = []  # e.g., "cutaway", "humbuckers"
    experience_level: Optional[str] = None  # beginner, intermediate, expert

class ProductRecommendation(BaseModel):
    guitar_id: str
    name: str
    price: float
    features: List[str]
    description: str
    score: float

# Initialize guitar recommendation agent
agent = GuitarRecommendationAgent()

# Mock guitar database (in production, this would be a real database)
GUITAR_DATABASE = [
    {
        "id": "1",
        "name": "Fender Stratocaster",
        "price": 1500,
        "style": "electric",
        "features": ["humbuckers", "tremolo", "cutaway"],
        "brand": "Fender",
        "level": "intermediate"
    },
    {
        "id": "2",
        "name": "Taylor 214ce",
        "price": 1800,
        "style": "acoustic",
        "features": ["cutaway", "electronics"],
        "brand": "Taylor",
        "level": "beginner"
    },
    # Add more guitars as needed
]

@app.post("/recommend/", response_model=List[ProductRecommendation])
async def recommend_guitars(preferences: GuitarPreferences):
    try:
        # Convert preferences to JSON string
        preferences_dict = preferences.dict()
        
        # Get recommendations from agent
        response = agent._recommend_products(json.dumps(preferences_dict))
        
        # Parse the response and convert to ProductRecommendation objects
        recommendations = json.loads(response)
        
        # Convert to our response model
        return [
            ProductRecommendation(
                guitar_id=rec['product_id'],
                name=rec['product_id'],  # This would need to be mapped to actual guitar names
                price=0.0,  # This would need to be mapped to actual prices
                features=[],  # This would need to be mapped to actual features
                description=rec['reason'],
                score=float(rec['score'])
            )
            for rec in recommendations['recommendations']
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/", response_model=Dict)
async def chat_with_agent(message: str):
    """Handle chat messages with the guitar recommendation agent"""
    try:
        response = agent.run_agent(message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
