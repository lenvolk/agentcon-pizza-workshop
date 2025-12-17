# Speckit Constitution (agentcon-pizza-workshop)

## Mission
Ship small, correct changes quickly while preserving the workshop’s learning flow and the VOLK web UI’s simplicity.

## Source of truth
- Repo facts + workflows: `.github/copilot-instructions.md`
- Product intent: `docs/prd.md`
- Web UI code: `src/server/` and `src/client/`
- Workshop scripts/data: `workshop/`

## Delegation (roles)
- Orchestrator (main agent): coordinates work, chooses the right subagent, and owns final integration.
- Subagents (preferred ownership boundaries):
  - Frontend UI: `src/client/` (HTML/CSS/JS, fetch calls, localStorage state)
  - Backend API: `src/server/` (FastAPI routes, errors, session store)
  - Agent/RAG/Knowledge: `workshop/`, `workshop/documents/`, knowledge/rag docs
  - MCP/Tools: MCP/tool wiring + `workshop/tools.py`
  - Docs: `docs/` and root `readme.md`

## Guardrails (project-specific)
- Do not add new endpoints or pages unless explicitly requested.
- Preserve existing API contracts:
  - `POST /api/session/start|message|end` with JSON bodies
  - Error shape is `{ "error": { "message": string, "hint"?: string } }`
- Keep UI strictly static (no framework). Touch only `src/client/index.html`, `src/client/styles.css`, `src/client/app.js`.
- Session store is in-memory only (`src/server/session_store.py`); assume server restarts reset sessions.
- Message length cap is 5000 chars on both client and server.

## Quality bar (what “done” means)
- Changes are minimal and localized to the correct area.
- Commands and configuration referenced are real for this repo.
- If behavior changes, ensure both sides remain aligned:
  - UI fetch paths and payloads match server routes and Pydantic models.
- Prefer raising `ApiError` helpers from `src/server/errors.py` instead of ad-hoc exceptions.

## Validation expectations
- For server changes: run or at least sanity-check `uvicorn src.server.app:app --reload --host 0.0.0.0 --port 8000`.
- For client changes: open `/` and exercise the flow (Welcome → send message → End chat).
- For Azure integration: mention required env vars and `az login --use-device-code` when relevant.
