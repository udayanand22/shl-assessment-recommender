from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend_assessments

app = FastAPI()

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/recommendations")
async def recommend_endpoint(req: RecommendationRequest):
    recommendations = recommend_assessments(req.query, req.top_k)
    return {"recommendations": recommendations}
