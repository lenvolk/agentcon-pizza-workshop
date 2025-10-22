# Tool Calling - Making Your Agent Act

In the previous chapters you gave your agent instructions and grounded it in your own data with File Search (RAG).  
Now, let’s enable your agent to **take actions** by calling **tools** — small, well-defined functions your agent can invoke to perform tasks (e.g., calculations, lookups, API calls).

## What Are Tools (Function Calling)?

**Tools** let your agent call *your code* with structured inputs.  
When a user asks for something that matches a tool’s purpose, the agent will select that tool, pass validated arguments, and use the tool’s result to craft a final answer.

#### Why this matters:
- **Deterministic actions:** offload precise work (math, lookup, API call) to your code.
- **Safety & control:** you define what the agent is allowed to do.
- **Better UX:** the agent can provide concrete, actionable answers.


## Adding the Pizza Size Calculator

We’ll add a tool that, given a **group size** and an **appetite level**, recommends how many and what size pizzas to order.

## Import the function 

`import` the function from `tools.py` in the imports 


```python
from tools import calculate_pizza_for_people
```
This should now look like
```
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from tools import calculate_pizza_for_people
from dotenv import load_dotenv
```

## Function Calling

Create a new file called **`tools.py`** and add the function below:

```python
def calculate_pizza_for_people(people_count: int, appetite_level: str = "normal") -> str:
    """
    Calculate the number and size of pizzas needed for a group of people.
    
    Args:
        people_count (int): Number of people who will be eating
        appetite_level (str): Appetite level - "light", "normal", or "heavy" (default: "normal")
    
    Returns:
        str: Recommendation for pizza size and quantity
    """
    if people_count <= 0:
        return "Please provide a valid number of people (greater than 0)."
    
    # Base calculations assuming normal appetite
    # Small pizza: 1-2 people
    # Medium pizza: 2-3 people  
    # Large pizza: 3-4 people
    # Extra Large pizza: 4-6 people
    
    appetite_multipliers = {
        "light": 0.7,
        "normal": 1.0,
        "heavy": 1.3
    }
    
    multiplier = appetite_multipliers.get(appetite_level.lower(), 1.0)
    adjusted_people = people_count * multiplier
    
    recommendations = []
    
    if adjusted_people <= 2:
        if adjusted_people <= 1:
            recommendations.append("1 Small pizza (perfect for 1-2 people)")
        else:
            recommendations.append("1 Medium pizza (great for 2-3 people)")
    elif adjusted_people <= 4:
        recommendations.append("1 Large pizza (serves 3-4 people)")
    elif adjusted_people <= 6:
        recommendations.append("1 Extra Large pizza (feeds 4-6 people)")
    elif adjusted_people <= 8:
        recommendations.append("2 Large pizzas (perfect for sharing)")
    elif adjusted_people <= 12:
        recommendations.append("2 Extra Large pizzas (great for groups)")
    else:
        # For larger groups, calculate multiple pizzas
        extra_large_count = int(adjusted_people // 5)
        remainder = adjusted_people % 5
        
        pizza_list = []
        if extra_large_count > 0:
            pizza_list.append(f"{extra_large_count} Extra Large pizza{'s' if extra_large_count > 1 else ''}")
        
        if remainder > 2:
            pizza_list.append("1 Large pizza")
        elif remainder > 0:
            pizza_list.append("1 Medium pizza")
        
        recommendations.append(" + ".join(pizza_list))
    
    result = f"For {people_count} people with {appetite_level} appetite:\n"
    result += f"🍕 Recommendation: {recommendations[0]}\n"
    
    if appetite_level != "normal":
        result += f"(Adjusted for {appetite_level} appetite level)"
    
    return result
```

## Exposing the Function as a Tool

To let the agent call this function, we define a **function tool** and add it to the existing `ToolSet` (the same way we added File Search).  
Add the following to your `agent.py`

Create the FunctionTool and seed it with a list of functions. In our example this is just the calculate_pizza_for_people function.

```Python
# Create a FunctionTool for the calculate_pizza_for_people function and add it to the toolset
# Pass the actual Python function(s) the agent should be able to call. Using a set is fine here.
function_tool = FunctionTool(functions={calculate_pizza_for_people})
```
Insert this block immediately after:

```
file_search = FileSearchTool(vector_store_ids=[vector_store.id])
toolset = ToolSet()
toolset.add(file_search)

```
and before 
```
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset  # Add the toolset to the agent
)
```

Now **add it to your toolset** (together with File Search if you added that in Chapter 3):

```python
toolset.add(functions)

```

Now **add Enable Automatic function calling**

Insert this block immediately after:

```
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

```
and before 
```
try:
    while True:
        # Get the user input
        user_input = input("You: ")
```
Add this code

```python
# Enable automatic function calling for this toolset so the agent can call functions directly
project_client.agents.enable_auto_function_calls(toolset)
```
Do not forget to add the extra import lines for enabling the function calling.

## Trying It Out

Run your agent and ask a question that should trigger the tool:


```
We are 7 people with heavy appetite. What pizzas should we order?
```

The agent should call the `calculate_pizza_for_people` tool, then reply with the recommendation it returns.


## Tips & Best Practices

- **Schema first:** provide a clear schema (types, enums, required fields).  
- **Validate inputs:** your tool should handle bad or missing data gracefully.  
- **Keep tools single-purpose:** small functions are easier for the agent to select and compose.  
- **Explainability:** include a brief description so the agent knows when to use the tool.

## Recap

In this chapter you:
- Created a **pizza calculator** function.
- Exposed it as a **function tool** the agent can call.
- Added it to your existing **ToolSet**.
- Verified tool calling by prompting your agent.
