<!--
Sync Impact Report

- Version change: N/A (template placeholders) → 1.0.0
- Modified principles: N/A (newly instantiated from template)
- Added sections: Project Guardrails; Workflow & Validation
- Removed sections: None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md (no change)
	- ✅ .specify/templates/tasks-template.md (no change)
	- ⚠️ .specify/templates/commands/*.md (folder not present in this repo)
- Follow-up TODOs: None
-->

# Speckit Constitution (agentcon-pizza-workshop)

## Core Principles

### Ship Small, Correct Changes
Ship small, correct changes quickly while preserving the workshop’s learning flow and the VOLK web UI’s simplicity. Changes MUST be minimal and localized to the correct area.

### Use the Repo as Source of Truth
When in doubt, prefer repository facts over assumptions:

- Repo facts + workflows: `.github/copilot-instructions.md`
- Product intent: `docs/prd.md`
- Web UI code: `src/server/` and `src/client/`
- Workshop scripts/data: `workshop/`

### Preserve Contracts and Keep the UI Static
Do not add new endpoints or pages unless explicitly requested. Preserve existing API contracts and error shape:

- `POST /api/session/start|message|end` with JSON bodies
- Error shape is `{ "error": { "message": string, "hint"?: string } }`

Keep UI strictly static (no framework). Touch only `src/client/index.html`, `src/client/styles.css`, and `src/client/app.js`.

Session persistence is in-memory only (`src/server/session_store.py`); assume server restarts reset sessions. Message length cap is 5000 chars on both client and server.

### Work Within Ownership Boundaries
Prefer the smallest-possible change and keep work in the appropriate area:

- Frontend UI: `src/client/` (HTML/CSS/JS, fetch calls, localStorage state)
- Backend API: `src/server/` (FastAPI routes, errors, session store)
- Agent/RAG/Knowledge: `workshop/`, `workshop/documents/`
- MCP/Tools: MCP/tool wiring + `workshop/tools.py`
- Docs: `docs/` and root `readme.md`

### Validate and Standardize Errors
If behavior changes, ensure both sides remain aligned (client fetch paths/payloads match server routes and Pydantic models). Prefer raising `ApiError` helpers from `src/server/errors.py` instead of ad-hoc exceptions.

Validation expectations:

- For server changes: run or at least sanity-check `uvicorn src.server.app:app --reload --host 0.0.0.0 --port 8000`.
- For client changes: open `/` and exercise the flow (Welcome → send message → End chat).
- For Azure integration: mention required env vars and `az login --use-device-code` when relevant.

## Project Guardrails

- Do not add new endpoints or pages unless explicitly requested.
- Preserve existing API contracts and error shape.
- Keep UI strictly static (no framework).
- Assume server restarts reset sessions (in-memory store).
- Keep the 5000 character message cap aligned on both client and server.

## Workflow & Validation

- Changes MUST be minimal and localized to the correct area.
- Commands and configuration referenced MUST be real for this repo.
- If behavior changes, verify the UI and server remain aligned end-to-end.

## Governance
This constitution supersedes other guidance for Speckit-driven work.

Amendments MUST:

- Update this file (`.specify/memory/constitution.md`).
- Update the Sync Impact Report at the top of this file.
- Bump the version using semantic versioning:
	- MAJOR: backward-incompatible governance changes or principle removals/redefinitions
	- MINOR: a new principle/section added or materially expanded guidance
	- PATCH: clarifications, wording, typo fixes, non-semantic refinements
- Propagate any changes into dependent templates under `.specify/templates/`.

Reviews MUST treat constitution conflicts as CRITICAL: adjust spec/plan/tasks to comply rather than weakening principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-17 | **Last Amended**: 2025-12-17
