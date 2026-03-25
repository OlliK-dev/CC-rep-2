import pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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