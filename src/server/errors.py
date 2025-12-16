from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ErrorPayload:
    message: str
    hint: Optional[str] = None

    def to_dict(self) -> dict:
        error: dict = {"message": self.message}
        if self.hint:
            error["hint"] = self.hint
        return {"error": error}


class ApiError(Exception):
    def __init__(self, status_code: int, *, message: str, hint: Optional[str] = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = ErrorPayload(message, hint)


def missing_prereq_error(*, missing: str) -> ApiError:
    return ApiError(
        400,
        message=f"Missing required configuration: {missing}",
        hint=(
            "Set it in your environment or .env, then restart the server. "
            "For Codespaces, ensure you've run `az login --use-device-code`."
        ),
    )


def auth_error() -> ApiError:
    return ApiError(
        400,
        message="Azure authentication failed.",
        hint="Run `az login --use-device-code` and retry.",
    )


def agent_unavailable_error() -> ApiError:
    return ApiError(
        500,
        message="The agent service is unavailable right now.",
        hint=(
            "Verify PROJECT_CONNECTION_STRING is valid and that Azure access is working, "
            "then retry."
        ),
    )


def session_not_found_error() -> ApiError:
    return ApiError(
        404,
        message="Session not found.",
        hint="Return to the Welcome screen and start a new session.",
    )


def invalid_message_error(*, message: str) -> ApiError:
    return ApiError(
        400,
        message=message,
    )
