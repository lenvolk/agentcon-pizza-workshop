# Tool Calling – Making Your Agent Act

In the previous chapters you gave your agent instructions and grounded it in your own data with File Search (RAG).  

Now, let’s enable your agent to **take actions** by calling **tools** — small, well-defined functions your agent can invoke to perform tasks (e.g., calculations, lookups, API calls).

## What Are Tools (Function Calling)?

**Tools** let your agent call *your code* with structured inputs.  
When a user asks for something that matches a tool’s purpose, the agent will select that tool, pass validated arguments, and use the tool’s result to craft a final answer.

### Why this matters
- **Deterministic actions:** offload precise work (math, lookup, API calls) to your code.  
- **Safety & control:** you define what the agent is allowed to do.  
- **Better UX:** the agent can provide concrete, actionable answers.



## Adding the Pizza Size Calculator tool

We’ll add a tool that, given a **group size** and an **appetite level**, recommends how many and what size pizzas to order.

### 1) Create `tools.py` (new file)

```python
<!--@include: ./codesamples/tools.py-->
```

::: info
This function needs no imports; it uses only Python built-ins.
:::


### 2) Import the function in `agent.py`

Add the import alongside your other imports:

```python
from tools import calculate_pizza_for_people
```

Your imports should look like this:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```



### 3) Expose the function as a tool

Create a `FunctionTool` seeded with the Python function(s) the agent may call:

```python
# Create a FunctionTool for the calculate_pizza_for_people function
function_tool = FunctionTool(functions={calculate_pizza_for_people})
```

Insert this block **immediately after** your File Search setup and toolset creation, like so:

**Existing**
```python
# Create the file_search tool
vector_store_id = "<INSERT COPIED VECTOR STORE ID>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Creating the toolset
toolset = ToolSet()
toolset.add(file_search)
```

**New**
```python
# Create the file_search tool
vector_store_id = "<INSERT COPIED VECTOR STORE ID>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Create the function tool
function_tool = FunctionTool(functions={calculate_pizza_for_people})

# Creating the toolset
toolset = ToolSet()
toolset.add(file_search)
toolset.add(function_tool)
```


### 4) Enable automatic function calling (optional, if supported)

Right after you create your toolset, enable auto function calling so the agent can invoke tools without you routing calls manually:

```python
toolset.add(function_tool)

# Enable automatic function calling for this toolset so the agent can call functions directly
project_client.agents.enable_auto_function_calls(toolset)
```

## Trying It Out

Run your agent and ask a question that should trigger the tool:

```
We are 7 people with heavy appetite. What pizzas should we order?
```

The agent should call `calculate_pizza_for_people` and reply with the recommendation it returns.



## Tips & Best Practices

- **Schema first:** if your SDK supports argument schemas, define clear types/enums/required fields.  
- **Validate inputs:** the tool should handle bad or missing data gracefully.  
- **Single-purpose tools:** small, focused tools are easier for the agent to choose and combine.  
- **Explainability:** name/describe tools so the agent knows when to use them.



## Recap

In this chapter you:
- Created a **pizza calculator** in a separate `tools.py`.  
- Exposed it as a **function tool** the agent can call.  
- Added it to your existing **ToolSet** (alongside File Search).  
- (Optionally) enabled **automatic function calling**.  
- Verified tool calling by prompting your agent.



## Final code sample

```python 
<!--@include: ./codesamples/agent_5_tools.py-->
```