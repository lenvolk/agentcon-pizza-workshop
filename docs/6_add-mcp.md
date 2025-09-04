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

```shell
pip install "azure-ai-agents>=1.2.0b3"
```

Add the MCP Tool to the packages

```python
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet, McpTool
```

## The Contoso Pizza MCP Server

For Contoso Pizza, the MCP server exposes APIs for pizzas, toppings, and order management.  
We’ll connect your agent to this server and **allow** a curated set of tools so the agent can fetch live information and place orders.



## Create the MCP Tool

Add the following block to your `agent.py` (after you’ve initialized the `project_client` and before creating the agent).

```python
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

### Notes
- **server_label**: a friendly name used in logs/telemetry.
- **server_url**: the MCP server endpoint (replace <!--@include: ./variables/mcp-url.md-->` with the actual URL).
- **allowed_tools**: a safety allowlist—only these tools are callable by the agent.
- **approval mode**: set to `"never"` here (no human approval prompts). Consider stricter modes for production.

:::warning
⚠️ Make sure you’ve imported the MCP tool class in your file (e.g., `from azure.ai.agents.models import MessageRole, ToolSet, McpTool`).
:::


## Add the MCP Tool to the Toolset

Add the tool to your existing `toolset` (where you also added File Search and the pizza calculator):

```python
toolset.add(mcp_tool)
```

When you create the agent, keep passing the `toolset`:

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
    # Create and process an agent run
    run = project_client.agents.runs.create(
        thread_id=thread.id, 
        agent_id=agent.id, 
        tool_resources=mcp_tool.resources
    )

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(0.1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
```


## Trying It Out

Ask your agent questions that should hit the MCP server tools, for example:

```
Show me the available pizzas.
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
