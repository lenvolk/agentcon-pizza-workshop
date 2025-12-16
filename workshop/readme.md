## Before You Start: Authenticate with Azure

Before running any agent or data upload scripts, you must authenticate with Azure so the agent can access Microsoft Foundry resources.

1. Open a terminal in your Codespace or dev container.
2. Run:

	```bash
	az login --use-device-code
	```

	Follow the instructions in your browser to complete authentication.

3. (Optional) If you have multiple Azure subscriptions, set the correct one:

	```bash
	az account set --subscription "<subscription name or id>"
	```

You only need to do this once per Codespace/session. The agent will use your Azure CLI credentials automatically.

---

**start building here**