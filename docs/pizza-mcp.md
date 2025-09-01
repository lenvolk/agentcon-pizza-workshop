
# Pizza MCP server


| Endpoint | Url |
| -- | -- |
| Get Order Key | https://nice-dune-07e53ec0f.2.azurestaticapps.net/
| Dashboard | https://nice-dune-07e53ec0f.2.azurestaticapps.net/
| API Endpoint | https://func-pizza-api-sc6u2typoxngc.azurewebsites.net

## Overview

This is the Pizza MCP server, exposing the Pizza API as a Model Context Protocol (MCP) server. The MCP server allows LLMs to interact with the pizza ordering process through MCP tools.

This server supports the following transport types:
- **Streamable HTTP**
- **SSE** (legacy, not recommended for new applications)

## MCP tools

The Pizza MCP server provides the following tools:

| Tool Name | Description |
|-----------|-------------|
| get_pizzas | Get a list of all pizzas in the menu |
| get_pizza_by_id | Get a specific pizza by its ID |
| get_toppings | Get a list of all toppings in the menu |
| get_topping_by_id | Get a specific topping by its ID |
| get_topping_categories | Get a list of all topping categories |
| get_orders | Get a list of all orders in the system |
| get_order_by_id | Get a specific order by its ID |
| place_order | Place a new order with pizzas (requires `userId`) |
| delete_order_by_id | Cancel an order if it has not yet been started (status must be `pending`, requires `userId`) |

## Test with MCP inspector

First, you need to start the Pizza API and Pizza MCP server locally.

1. In a terminal window, start MCP Inspector:
    ```bash
    npx -y @modelcontextprotocol/inspector
    ```
2. Ctrl+click to load the MCP Inspector web app from the URL displayed by the app (e.g. http://127.0.0.1:6274)
3. In the MCP Inspector, set the transport type to **HTTP** and 
3. Put `http://localhost:3000/mcp` in the URL field and click on the **Connect** button.
4. In the **Tools** tab, select **List Tools**. Click on a tool and select **Run Tool**.

> [!NOTE]
> This application also provides an SSE endpoint if you use `/sse` instead of `/mcp` in the URL field. 
