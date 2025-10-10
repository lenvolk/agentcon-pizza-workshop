# Integrating MCP (Model Context Protocol)

In earlier chapters, your agent learned to follow instructions, ground itself in your data (RAG/File Search), and call custom tools.  
In this final chapter, you’ll connect your agent to an **MCP server** so it can use **external capabilities** (like live menus, toppings, and order management) over a standard protocol.


## What is MCP and why use it?

**MCP (Model Context Protocol)** is an open protocol for connecting AI models to tools, data sources, and services through interoperable **MCP servers**.  
Instead of tightly coupling your agent to each API, you connect **once** to an MCP server and gain access to all tools it exposes.

**Benefits:**
- **Interoperability:** a consistent way to expose tools from any service to any MCP‑aware agent.
- **Separation of concerns:** keep business logic and integrations in the server; keep the agent simple.
- **Security & governance:** centrally manage what tools are available and how they’re approved.
- **Scalability:** add or update tools on the server without redeploying your agent code.


## Install the MCP Package

Before using MCP, install the latest Azure AI Agents SDK that includes MCP support:

In the terminal install the required library

```shell
pip install "azure-ai-agents>=1.2.0b3"
```

Add the MCP Tool and time to the packages in the import section of `agents.py`

```python
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet, McpTool
```
```python
import time
```

This should now look like 

```
import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet, McpTool
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```

## The Contoso Pizza MCP Server

For Contoso Pizza, the MCP server exposes APIs for pizzas, toppings, and order management.  
We’ll connect your agent to this server and **allow** a curated set of tools so the agent can fetch live information and place orders.

## Create the MCP Tool

The MCP tool support need to be intersted between the following block in 'agents.py'

```
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

```
And before 
```
try:
    while True:
        # Get the user input
        user_input = input("You: ")
```

## Add the MCP Tool to the Toolset

Add the tool to your existing `toolset` the next block should be added after 

```
# Add MCP tool so the agent can call Contoso Pizza microservices
mcp_tool = McpTool(
    server_label="contoso_pizza",
    server_url="<!--@include: ./variables/mcp-url.md-->",
    allowed_tools=[
        "get_pizzas",
        "get_pizza_by_id",
        "get_toppings",
        "get_topping_by_id",
        "get_topping_categories",
        "get_orders",
        "get_order_by_id",
        "place_order",
        "delete_order_by_id"
    ],
)
mcp_tool.set_approval_mode("never")
```

Add the following after the above to 'agents.py'

```python
toolset.add(mcp_tool)
```
### Notes
- **server_label**: a friendly name used in logs/telemetry.
- **server_url**: the [MCP server endpoint](./pizza-mcp.md)
- **allowed_tools**: a safety allowlist - only these tools are callable by the agent.
- **approval mode**: set to `"never"` here (no human approval prompts). Consider stricter modes for production.

:::warning
⚠️ Make sure you’ve imported the MCP tool class in your file (e.g., `from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet, McpTool`).
:::
## NOTE
When you create the agent, the agent keep passing the `toolset` using the toolset=toolset:

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions=open("instructions.txt").read(),
    toolset=toolset
)
```
### Change how we fetch All Messages from the Thread  

**Replace this code:**

```python
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent.id
    )  
```

**With this code:**

```python
    # Process the agent run
        run = project_client.agents.runs.create(
            thread_id=thread.id,
            agent_id=agent.id,
            tool_resources=mcp_tool.resources,
        )
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(0.1)
            run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
```

## Get a User ID

To order pizza you need a **User ID**. You can get one by navigating to this URL:  
[<!--@include: ./variables/customer-registration.md-->](<!--@include: ./variables/customer-registration.md-->).

Next, add the following section to your `instructions.txt` file:

```txt
## User details:
Name: <YOUR NAME>
UserId: <USER GUID>
```

This should now look like 

```
## Tools & Data Access
- Use the **Contoso Pizza Store Information Vector Store** to search get information about stores, like address and opening times.
    - **Tool:** `file_search`
    - Only return information found in the vector store or uploaded files.
    - If the information is ambiguous or not found, ask the user for clarification.

