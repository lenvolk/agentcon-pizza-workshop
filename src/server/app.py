from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from src.server.routes.session_routes import router as session_router
from src.server.errors import ApiError


ROOT = Path(__file__).resolve().parents[2]
CLIENT_DIR = ROOT / "src" / "client"

# Allow local workshop configuration via a `.env` file.
# NOTE: This does not override existing environment variables.
load_dotenv(override=False)

app = FastAPI(title="VOLK Pizza Web UI")
app.include_router(session_router)


@app.exception_handler(ApiError)
def handle_api_error(request: object, exc: ApiError) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(status_code=exc.status_code, content=exc.payload.to_dict())


app.mount("/", StaticFiles(directory=CLIENT_DIR, html=True), name="client")
