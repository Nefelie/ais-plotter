from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
import logging
from fastapi.responses import JSONResponse

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Svelte app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

class Point(BaseModel):
    lon: float
    lat: float
    MMSI: int

class PointsResponse(BaseModel):
    points: List[Point]

# Function to load points from a static pickle file
def load_points_from_pickle(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_pickle(filepath)
        logger.debug(f"Loaded data from {filepath}: {df.head()}")
        return df
    except Exception as e:
        logger.error(f"Error loading DataFrame from pickle: {e}")
        return pd.DataFrame()

# GET endpoint to retrieve points from a static file
@app.get("/api/points", response_model=PointsResponse)
async def get_points():
    logger.debug("GET /api/points endpoint hit")
    filepath = "../AIS/maritime_graph/data/ships.pkl"  # Ensure this path is correct
    df = load_points_from_pickle(filepath)
    
    if not df.empty:
        try:
            if 'lat' not in df.columns or 'lon' not in df.columns or 'MMSI' not in df.columns:
                raise ValueError("Required columns ('lat', 'lon', 'MMSI') not found in the DataFrame.")
            df_transformed = df[['lat', 'lon', 'MMSI']].head(200000).copy()
            points_data = df_transformed.to_dict(orient="records")
            return PointsResponse(points=points_data)
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return PointsResponse(points=[])
    else:
        return PointsResponse(points=[])

# POST endpoint to upload and process a .pickle file
@app.post("/api/upload-pickle", response_model=PointsResponse)
async def upload_pickle(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()

        # Load the contents as a DataFrame
        df = pd.read_pickle(pd.io.common.BytesIO(contents))

        # Verify required columns
        if 'lat' not in df.columns or 'lon' not in df.columns or 'MMSI' not in df.columns:
            raise ValueError("Uploaded file must contain 'lat', 'lon', and 'MMSI' columns.")
        
        # Process the DataFrame
        df_transformed = df[['lat', 'lon', 'MMSI']].copy()
        points_data = df_transformed.to_dict(orient="records")

        return PointsResponse(points=points_data)

    except Exception as e:
        logger.error(f"Error processing uploaded pickle file: {e}")
        raise HTTPException(status_code=400, detail="Failed to process the uploaded pickle file.")
