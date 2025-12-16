from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from src.server.agent_session import agent_session_service
from src.server.errors import invalid_message_error, session_not_found_error
from src.server.session_store import SessionRecord, session_store


router = APIRouter(prefix="/api/session")


class StartSessionRequest(BaseModel):
    sessionId: str


class StartSessionResponse(BaseModel):
    sessionId: str
    status: str


class SendMessageRequest(BaseModel):
    sessionId: str
    message: str


class SendMessageResponse(BaseModel):
    sessionId: str
    reply: str


class EndSessionRequest(BaseModel):
    sessionId: str


class EndSessionResponse(BaseModel):
    sessionId: str
    status: str


@router.post("/start", response_model=StartSessionResponse)
def start_session(payload: StartSessionRequest) -> StartSessionResponse:
    existing = session_store.get(payload.sessionId)
    if existing is not None:
        return StartSessionResponse(sessionId=payload.sessionId, status="ready")

    started = agent_session_service.start_session()
    session_store.set(
        SessionRecord(
            session_id=payload.sessionId,
            agent_id=started.agent_id,
            thread_id=started.thread_id,
        )
    )
    return StartSessionResponse(sessionId=payload.sessionId, status="ready")


@router.post("/message", response_model=SendMessageResponse)
def send_message(payload: SendMessageRequest) -> SendMessageResponse:
    record = session_store.get(payload.sessionId)
    if record is None:
        raise session_not_found_error()

    try:
        reply = agent_session_service.send_message(
            agent_id=record.agent_id,
            thread_id=record.thread_id,
            message=payload.message,
        )
    except ValueError as exc:
        raise invalid_message_error(message=str(exc)) from exc

    return SendMessageResponse(sessionId=payload.sessionId, reply=reply)


@router.post("/end", response_model=EndSessionResponse)
def end_session(payload: EndSessionRequest) -> EndSessionResponse:
    record = session_store.delete(payload.sessionId)
    if record is None:
        raise session_not_found_error()

    agent_session_service.end_session(agent_id=record.agent_id)
    return EndSessionResponse(sessionId=payload.sessionId, status="ended")
