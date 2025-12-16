from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Dict, Optional


@dataclass(frozen=True)
class SessionRecord:
    session_id: str
    agent_id: str
    thread_id: str


class SessionStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._sessions: Dict[str, SessionRecord] = {}

    def get(self, session_id: str) -> Optional[SessionRecord]:
        with self._lock:
            return self._sessions.get(session_id)

    def set(self, record: SessionRecord) -> None:
        with self._lock:
            self._sessions[record.session_id] = record

    def delete(self, session_id: str) -> Optional[SessionRecord]:
        with self._lock:
            return self._sessions.pop(session_id, None)


session_store = SessionStore()
