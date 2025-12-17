---
applyTo: "**"
---

# Copilot instructions (agentcon-pizza-workshop)

## Big picture
- This repo has **two tracks**:
  - **Workshop scripts** in `workshop/` (standalone Python that interacts with Microsoft Foundry / Azure AI).
  - **VOLK web UI** in `src/`:
    - `src/server/` is a **FastAPI** app that talks to Azure AI Agents.
    - `src/client/` is a **static HTML/CSS/JS** frontend served by the FastAPI server.

## Web UI architecture (001-web-ui)
- Server entrypoint: `src/server/app.py` mounts `src/client/` at `/` and exposes an API under `/api/session/*`.
- API routes live in `src/server/routes/session_routes.py`:
  - `POST /api/session/start` creates an Azure AI Agent + thread and stores IDs in memory.
  - `POST /api/session/message` sends a user message to the thread and returns the agent’s reply.
  - `POST /api/session/end` best-effort deletes the agent and clears the session.
- Session persistence is **in-memory** only via `src/server/session_store.py` (thread-safe dict).
  - Restarting the server resets sessions.
  - The browser UI persists state in `localStorage` (`src/client/app.js`), so a stale `sessionId` can exist after a server restart; `/start` will create a new backing agent/thread when needed.
- Azure AI integration and tool wiring is in `src/server/agent_session.py`:
  - Reads agent instructions from `workshop/instructions.txt`.
  - Adds tools: File Search (vector store), a Python function from `workshop/tools.py`, and an MCP tool.
- Error handling is standardized via `src/server/errors.py` and the FastAPI exception handler in `src/server/app.py`.

## Key configuration (env vars)
- Required:
  - `PROJECT_CONNECTION_STRING` (used by `AIProjectClient` in `src/server/agent_session.py`).
- Optional:
  - `VECTOR_STORE_ID` (defaults to a hard-coded dev value in `src/server/agent_session.py`).
  - `PIZZA_MCP_SSE_URL` (defaults to the containerapps SSE URL in `src/server/agent_session.py`).
  - `PIZZA_MODEL` (defaults to `gpt-4o`).
- Local dev uses `.env` (loaded via `python-dotenv`); `.env` is gitignored. Start from `.env.example`.

## Common workflows
- Python deps: `pip install -r requirements.txt` (FastAPI/Uvicorn are present in the devcontainer environment).
- Run the web server (serves the UI + API):
  - `uvicorn src.server.app:app --reload --host 0.0.0.0 --port 8000`
  - Open `http://localhost:8000`
- Azure auth prereq (for anything that calls Azure):
  - `az login --use-device-code`
- Docs site (VitePress):
  - `npm install`
  - `npm run docs:dev`

## Project-specific conventions
- Prefer raising `ApiError` from `src/server/errors.py` inside server code; the exception handler returns `{ "error": {"message", "hint" } }`.
- Message size is capped at 5000 chars on both client and server (`src/client/app.js`, `src/server/agent_session.py`).
- Keep client calls aligned with existing endpoints in `src/client/app.js` (it only uses `POST` JSON).
- Keep UI strictly static (no framework): edit `src/client/index.html`, `src/client/styles.css`, `src/client/app.js`.

## Debugging (common failures)
- If `/api/session/start` fails with “Missing required configuration”, set `PROJECT_CONNECTION_STRING` (use `.env.example` as a template) and restart the server (`python-dotenv` loads `.env` at startup in `src/server/app.py`).
- If auth fails, run `az login --use-device-code` (the server uses `DefaultAzureCredential` in `src/server/agent_session.py`).
- When the UI shows an error panel, it’s rendering the server’s `{ error: { message, hint } }` payload; update hints by changing `src/server/errors.py`.

## Where to look first
- Web UI: `src/server/app.py`, `src/server/routes/session_routes.py`, `src/client/app.js`.
- Agent behavior/tools: `src/server/agent_session.py`, `workshop/instructions.txt`, `workshop/tools.py`.
