
# Pizza MCP server

For this workshop we use the Open Source example [Pizza MCP Agent](https://github.com/Azure-Samples/pizza-mcp-agents).

This project demonstrates how to build AI agents that can interact with real-world APIs using the Model Context Protocol (MCP). It features a complete pizza ordering system with a serverless API, web interfaces, and an MCP server that enables AI agents to browse menus, place orders, and track order status.

The system consists of multiple interconnected services:
- **Pizza MCP server:** MCP server enabling AI agent interactions
- **Pizza web app:** Live order dashboard, showing real-time pizza orders status
- **Registration system:** User registration for accessing the pizza ordering system

|  Name | Description |
|-----------|-------------|
| Pizza MCP server | [<!--@include: ./variables/mcp-url.md-->](<!--@include: ./variables/mcp-url.md-->)|
| Pizza web app | [<!--@include: ./variables/pizza-dashboard.md-->](<!--@include: ./variables/pizza-dashboard.md-->)|
| Registration system | [<!--@include: ./variables/customer-registration.md-->](<!--@include: ./variables/customer-registration.md-->) |


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
3. In the MCP Inspector, set the transport type to **SSE** and 
3. Put `<!--@include: ./variables/mcp-url.md-->` in the URL field and click on the **Connect** button.
4. In the **Tools** tab, select **List Tools**. Click on a tool and select **Run Tool**.

> [!NOTE]
> This application also provides an SSE endpoint if you use `/sse` instead of `/mcp` in the URL field. 
