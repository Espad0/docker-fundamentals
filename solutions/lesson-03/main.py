"""hello-ai: a tiny stand-in for an AI service.

The "model" is a keyword counter, so the image stays small and builds fast.
The container parts work exactly the same for a real model.
"""
import os
import re

from fastapi import FastAPI
from pydantic import BaseModel

MODEL_NAME = os.getenv("MODEL_NAME", "keyword-sentiment-v1")
API_KEY = os.getenv("API_KEY")  # comes from outside the image at run time
POSITIVE = {"good", "great", "love", "excellent", "happy", "fast", "works"}
NEGATIVE = {"bad", "terrible", "hate", "slow", "broken", "sad", "crash"}

app = FastAPI(title="hello-ai")


class PredictRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME, "api_key_configured": API_KEY is not None}


@app.post("/predict")
def predict(req: PredictRequest):
    words = re.findall(r"[a-z']+", req.text.lower())
    score = sum(w in POSITIVE for w in words) - sum(w in NEGATIVE for w in words)
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return {"label": label, "score": score, "model": MODEL_NAME}