## User details:
Name: <YOUR NAME>
UserId: <USER GUID>

## Response
You will interact with users primarily through voice, so your responses should be natural, short and conversational. 
1. **Only use plain text**
2. No emoticons, No markup, No markdown, No html, only plain text.
3. Use short and conversational language.
```
By adding this the agent will make orders using your userid. 

::: tip
You can see your orders: 
[<!--@include: ./variables/pizza-dashboard.md-->](<!--@include: ./variables/pizza-dashboard.md-->).
:::

## Final Code 
```
import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet, McpTool
from tools import calculate_pizza_for_people
from dotenv import load_dotenv

load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

# Upload all files in the documents directory
print(f"Uploading files from ./documents ...")
file_ids = [
    project_client.agents.files.upload_and_poll(file_path=os.path.join("./documents", f), purpose=FilePurpose.AGENTS).id
    for f in os.listdir("./documents")
    if os.path.isfile(os.path.join("./documents", f))
]
print(f"Uploaded {len(file_ids)} files.")
# Create a vector store with the uploaded files
vector_store = project_client.agents.vector_stores.create_and_poll(
    data_sources=[],
    name="contoso-pizza-store-information"
)
print(f"Created vector store, vector store ID: {vector_store.id}")
# Create a vector store file batch to process the uploaded files
batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
file_search = FileSearchTool(vector_store_ids=[vector_store.id])
toolset = ToolSet()
toolset.add(file_search)

# Create a FunctionTool for the calculate_pizza_for_people function and add it to the toolset
# Pass the actual Python function(s) the agent should be able to call. Using a set is fine here.
function_tool = FunctionTool(functions={calculate_pizza_for_people})
toolset.add(function_tool)

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset  # Add the toolset to the agent
)
print(f"Created agent, ID: {agent.id}")

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="pizza-bot",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
)
print(f"Created agent with system prompt, ID: {agent.id}")

thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Define the MCP tool
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

# Set approval mode (valid options depend on SDK: 'never', 'always', 'manual', etc.)
mcp_tool.set_approval_mode("never")

# Add the MCP tool to the toolset so the agent can use it
toolset.add(mcp_tool)

# Enable automatic function calling for this toolset so the agent can call functions directly
project_client.agents.enable_auto_function_calls(toolset)

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

        # Process the agent run
        run = project_client.agents.runs.create(
            thread_id=thread.id,
            agent_id=agent.id,
            tool_resources=mcp_tool.resources,
        )
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(0.1)
            run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

        # List messages and print the first text response from the agent
        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None)
        if first_message:
            print(
                next(
                    (item["text"]["value"] for item in first_message.content if item.get("type") == "text"),
                    ""
                )
            )
           
finally:
    # Clean up the agent when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## Trying It Out

Ask your agent questions that should hit the MCP server tools, for example:

```
Show me the available pizzas.
```

```
What is the price for a pizza hawai.
```

```
Place an order for 2 large pepperoni pizzas.
```

The agent will call the allowed MCP tools, then summarize their responses in natural language—while still following your **instructions.txt** rules (tone, currency/time conversions, etc.).



## Best Practices

- **Principle of least privilege:** only allow tools your agent truly needs.
- **Observability:** log tool calls and handle failures gracefully.
- **Versioning:** pin server URLs or versions where possible to avoid breaking changes.
- **Human‑in‑the‑loop:** consider approval modes other than `"never"` for sensitive actions.
- **Resilience:** the agent should explain transient errors and suggest retries when remote tools fail.



## Recap

In this chapter, you:
- Learned what **MCP** is and why it’s useful.
- Installed the updated **Azure AI Agents SDK** with MCP support.
- Configured an **MCP tool** to connect to the Contoso Pizza server.
- Added it to your **ToolSet** so your agent can fetch menu data and manage orders.
- Tested the setup with example prompts.

---


🎉 **You’ve completed the workshop!** Your agent now has instructions, knowledge (RAG), custom tools, and MCP‑powered capabilities.
