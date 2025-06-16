# Zoomout

Zoomout is a context-aware chatbot interface powered by local LLMs (via Ollama), with UI served by FastAPI.

## Features
- Three reasoning modes: Cognition, Perspective, Action
- Tone control (Cool, Neutral, Warm)
- Local Ollama model selection
- Modern, responsive chat UI

## Quickstart

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- Ollama running locally (see https://ollama.com/)

### 2. Clone and Setup
```sh
git clone <this-repo-url>
cd zoomout
```

### 3. Development
Run both backend and frontend with one command:
```sh
uv venv
source .venv/bin/activate
uv pip install .
uvicorn main:app --host 0.0.0.0 --port 8000
```
- Visit http://localhost:8000 (served from /static)

## Project Structure
- `main.py` — FastAPI backend
- `docs/` — Planning and architecture docs

## Notes
- Ollama must be running locally for model listing and chat.
- API endpoints: `/models`, `/chat`, `/history`

---
See `docs/plan.md` and `docs/architecture.md` for more details.
