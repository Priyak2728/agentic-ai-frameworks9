# file: simple_mcp_server.py

import asyncio
import sys
import json
import requests

from mcp.server import Server
from mcp.types import Tool, TextContent

# 🔹 Create MCP server
server = Server(name="weather-mcp-server")

# 🔹 TOOL EXECUTION (REAL API)
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "get_weather":
        city = arguments.get("city", "Unknown")

        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url)
            response.encoding = "utf-8"

            return [TextContent(type="text", text=response.text)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error fetching weather: {str(e)}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]

# 🔹 TOOL DISCOVERY (MCP)
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., Mumbai, London)"
                    }
                },
                "required": ["city"]
            }
        )
    ]

# 🔹 MAIN LOOP (CLIENT SIMULATION)
async def main():
    print(" MCP Server ready", file=sys.stderr)

    tools = await list_tools()
    print("\n Available Tools:", file=sys.stderr)
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}", file=sys.stderr)

    print("\n Send JSON like:", file=sys.stderr)
    print('{"tool": "get_weather", "arguments": {"city": "Mumbai"}}\n', file=sys.stderr)

    while True:
        line = await asyncio.to_thread(sys.stdin.readline)

        if not line or not line.strip():
            continue

        try:
            data = json.loads(line.strip())

            tool_name = data.get("tool", "")
            args = data.get("arguments", {})

            result = await handle_call_tool(tool_name, args)

            response = {
                "status": "success",
                "result": [r.text if hasattr(r, "text") else str(r) for r in result]
            }

            print(json.dumps(response))

        except json.JSONDecodeError:
            print(json.dumps({"status": "error", "error": "Invalid JSON"}))

        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e)}))

# 🔹 RUN SERVER
if __name__ == "__main__":
    print("🚀 Starting MCP Server...", file=sys.stderr)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n MCP Server stopped", file=sys.stderr)