from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    FileSearchTool,
    FunctionTool,
    McpTool,
    MessageRole,
    RequiredMcpToolCall,
    RunHandler,
    ThreadRun,
    ToolApproval,
    ToolSet,
)
from azure.identity import DefaultAzureCredential

from src.server.errors import agent_unavailable_error, auth_error, missing_prereq_error


try:
    from workshop.tools import calculate_pizza_for_people
except Exception:
    # Namespace-package import should work when repo root is on sys.path.
    # If it fails, we'll surface a runtime error during session start.
    calculate_pizza_for_people = None  # type: ignore


DEFAULT_MAX_MESSAGE_CHARS = 5000
DEFAULT_VECTOR_STORE_ID = "vs_bXJCOxUtuWX8vlv7bsr5GqWd"


@dataclass(frozen=True)
class StartedSession:
    agent_id: str
    thread_id: str


class _McpApprovalRunHandler(RunHandler):
    def __init__(self, *, mcp_tool: McpTool) -> None:
        self._mcp_tool = mcp_tool

    def submit_mcp_tool_approval(
        self, *, run: ThreadRun, tool_call: RequiredMcpToolCall, **kwargs: Any
    ) -> ToolApproval:
        return ToolApproval(
            tool_call_id=tool_call.id,
            approve=True,
            headers=self._mcp_tool.headers,
        )


class AgentSessionService:
    def __init__(self) -> None:
        self._project_client: Optional[AIProjectClient] = None

    def _get_project_client(self) -> AIProjectClient:
        if self._project_client is not None:
            return self._project_client

        endpoint = os.environ.get("PROJECT_CONNECTION_STRING")
        if not endpoint:
            raise missing_prereq_error(missing="PROJECT_CONNECTION_STRING")

        try:
            self._project_client = AIProjectClient(
                endpoint=endpoint, credential=DefaultAzureCredential()
            )
            return self._project_client
        except Exception as exc:
            message = str(exc).lower()
            if "credential" in message or "authentication" in message or "unauthorized" in message:
                raise auth_error() from exc
            raise agent_unavailable_error() from exc

    def _build_toolset(self) -> tuple[ToolSet, _McpApprovalRunHandler]:
        vector_store_id = os.environ.get("VECTOR_STORE_ID") or DEFAULT_VECTOR_STORE_ID
        file_search = FileSearchTool(vector_store_ids=[vector_store_id])

        if calculate_pizza_for_people is None:
            raise agent_unavailable_error()
        function_tool = FunctionTool(functions={calculate_pizza_for_people})

        mcp_tool = McpTool(
            server_label="contoso_pizza",
            server_url=os.environ.get(
                "PIZZA_MCP_SSE_URL",
                "https://ca-pizza-mcp-sc6u2typoxngc.graypond-9d6dd29c.eastus2.azurecontainerapps.io/sse",
            ),
            allowed_tools=[
                "get_pizzas",
                "get_pizza_by_id",
                "get_toppings",
                "get_topping_by_id",
                "get_topping_categories",
                "get_orders",
                "get_order_by_id",
                "place_order",
                "delete_order_by_id",
            ],
        )
        mcp_tool.set_approval_mode("never")

        toolset = ToolSet()
        toolset.add(file_search)
        toolset.add(function_tool)
        toolset.add(mcp_tool)

        handler = _McpApprovalRunHandler(mcp_tool=mcp_tool)
        return toolset, handler

    def start_session(self) -> StartedSession:
        project_client = self._get_project_client()

        toolset, handler = self._build_toolset()
        project_client.agents.enable_auto_function_calls(toolset)

        try:
            with open("workshop/instructions.txt", "r", encoding="utf-8") as f:
                instructions = f.read()
        except Exception as exc:
            raise agent_unavailable_error() from exc

        try:
            agent = project_client.agents.create_agent(
                model=os.environ.get("PIZZA_MODEL", "gpt-4o"),
                name="pizza-bot",
                instructions=instructions,
                top_p=0.7,
                temperature=0.7,
                toolset=toolset,
            )
            thread = project_client.agents.threads.create()
            return StartedSession(agent_id=agent.id, thread_id=thread.id)
        except Exception as exc:
            raise agent_unavailable_error() from exc

    def send_message(self, *, agent_id: str, thread_id: str, message: str) -> str:
        if len(message) > DEFAULT_MAX_MESSAGE_CHARS:
            raise ValueError(f"Message exceeds {DEFAULT_MAX_MESSAGE_CHARS} characters")

        project_client = self._get_project_client()
        toolset, handler = self._build_toolset()
        project_client.agents.enable_auto_function_calls(toolset)

        try:
            project_client.agents.messages.create(
                thread_id=thread_id,
                role=MessageRole.USER,
                content=message,
            )
            project_client.agents.runs.create_and_process(
                thread_id=thread_id,
                agent_id=agent_id,
                run_handler=handler,
            )

            messages = project_client.agents.messages.list(thread_id=thread_id)
            agent_message = next(
                (m for m in messages if getattr(m, "role", None) == MessageRole.AGENT),
                None,
            )
            if not agent_message:
                return ""

            return next(
                (
                    item["text"]["value"]
                    for item in agent_message.content
                    if item.get("type") == "text"
                ),
                "",
            )
        except Exception as exc:
            raise agent_unavailable_error() from exc

    def end_session(self, *, agent_id: str) -> None:
        project_client = self._get_project_client()
        try:
            project_client.agents.delete_agent(agent_id)
        except Exception:
            # Best-effort cleanup.
            pass


agent_session_service = AgentSessionService()
