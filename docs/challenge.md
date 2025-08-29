# Challenge: Build an agent to order pizza

**Duration**: 3 hours

Complete the Challenge below within the time provided. The challenge is broken up into steps called Levels. Reach Level 7 to complete the Challenge.

## The Challenge

Build a code-first AI Agent that can order pizza using the Azure AI Agent Service. The agent will interpret the user's request and make an order via the provided Pizza API.

In this challenge you will:
- Use the AI Agent Project SDK
- Create an Azure AI Foundry resource 
- Deploy a model
- Write instructions
- Add knowledge to your agent
- Use tools 
- Connect to an MCP Server or API
- Change from text input to visual input
- Use the code interpreter


## Level 1: Interact with Azure AI Foundry

In this first level we will set up Azure AI Foundry and deploy your first model.

### 📋Tasks

1. Follow your facilitators instructions to log into  your provided Azure subscription
1. Sign in to Azure AI Foundry at https://ai.azure.com
1. Create an Azure AI Foundry resource for your project
1. Deploy a GPT-4o model for your project
1. Launch the playground for your deployed model
1. OPTIONAL: Share your completion of this level in the #open-hack channel of the [Azure AI Foundry Discord](https://aka.ms/open-hack/discord) (and do this for later levels, too):

```
I have achieved Level 1 of the Open Hack "Build An Agent to Order Pizza" 🍕
```

### 📚 Resources

- [Quickstart: Get started with Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/quickstarts/get-started-code?tabs=azure-ai-foundry&pivots=fdp-project)

