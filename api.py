from fastapi import FastAPI
from recommender import SHLRecommender
from pydantic import BaseModel

app = FastAPI()
recommender = SHLRecommender()

class Query(BaseModel):
    text: str
    top_k: int = 5

@app.post("/recommend")
async def recommend(query: Query):
    return {"recommendations": recommender.recommend(query.text, query.top_k)}

# Run with: uvicorn api:app --reload