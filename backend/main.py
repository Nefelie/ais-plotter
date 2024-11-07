from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example DataFrame (replace this with your actual DataFrame)
data = {
    "longitude": [-0.1278, 2.3522, 13.4050],
    "latitude": [51.5074, 48.8566, 52.5200],
    "name": ["London", "Paris", "Berlin"],
}

df = pd.DataFrame(data)

# Pydantic models to structure the data
class Point(BaseModel):
    longitude: float
    latitude: float
    name: str

class PointsResponse(BaseModel):
    points: List[Point]

# FastAPI endpoint to get points as JSON
@app.get("/api/points", response_model=PointsResponse)
async def get_points():
    points_data = df.to_dict(orient="records")
    return {"points": points_data}
