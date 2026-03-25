import pickle
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


def _parse_allowed_origins():
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,https://cc-rep-2.onrender.com",
    )
    return [origin.strip().rstrip("/") for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("sentiment_model_v1.0_pkl", "rb") as file:
    sentiment_model = pickle.load(file)

class SentimentRequest(BaseModel):
    text: str

@app.post("/sentiment")
async def analyze_sentiment(payload: SentimentRequest):
    prediction = sentiment_model.predict([payload.text])[0]
    return {"sentiment": str(prediction)}
