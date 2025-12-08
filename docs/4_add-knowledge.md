# Adding Knowledge with File Search  

In the previous chapters, you created a basic agent and gave it instructions through a system prompt.  
Now it’s time to **make your agent smarter** by grounding it in **your own data**.  



## Why Add Knowledge?  

By default, the model only knows what it was trained on - it doesn’t have access to your organization’s private or domain-specific information.  
To bridge this gap, we’ll use **Retrieval-Augmented Generation (RAG)**.  

- **RAG** lets the agent fetch relevant information from your own data before generating a response.  
- This ensures your agent’s answers are **accurate, up-to-date, and grounded** in real information.  
- In Microsoft Foundry, we’ll use the **File Search** feature to implement this.  

In this chapter, you’ll use a folder called **`./documents`** that contains information about **Contoso Pizza stores** - such as locations, opening hours, and menus.  

We’ll upload these files to **Microsoft Foundry**, create a **vector store**, and connect that store to the agent using a **File Search tool**.  


## Step 1 - Create a Vector Store Script  

We’ll build this step by step to make sure everything is clear.  
Your goal: create a script that uploads files, creates a vector store, and vectorizes your data for search.  

### Part A - Prepare Your Environment  

**Goal:** Load secrets from `.env` and import the necessary SDKs.  

Create a new file called **`add_data.py`** and add:  

```python
import os
from dotenv import load_dotenv

# Azure SDK imports
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FilePurpose

# Load environment variables (expects PROJECT_CONNECTION_STRING in .env)
load_dotenv(override=True)
```

**Why:**  
- `.env` keeps your credentials separate from code.  
- `AIProjectClient` lets you interact with your Microsoft Foundry project.  
- `FilePurpose.AGENTS` tells the service these files are for agents.  

### Part B - Connect to Your Microsoft Foundry Project  

**Goal:** Create the project client using your connection string.  

Append this to your script:  

```python
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
```

**Why:**  
This connects your script to your Microsoft Foundry project, allowing file uploads and vector store creation to happen in your workspace.  


### Part C - Upload Your Documents  

**Goal:** Upload files from `./documents` and collect their IDs.  

Append this:  

```python
DOCS_DIR = "./documents"

if not os.path.isdir(DOCS_DIR):
    raise FileNotFoundError(
        f"Documents folder not found at {DOCS_DIR}. "
        "Create it and add your Contoso Pizza files (PDF, TXT, MD, etc.)."
    )

print(f"Uploading files from {DOCS_DIR} ...")
file_ids = []
for fname in os.listdir(DOCS_DIR):
    fpath = os.path.join(DOCS_DIR, fname)
    # skip directories and hidden files like .DS_Store
    if not os.path.isfile(fpath) or fname.startswith('.'):
        continue
    uploaded = project_client.agents.files.upload_and_poll(
        file_path=fpath,
        purpose=FilePurpose.AGENTS
    )
    file_ids.append(uploaded.id)

print(f"Uploaded {len(file_ids)} files.")
if not file_ids:
    raise RuntimeError("No files uploaded. Put files in ./documents and re-run.")
```

**Why:**  
Your documents must be uploaded before they can be vectorized and made searchable.  

**Tip:** Keep documents short and relevant (store info, hours, menus). Split very large docs when possible.  


### Part D - Create a Vector Store  

**Goal:** Create an empty vector store that will store and index your document embeddings.  

Append:  

```python
vector_store = project_client.agents.vector_stores.create_and_poll(
    data_sources=[],
    name="contoso-pizza-store-information"
)
print(f"Created vector store, ID: {vector_store.id}")
```

**Why:**  
A vector store is what enables semantic search - it finds text that *means* the same thing as the user’s query, even if the words differ.  


### Part E - Vectorize Files into the Store  

**Goal:** Add your uploaded files to the vector store and process them for search.  

Append:  

```python
batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
print(f"Created vector store file batch, ID: {batch.id}")
```

**Why:**  
This creates vector embeddings for your files so the agent can later retrieve relevant chunks via the File Search tool.  


### Final file
```python
<!--@include: ./codesamples/add_data.py-->
```

### Run the Script  

From your **`workshop/`** directory, run:  

```bash
python add_data.py
```

Example output:  

```
Uploading files from ./documents ...
Uploaded 19 files.
Created vector store, ID: vs_ii6H96sVMeQcXICvj7e3DsrK
Created vector store file batch, ID: vsfb_47c68422adc24e0a915d0d14ca71a3cf
```

✅ **Copy the vector store ID** - you’ll use it in the next section.  



## Step 2 - Add the File Search Tool  

Now that you’ve created your vector store, let’s connect it to your agent.  

In `agent.py`, right after you create your `AIProjectClient`, add:  

```python
# Create the File Search tool
vector_store_id = "<INSERT YOUR VECTOR STORE ID HERE>"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])
```

### Add the Tool to a Toolset  

```python
# Create the toolset
toolset = ToolSet()
toolset.add(file_search)
```



### Create the Agent with Knowledge  

Find the block where you create your agent and modify it to include the toolset:  

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



## Step 3 - Run the Agent  

Try it out:  

```bash
python agent.py
```

Ask questions like:  
> “Which Contoso Pizza stores are open after 8pm?”  
> “Where is the nearest Contoso Pizza store?”  

Type `exit` or `quit` to stop the conversation.  



## Recap  

In this chapter, you:  
- Learned how **RAG** grounds your agent with your own data  
- Uploaded files from the `./documents` directory  
- Created and populated a **vector store**  
- Added a **File Search tool** to your agent  
- Extended your PizzaBot to answer questions about **Contoso Pizza stores**  


## Final code sample

```python 
<!--@include: ./codesamples/agent_4_rag.py-->
```