import os
import pickle
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "sentiment_model_v1.0_pkl"))
sentiment_model = None


def _parse_allowed_origins():
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "https://cc-rep-2-backend-git-cloud-computing-2026.2.rahtiapp.fi/",
    )
    return [origin.strip().rstrip("/") for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_model():
    global sentiment_model

    if sentiment_model is not None:
        return sentiment_model

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at '{MODEL_PATH}'. Set MODEL_PATH or deploy sentiment_model_v1.0_pkl."
        )

    with MODEL_PATH.open("rb") as file:
        sentiment_model = pickle.load(file)

    return sentiment_model

class SentimentRequest(BaseModel):
    text: str


@app.post("/sentiment")
async def analyze_sentiment(payload: SentimentRequest):
    try:
        model = _load_model()
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {error}") from error

    prediction = model.predict([payload.text])[0]
    return {"sentiment": str(prediction)}
