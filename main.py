from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import json
import os
import requests
import time
import re
from typing import Optional
from uuid import uuid4

app = FastAPI()

# Create static directory if not exists (for the frontend)
if not os.path.exists("static"):
    os.mkdir("static")

# Serve static files (for production build)
if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="dist")
else:
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple memory (per-session)
chat_history = []

# In-memory session chat history
def get_session_id(session_id: Optional[str]) -> str:
    if not session_id:
        return str(uuid4())
    return session_id

session_histories = {}

# Ollama tools
def list_ollama_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        return [model['name'] for model in data.get('models', [])]
    except Exception:
        return []

def chat_with_model(model: str, prompt: str) -> str:
    result = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True)
    return result.stdout.strip()

# Request schema
class ChatRequest(BaseModel):
    model: str
    mode: str  # normal, cognition, perspective, action
    message: str
    tone: Optional[str] = "neutral"  # cool, neutral, warm

@app.get("/", response_class=HTMLResponse)
async def index(response: Response, session_id: Optional[str] = Cookie(None)):
    sid = get_session_id(session_id)
    response.set_cookie(key="session_id", value=sid)
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/models")
async def get_models():
    models = list_ollama_models()
    return JSONResponse(content={"models": models})

@app.get("/history")
async def get_history(session_id: Optional[str] = Cookie(None)):
    sid = get_session_id(session_id)
    return JSONResponse(content={"history": session_histories.get(sid, [])})

@app.post("/chat")
async def chat(req: ChatRequest, session_id: Optional[str] = Cookie(None)):
    sid = get_session_id(session_id)
    tone_prefix = {
        "cool": "[Cool tone] ",
        "neutral": "",
        "warm": "[Warm and friendly tone] "
    }.get(req.tone or "neutral", "")
    system_prefix = {
        "normal": "",
        "cognition": "Analyze this deeply: ",
        "perspective": "Reframe this differently: ",
        "action": "Suggest actionable next steps for this: "
    }.get(req.mode, "")
    prompt = f"{tone_prefix}{system_prefix}{req.message}"
    start_time = time.time()
    response = chat_with_model(req.model, prompt)
    duration = time.time() - start_time
    # Estimate token count (simple whitespace split, or use regex for better accuracy)
    token_count = len(re.findall(r'\w+', response))
    tokens_per_second = token_count / duration if duration > 0 else 0
    session_histories.setdefault(sid, []).append({"user": req.message, "bot": response, "mode": req.mode, "tone": req.tone})
    return JSONResponse(content={
        "response": response,
        "metadata": {
            "token_count": token_count,
            "duration": duration,
            "tokens_per_second": tokens_per_second
        }
    })
