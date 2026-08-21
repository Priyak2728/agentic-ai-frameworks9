import boto3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["weather_mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available Tools:")
            print(tools)

            result = await session.call_tool(
                "get_weather",
                {
                    "city": "Mumbai"
                }
            )

            print(result)

asyncio.run(main())