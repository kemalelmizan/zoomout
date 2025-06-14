# Zoomout — Planning Document

## Overview

**Zoomout** is a context-aware chatbot interface powered by local LLMs (via Ollama) that starts with simple conversation but gradually detects deeper structure and meaning in user interactions. It provides insights via three reasoning modes: **Cognition**, **Perspective**, and **Action**. As conversations evolve, the system "zooms out" to detect broader patterns (e.g., recognizing the Tower of Hanoi from indirect descriptions).

## Goals

* Build a lightweight offline-first chatbot interface
* Dynamically infer and surface higher-level structure from chat history
* Let users manually or automatically toggle between three cognitive modes
* Support Ollama models locally with ability to select model

## Modes of Reasoning

1. **Cognition** — understand structure, logic, and deeper meaning
2. **Perspective** — reframe, shift viewpoint, question assumptions
3. **Action** — give practical steps, plans, or strategies

## User Interface Design

### Default Behavior

* Start with basic chatbot UI
* System auto-selects one of the 3 modes based on context
* Response is shaped accordingly

### Mode Selection

* Auto + Smart Override is the preferred design
* Subtle label shows system-selected mode:

  > Mode: 🧠 Cognition | \[Change]
* Clicking \[Change] opens simple 3-option selector (radio or tabs)

### Advanced Control (Optional for Power Users)

* Add slider or triangular pad to blend modes
* Optionally include tone/warmth control:

  > Tone: ❄️ Cool | 🧊 Neutral | 🔥 Warm

## Technical Stack

### Backend (Python / FastAPI)

* Serves static frontend files
* Lists installed Ollama models (`ollama list`)
* Accepts chat POST requests with: message, model, and mode
* Prepends prompt with system message based on mode
* Runs `ollama run <model>` to get responses

### Frontend (HTML/JS)

* Simple form with:

  * Model dropdown (loaded from `/models`)
  * Mode selector
  * Chat history window
  * Input + send button

## API Endpoints

* `GET /` — Serve main chat interface
* `GET /models` — Return list of local Ollama models
* `POST /chat` — Accept message + mode + model, return model response

## Example Prompt Prefixes

* Cognition: *"Analyze this deeply: "*
* Perspective: *"Reframe this differently: "*
* Action: *"Suggest actionable next steps for this: "*

## Naming Rationale

**Zoomout**: The name emphasizes the core capability — stepping back from the surface level of user input to discover patterns, structure, and strategy underneath.

## Future Features (Optional Ideas)

* Auto-summary of detected task or structure (e.g. "This looks like Tower of Hanoi")
* Session memory, save/load past chats
* Warmth/tone tuning
* Visual metaphors (radar/spider chart of reasoning)
* React or mobile frontend

---

This `plan.md` document serves as the foundation for developing Zoomout. Next steps can include directory structure setup, React frontend planning, and persistence or session management.
