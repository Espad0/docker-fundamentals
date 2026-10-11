"""hello-ai: a tiny stand-in for an AI service.

The "model" is a keyword counter. If DATABASE_URL is set, every prediction
is also saved to Postgres, and GET /history returns the latest ones.
"""
import os
import re
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

MODEL_NAME = os.getenv("MODEL_NAME", "keyword-sentiment-v1")
API_KEY = os.getenv("API_KEY")  # comes from outside the image at run time
DATABASE_URL = os.getenv("DATABASE_URL")  # e.g. postgresql://user:pass@db:5432/hello
POSITIVE = {"good", "great", "love", "excellent", "happy", "fast", "works"}
NEGATIVE = {"bad", "terrible", "hate", "slow", "broken", "sad", "crash"}


def db():
    return psycopg.connect(DATABASE_URL, connect_timeout=3)


@asynccontextmanager
async def lifespan(app):
    if DATABASE_URL:
        with db() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS predictions (
                       id SERIAL PRIMARY KEY,
                       text TEXT NOT NULL,
                       label TEXT NOT NULL,
                       score INTEGER NOT NULL,
                       created_at TIMESTAMPTZ NOT NULL DEFAULT now())"""
            )
    yield


app = FastAPI(title="hello-ai", lifespan=lifespan)


class PredictRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    body = {"status": "ok", "model": MODEL_NAME, "api_key_configured": API_KEY is not None}
    if not DATABASE_URL:
        body["database"] = "not configured"
        return body
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        body["database"] = "connected"
        return body
    except psycopg.Error as e:
        body.update(status="error", database=f"unreachable: {e.__class__.__name__}")
        return JSONResponse(body, status_code=503)


@app.post("/predict")
def predict(req: PredictRequest):
    words = re.findall(r"[a-z']+", req.text.lower())
    score = sum(w in POSITIVE for w in words) - sum(w in NEGATIVE for w in words)
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    if DATABASE_URL:
        with db() as conn:
            conn.execute(
                "INSERT INTO predictions (text, label, score) VALUES (%s, %s, %s)",
                (req.text, label, score),
            )
    return {"label": label, "score": score, "model": MODEL_NAME}


@app.get("/history")
def history(limit: int = 10):
    if not DATABASE_URL:
        return JSONResponse({"error": "no database configured"}, status_code=404)
    with db() as conn:
        rows = conn.execute(
            "SELECT id, text, label, score, created_at FROM predictions ORDER BY id DESC LIMIT %s",
            (limit,),
        ).fetchall()
    return [
        {"id": r[0], "text": r[1], "label": r[2], "score": r[3], "created_at": r[4].isoformat()}
        for r in rows
    ]
