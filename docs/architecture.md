# Zoomout — Architecture Document

## Overview
Zoomout is a context-aware chatbot interface powered by local LLMs (via Ollama), designed to provide insights through three reasoning modes: Cognition, Perspective, and Action. The system is built with an offline-first approach, using FastAPI for the backend and a simple HTML/JS frontend.

## System Components

### 1. Backend (Python / FastAPI)
- **Static File Serving**: Serves the frontend from the `static/` directory.
- **Model Management**: Lists available Ollama models by querying the local Ollama server.
- **Chat Endpoint**: Accepts chat requests, prepends a mode-specific system prompt, and invokes the selected Ollama model using a subprocess call.
- **Session Memory**: Maintains a simple in-memory chat history (per session, not persistent).

#### API Endpoints
- `GET /` — Serves the main chat interface (`static/index.html`).
- `GET /models` — Returns a list of available Ollama models.
- `POST /chat` — Accepts a message, mode, and model; returns the model's response.

#### Prompt Engineering
- Each reasoning mode uses a specific prefix:
  - Cognition: "Analyze this deeply: "
  - Perspective: "Reframe this differently: "
  - Action: "Suggest actionable next steps for this: "

### 2. Frontend (HTML/JS)
- **Model Selector**: Dropdown populated from `/models`.
- **Mode Selector**: Dropdown for Cognition, Perspective, or Action.
- **Chat Window**: Displays chat history.
- **Input Box**: For user messages.
- **Send Button**: Triggers chat request.

## Architecture Decisions

- **FastAPI** was chosen for its simplicity and async support.
- **Ollama Integration**: Uses subprocess for model invocation to keep dependencies minimal and leverage local LLMs.
- **Frontend Simplicity**: Pure HTML/JS for ease of use and offline capability.
- **No Persistent Storage**: Chat history is in-memory only; future versions may add session persistence.
- **Mode Handling**: Modes are handled via prompt prefixes, allowing flexible reasoning without complex prompt engineering.

## Missing Features & Recommendations

- **Session Persistence**: Currently, chat history is not saved. For multi-session support, implement persistent storage (e.g., SQLite, file-based, or browser localStorage).
- **Advanced Mode Blending**: The UI and backend support only one mode at a time. For blending modes, extend the prompt logic and UI (e.g., slider or triangular pad).
- **Tone/Warmth Control**: Not implemented. Add a UI selector and extend prompt prefixes for tone.
- **Auto-Detection of Structure**: Not implemented. Add logic to analyze chat history and surface detected patterns.
- **Frontend Enhancements**: Consider React or another framework for richer UI/UX.

## Directory Structure

- `main.py` — FastAPI backend
- `static/` — Frontend assets (HTML/JS)
- `docs/plan.md` — Planning document
- `docs/architecture.md` — (This file)

## Future Directions
- Add session memory and persistence
- Implement advanced mode blending and tone control
- Auto-summary and pattern detection
- Visual metaphors for reasoning modes
- Mobile or React frontend

---
This document describes the current architecture and highlights areas for future development based on the project plan.