- [Deploy AI models in Azure AI Foundry](https://aka.ms/openhack/aifoundry)

### ✅ Pass Criteria and Requirements

You can interact with your deployed model in the playground.

Your deployed model responds to the prompt "Order me a cheese pizza" with any response.

### 🛠️ Hints and Tips

If you haven't been provided with an Azure suscription, you can use your own or [sign up for an account](https://azure.microsoft.com/pricing/purchase-options/azure-account). 

The first thing you will do in Azure AI Foundry is create a Project resource. Give your AI Foundry project a unique name — something like `myname-openhack-pizza` will work. 

The AI Foundry Agent can answer your questions about how to achieve tasks. Click the 
<img src="img/foundry-agent.png" alt="AI Foundry Agent" width="20">
icon in the header bar to open the AI Foundry Agent.

An easy way to deploy a model is to find it in the model catalog, and then click the "Use this model" button.

Use the Autodeploy options in the Azure AI Agent Service quickstart to deploy a model and connected resources: [Create an AI Agent with Azure AI Agent Service](https://aka.ms/openhack/aiagentservice)
  

## Level 2: Set up your dev environment and create your first agent

In this level we will configure your development environment and install requirements in the local file system.

### 📋Tasks

1. Launch your editing environment of choice, for example:
    - GitHub Codespaces, on this repository
    - Visual Studio Code, on the provided Virtual Machine
    - Visual Studio or another IDE on your own laptop

2. Install the Azure AI Foundry SDK for the language of your choice
1. Connect to Azure AI Foundry
1. Create a basic agent that says hello

### 📚 Resources

- [Quickstart for GitHub Codespaces](https://docs.github.com/codespaces/quickstart)

- [Install Azure CLI](https://aka.ms/openhack/azurecli)

- [How to use `az login`](https://aka.ms/openhack/azlogin)

- [Quickstart: Create an new agent](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure)

### ✅ Pass Criteria and Requirements

Your agent appears in Azure AI Foundry, in the "Agents" tab.

You can launch your agent from the command line and from the Azure AI Foundry Agent Playground.

Your agent responds "hello" to your input.

### 🛠️ Hints and Tips

Things will be easier if you use GitHub Codespaces, especially for Python developers. If you do, the following tools will be pre-installed for you in the dev container:

  - A recent version of [python](https://www.python.org/downloads/)
  - The [Azure CLI](https://learn.microsoft.com/cli/azure/?view=azure-cli-latest)
  - A `myagent` folder for sandbox development (this folder will not be tracked by git)

(You'll need to make sure these tools are available to you otherwise.)

Use `az login` to log in to your Azure Subscription via the Azure CLI.

You could ask GitHub Codespaces Agent to "create an agent using Azure AI Foundry SDK that always responds 'Hello' to any input" to get started.

To create your agent from scratch, use either the [Azure AI Foundry Agent Playground](https://aka.ms/openhack/agent-playground) or Azure AI Agent Service code samples in [Python](https://aka.ms/openhack/agent-python-sample) or [.NET](https://aka.ms/openhack/agent-dotnet) to create an AI Agent and confirm the service is properly working.


## Level 3: Add instructions and persistent memory

We will give our first set of instruction to the agent and give it a personality in this level.

### 📋Tasks

1. Give the agent a personality suitable for your pizza brand
1. Make sure the agent asks for the customer's name before making an order
1. Instruct the agent to only respond to pizza ordering related questions

### ✅ Pass Criteria and Requirements

Your agent has your desired personality and can carry on a conversation about pizza. 

Your agent asks your name, and remembers it later in the conversation.

Your agent understands a request to order a pizza (even if it can't actually make an order yet). 

Your agent doesn't attempt to act on non-pizza-related questions.

### 📚 Resources

* [Threads, Runs, and Messages in Azure AI Foundry Agent Service](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/threads-runs-messages)

### 🛠️ Hints and Tips

If your agent can't remember your name, make sure you are not creating a new thread for each chat  interaction.

You may find you have multiple agents with the same name in AI Foundry. Give your agent a distinctive name (e.g. "Level 3 Pizza Agent") and write code to replace any existing agent by that name to make it easier to keep track.

Can't think of a personality to use? Feel free to adapt the instructions below:

    You are an agent that helps customers order pizzas from Contoso pizza.
    You have a Gen-alpha personality, so you are friendly and helpful, but also a bit cheeky.
    You can provide information about Contoso Pizza and its retail stores.
    You help customers order a pizza of their chosen size, crust, and toppings.
    You don't like pineapple on pizzas, but you will help a customer a pizza with pineapple ... with some snark.
    Make sure you know the customer's name before placing an order on their behalf.
    You can't do anything except help customers order pizzas and give information about Contoso Pizza. You will gently deflect any other questions.

## Level 4: Give your agent knowledge

We will give our agent information about stores the customer can order from.

### 📋Tasks

- Make the agent respond to questions about stores, based on the files in the data/store-information folder
- Make sure the agent asks which store to contact before confirming an order

### ✅ Pass Criteria and Requirements

Your agent can list the available Contoso Pizza stores and answer questions about them.

Your agent about a store location before confirming an order.

### 📚 Resources

* Quickstart: [Add files to the agent](https://learn.microsoft.com/azure/ai-foundry/quickstarts/get-started-code?tabs=python&pivots=fdp-project#add-files-to-the-agent)

### 🛠️ Hints and Tips

A tempting solution is to embed the store information in the prompt, but this solution won't scale. Instead, add knowledge to the agent in AI Foundry. This documentation may help: https://ai.azure.com/doc/azure/ai-foundry/agents/how-to/tools/overview

## Level 5: Add a pizza estimation function

We will give our agent the ability to estimate the appropriate amount of pizza to order, if asked.

### 📋Tasks

- Add a function to the agent to calculate the amount of pizza needed

### 📚 Resources

- [Azure AI Agents function calling](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/function-calling?pivots=python)

### ✅ Pass Criteria and Requirements

Your agent suggests a reasonable amount of pizza given the number of people and their appetite level.

Your agent asks for information about the diners to make that calculation.

### 🛠️ Hints and Tips

Create a simple function in Python or your language of choice that returns the size or amount of pizza needed for a given number of people, and add that function as a tool for the agent.

A large pizza is generally suitable for two adults and two children.


## Level 6: Connect the to the ordering service via the API

We have provided an API for your agent to make orders with Contoso Pizza directly. In this level we will verify the API connection is working before converting to an MCP-based connection in the next level.

### 📋Tasks

- Connect the agent to the Pizza API 

### 📚 Resources

* [Pizza API](https://github.com/Azure-Samples/pizza-mcp-agents)

### ✅ Pass Criteria and Requirements

Your agent can successfully retrieve the pizza menu and give information about available toppings.

Your agent can place an order for a pizza, and the order appears on the dashboard in the room.

### 🛠️ Hints and Tips

For Open Hack events, a Pizza API service has been deployed and is connected to the dashboard showing in the room. Your instructor will provide the endpoint to use.

If you're not at an open hack event, you can deploy the pizza service independently.


## Level 7: Connect to the Pizza MCP Server

Now that you have verified the API connection works, we will connect the agent to an MCP server instead of interfacing with the API directly. This gives Contoso Pizza the ability to add new capabilities to the agent more easily.

Your instructor will give you the URL for the Pizza MCP Server.

### 📋Tasks
- Create a Contoso Pizza ID user ID (your instuctor will provide the URL)
- Replace the API integration by and use MCP instead
- Provide the user ID to your agent for use in the System prompt
- Create clear instructions

### 📚 Resources

- [Documentation: adding MCP servers to agents in AI Foundry](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/model-context-protocol)

### ✅ Pass Criteria and Requirements

Your agent can take an order for pizza, and it appears on the in-room dashboard.

The AI Agent can provide the status of the customer's pizza order(s).

Your agent can cancel an order after it has been placed, if the cancellation is requested quickly enough.

### 🛠️ Hints and Tips

For Open Hack events, your instructor will provide the URL of the MCP server to use.

- You can test the MCP server with an existing AI chat UI that supports MCP integration. Some suggestions are: [Chainlit](https://docs.chainlit.io/advanced-features/mcp), [Visual Studio Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) or [Visual Studio](https://learn.microsoft.com/en-us/visualstudio/ide/mcp-servers?view=vs-2022).

- Semantic Kernel has built-in support for MCP Servers for both [Python](https://devblogs.microsoft.com/semantic-kernel/semantic-kernel-adds-model-context-protocol-mcp-support-for-python/) and [.NET](https://devblogs.microsoft.com/semantic-kernel/integrating-model-context-protocol-tools-with-semantic-kernel-a-step-by-step-guide/).

    - [Semantic Kernel MCP Server with Plugins - Python](https://github.com/microsoft/semantic-kernel/blob/main/python/samples/concepts/mcp/agent_with_mcp_plugin.py)
    - [Semantic Kernel MCP Server with Plugins - .NET](https://github.com/microsoft/semantic-kernel/tree/main/dotnet/samples/Demos/ModelContextProtocolPlugin) 

- If you are using other frameworks:

    - [Building Java AI Agents using LangChain4j and Dynamic Sessions](https://developer.microsoft.com/en-us/reactor/events/25337/)

    - [Model Context Protocol (MCP) with LangChain4j](https://github.com/langchain4j/langchain4j/blob/main/docs/docs/tutorials/mcp.md)

    - [LangChain JS MCP Adapters](https://github.com/langchain-ai/langchainjs-mcp-adapters)

- If you are interested in creating your own MCP Server, you will the [MCP for Beginners](https://aka.ms/openhack/mcp-for-beginners) a useful guide.


# **Challenge completed!**

Congratulations, you have successfuly created a Pizza Agent satisfying the requirements of Contoso Pizza! 

## Save your agent

To save the code you created: 

* Delete the file `.gitignore` (this file suppresses changes to the `myagent` folder)
* Sync your changes from GitHub Codespaces to save the scripts you created in your own fork in GitHub.

## Optional: Celebrate your success

Share your achievement in the #open-hack channel of the [Azure AI Foundry Discord](https://aka.ms/open-hack/discord).

    I have completed the final level of the Open Hack "Build An Agent to Order Pizza" 🍕

# Want to Keep going?

If you have time left, here are some other challenges to try, or try them at home after the Open Hack.

 For questions outside of the Open Hack, we created the Azure AI Foundry Developer Community — your one-stop hub for 🌐 a vibrant forum for Q&A + code,
🎙️ DevBlogs with the latest updates,
and 🎮 real-time Discord chats, events & learning.

* Post in the [Azure AI Foundry Forum](https://github.com/orgs/azure-ai-foundry/discussions) in GitHub Discussions 
* [Hop on the Azure AI Foundry Discord](https://aka.ms/open-hack/discord)

## Extra Level 8: Accept Voice Based Orders

In this level, you will enable order creation by voice. You will create an AI Agent that allows users to place orders through voice commands.

### ✅ Pass Criteria

You have completed this checkpoint if:
    - You have deployed a model using supports either speech-to-text or speech-to-speech.
    - The AI Agent can correctly identify the pizza order based on the voice input.
    - The user receives a confirmation of the order being successfully created.

### Hints and Tips

- Deploy a speech to text or speech-to-speech model using the Azure AI Foundry that supports audio input.

- Design a flow that allows that allows the user to speak to the AI Agent, confirm the order and then create the order. (The Azure AI Foundry Agent playground provides a UI for providing audio input.)

- Plan out each step of the process and what models or tools are needed for each step, including first speech recognition, then order creation.

### 📚 Resources

* [How to use the GPT-4o Realtime API for speech and audio (Preview)](https://aka.ms/openhack/realtime)
* [Azure OpenAI RealTime Voice with Agents in Chainlit](https://aka.ms/openhack/realtime-chainlit)


## Extra Level 8: Visual ordering

In this level, you will enable order creation by images. You will create an AI Agent that allows users to upload a picture of pizza and based on the picture of that pizza, the order is created.

### 📋Tasks

- Add the capability to take an image as input
- Use the image to order a pizza (I want to order a pizza like this one the image)
- Make sure it breaks it down in toppings and matches the right base pizza and add the extra toppings

### 📚 Resources

[Get started with multimodal vision chat apps using Azure OpenAI](https://aka.ms/openhack/vision-chat)

### ✅ Pass Criteria

You have completed this level if:

- The AI Agent can identify the pizza in the image and create the order.

- The user recieves a confirmation of the order being successfully created.

### 🛠️ Hints and Tips

- Deploy a multi-modal model that supports image input to Azure AI Foundry. 

- Design a flow that allows the user to upload an image of a pizza. (The Azure AI Foundry Agent playground provides a UI for uploading images.)

- Plan out each step of the process and what models or tools are needed for each step, including first image recognition, then order creation.


## Extra Level 9: Code interpreter

- Add the capbility to create graphical reports based on the data in data/sales-data
- Enable code interpreter
- Add data
- Ask to create graphs

## Extra Level 10: Add content filtering

- Create a content filter
- You should not be able to order a pizza with poison 

## Extra Level 11: Clean up your code for production

- Make sure no secrets like the Contoso user ID are included in your Python/C# files. 

### 🛠️ Hints and Tips

Move secrets to the `.env` file instead.