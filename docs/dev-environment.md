# Developer Environment Setup  

To build and run the PizzaBot agent during this workshop, you’ll use a pre-configured **GitHub Codespaces** development environment.  

This setup ensures:  
- Python **3.10** is ready to go  
- All required dependencies are pre-installed  
- GitHub Copilot is enabled  
- You can start coding right away in a consistent environment  

## Steps  

### 1. Fork the Repository  
1. Go to the official workshop repo:  
   👉 [https://github.com/GlobalAICommunity/agentcon-pizza-workshop](https://github.com/GlobalAICommunity/agentcon-pizza-workshop)  
2. Click **Fork** in the top right corner.  
3. Select your GitHub account as the destination.  

This creates your own copy of the workshop repo.  

### 2. Start a Codespace  
1. In your forked repository, click the green **Code** button.  
2. Select the **Codespaces** tab.  
3. Click **Create codespace on main**.  

GitHub will now start a new Codespace using the provided **devcontainer configuration**.  
This will:  
- Build a container with Python 3.10  
- Create a virtual environment (`.venv`)  
- Install all dependencies from `requirements.txt`  

This step can take a few minutes the first time.  


### 3. Open the Workshop Directory  
When your Codespace starts, make sure you’re working inside the `workshop/` directory:  

```bash
cd workshop
```

All your Python files (`agent.py`, `tools.py`, etc.) should be created and run from here.  


### 4. Verify Your Environment  
Run the following to check that everything is set up correctly:  

```bash
python --version
```
Expected output: **Python 3.10.x**  

If you plan to use MCP servers configured in `.vscode/mcp.json`, also verify the common MCP runners are available:

```bash
uvx --version
npx --version
```


### 5. Start Coding 🚀  

From here, start with [the workshop](./1_microsoft-foundry).


## Recap  

In this setup section, you have:  
- Forked the workshop repo into your GitHub account  
- Started a GitHub Codespace with the provided devcontainer  
- Ensured Python 3.10 and dependencies are installed  
- Opened the `workshop/` directory as your working folder  

You’re now ready to build the **PizzaBot agent** step by step. 🍕🤖  

## Troubleshooting

### MCP runner commands not found

If you see errors like `uvx: command not found` or `dnx: command not found` when starting an MCP server, it usually means the devcontainer image doesn’t have the required runner installed.

- This workshop repo is set up to use MCP servers that run via `uvx` (Python) or `npx` (Node).
- If you added a server from an MCP gallery that references `dnx`, switch to a server config that uses `uvx`/`npx`, or install the missing runner.

If you see `npx: command not found`, install Node.js + npm (which provides `npx`) and then retry:

```bash
# Debian/Ubuntu-based containers
sudo apt-get update && sudo apt-get install -y nodejs npm

# Alpine-based containers
sudo apk add --no-cache nodejs npm

npx --version
```

If you’re using Codespaces and you changed the devcontainer definition, run **Codespaces: Rebuild Container** so the new tools get installed.
