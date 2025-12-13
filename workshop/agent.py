import os
import time
from typing import Any
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet,
    McpTool, ToolApproval, ThreadRun, RequiredMcpToolCall, RunHandler
)
from tools import calculate_pizza_for_people
from dotenv import load_dotenv

load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

# Create the File Search tool
vector_store_id = "vs_bXJCOxUtuWX8vlv7bsr5GqWd"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Create a FunctionTool for the calculate_pizza_for_people function
function_tool = FunctionTool(functions={calculate_pizza_for_people})

# Add MCP tool so the agent can call Contoso Pizza microservices
mcp_tool = McpTool(
    server_label="contoso_pizza",
    server_url="https://ca-pizza-mcp-sc6u2typoxngc.graypond-9d6dd29c.eastus2.azurecontainerapps.io/sse",
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

# Custom RunHandler to approve MCP tool calls
class MyRunHandler(RunHandler):
    def submit_mcp_tool_approval(
        self, *, run: ThreadRun, tool_call: RequiredMcpToolCall, **kwargs: Any
    ) -> ToolApproval:
        print(f"[RunHandler] Approving MCP tool call: {tool_call.id} for tool: {tool_call.name}")
        return ToolApproval(
            tool_call_id=tool_call.id,
            approve=True,
            headers=mcp_tool.headers,
        )

# Create the toolset
toolset = ToolSet()
toolset.add(file_search)
toolset.add(function_tool)
toolset.add(mcp_tool)

# Enable automatic function calling for this toolset so the agent can call functions directly
project_client.agents.enable_auto_function_calls(toolset)

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="pizza-bot",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset
)
print(f"Created agent with system prompt, ID: {agent.id}")


thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")


try:
    while True:

        # Get the user input
        user_input = input("You: ")

        # Break out of the loop
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add a message to the thread
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER, 
            content=user_input
       )
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=agent.id,
            run_handler=MyRunHandler()  # Enables controlled MCP approvals
        )

        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None) 
        if first_message: 
            print(next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), ""))
finally:
    # Clean up the agent when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")