# Adding Knowledge with File Search  

In the previous chapters, you created a basic agent and gave it instructions through a system prompt.  
Now it’s time to **make your agent smarter** by grounding it in **your own data**.  

## Why Add Knowledge?  

By default, the model only has its built-in training knowledge, which might not include your specific business information.  
To bridge this gap, we use **Retrieval-Augmented Generation (RAG)** technology.  

- **RAG** allows the model to fetch relevant information from your own data before generating a response.  
- This ensures the agent’s answers are always **accurate, up to date, and grounded** in real data.  
- The mechanism we’ll use here is called **File Search**.  


## File Search and the Documents Directory  

In this example, we’ll use a directory called **`./documents`** that contains information about **Contoso Pizza stores** (e.g., addresses, opening hours, menus).  

We’ll upload these documents to Azure AI Foundry, process them into a **vector store**, and then connect that store to the agent using a **File Search tool**.  

## Adding File Search to the Agent  

We’ll extend our `agent.py` to include the **File Search tool**.  

:::info
Put this code after the creation of the `AIProjectClient` object. 
:::

You should insert the document upload code **immediately after the creation of the `AIProjectClient` object**, this means placing it **right after this block**:

```python
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
```
### Upload Documents  

The first step is to upload all the files in the `./documents` directory.

```python
# Upload all files in the documents directory
print(f"Uploading files from ./documents ...")
file_ids = [
    project_client.agents.files.upload_and_poll(file_path=os.path.join("./documents", f), purpose=FilePurpose.AGENTS).id
    for f in os.listdir("./documents")
    if os.path.isfile(os.path.join("./documents", f))
]
print(f"Uploaded {len(file_ids)} files.")
```

---

### Create a Vector Store  

A **vector store** is where the documents are indexed and stored for semantic search.  

```python
# Create a vector store with the uploaded files
vector_store = project_client.agents.vector_stores.create_and_poll(
    data_sources=[],
    name="contoso-pizza-store-information"
)
print(f"Created vector store, vector store ID: {vector_store.id}")
```

---

### Process the Files  

We then create a **file batch** to process the uploaded files and add them to the vector store.  

```python
# Create a vector store file batch to process the uploaded files
batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
```

---

### Create the File Search Tool  

Next, we create a **File Search tool** that can query the vector store.  

```python
file_search = FileSearchTool(vector_store_ids=[vector_store.id])
```

---

### Add the Tool to a Toolset  

Tools are grouped into a **ToolSet**, which is then passed into the agent.  

```python
toolset = ToolSet()
toolset.add(file_search)
```

---

### Create the Agent with Knowledge  

Finally, we create the agent again, this time adding the toolset.  

```python
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions=open("instructions.txt").read(),
    top_p=0.7,
    temperature=0.7,
    toolset=toolset  # Add the toolset to the agent
)
print(f"Created agent, ID: {agent.id}")
```

## Run the Agent  

Try out the Agent:  

```shell
python agent.py
```

Try and ask questions about the contoso pizza stores.

You can now chat with your agent directly in the terminal. Type `exit` or `quit` to stop the conversation.  


## Final Code 

```
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
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
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )

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

## Recap  

In this chapter, you have:  

- Learned how **RAG** grounds your agent with real data  
- Uploaded files from the `./documents` directory  
- Created a **vector store** to store and index your files  
- Built a **File Search tool**  
- Connected the toolset to your agent so it can answer questions about **Contoso Pizza stores**  

