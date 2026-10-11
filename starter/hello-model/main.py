"""hello-model: sentiment analysis with a real transformer model.

The model loads in a background thread, so the server can answer health
checks while it loads: /health/live says "the process is up", /health/ready
says "the model is loaded and requests will work".
"""
import asyncio
import json
import os
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

MODEL_DIR = os.getenv("MODEL_DIR", "/models/sst2")
state = {"status": "starting", "error": None, "load_seconds": None, "torch_threads": None}
classifier = None


def load_model():
    global classifier
    started = time.perf_counter()
    try:
        if not Path(MODEL_DIR, "config.json").exists():
            state["status"] = "downloading"
            from download_model import download
            download(MODEL_DIR)
        state["status"] = "loading"
        import torch
        from transformers import pipeline  # importing these is part of the start-up cost

        classifier = pipeline("sentiment-analysis", model=MODEL_DIR, device="cpu")
        state["torch_threads"] = torch.get_num_threads()
        state["load_seconds"] = round(time.perf_counter() - started, 1)
        state["status"] = "ready"
        print(f"model ready in {state['load_seconds']} s", flush=True)
    except Exception as e:
        state.update(status="failed", error=repr(e))
        print("model failed to load:", repr(e), flush=True)


@asynccontextmanager
async def lifespan(app):
    threading.Thread(target=load_model, daemon=True).start()
    yield


app = FastAPI(title="hello-model", lifespan=lifespan)


class PredictRequest(BaseModel):
    text: str


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    body = {k: state[k] for k in ("status", "load_seconds", "torch_threads")}
    if state["status"] != "ready":
        return JSONResponse(body | {"error": state["error"]}, status_code=503)
    return body


@app.post("/predict")
def predict(req: PredictRequest):
    if classifier is None:
        return JSONResponse({"error": f"model is {state['status']}"}, status_code=503)
    started = time.perf_counter()
    result = classifier(req.text)[0]
    return {
        "label": result["label"].lower(),
        "score": round(result["score"], 4),
        "ms": round((time.perf_counter() - started) * 1000, 1),
    }


@app.get("/stream")
async def stream(text: str = "containers make AI apps portable"):
    """Send a reply piece by piece, the way LLM APIs stream tokens."""

    async def events():
        for word in f"You wrote: {text}. Streaming sends each piece as soon as it is ready.".split():
            yield f"data: {json.dumps({'token': word})}\n\n"
            await asyncio.sleep(0.3)
        yield "data: [DONE]\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")
