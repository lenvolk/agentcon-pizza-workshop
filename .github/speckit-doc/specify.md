# Speckit Specify (inputs + scope)

## Primary inputs (always include)
- Repo operating guide: `.github/copilot-instructions.md`
- Product requirements: `docs/prd.md`

## Web UI scope
- Server entrypoint: `src/server/app.py`
- Routes: `src/server/routes/session_routes.py`
- Error contract: `src/server/errors.py`
- Session persistence: `src/server/session_store.py`
- Azure agent wiring: `src/server/agent_session.py`
- Client app: `src/client/index.html`, `src/client/styles.css`, `src/client/app.js`

## Workshop scope
- Workshop scripts: `workshop/agent.py`, `workshop/add_data.py`, `workshop/tools.py`
- Agent instructions: `workshop/instructions.txt`
- Knowledge docs: `workshop/documents/`

## Environment/config files
- Python deps: `requirements.txt`
- Docs site tooling: `package.json`
- Local env template: `.env.example` (note: `.env` is gitignored)

## Agent map (optional, if using subagents)
- Main agent/orchestrator: selects the right subagent, enforces guardrails, integrates final output.
- Subagents live under `.github/agents/subagents/`:
  - `frontend-ui.agent.md`
  - `backend-api.agent.md`
  - `agent-rag-knowledge.agent.md`
  - `mcp-tools-integration.agent.md`
  - `docs-and-speckit.agent.md`

## Out of scope by default
- New product features not described by the user/PRD
- Large refactors or renames
- Adding new external dependencies without an explicit request
