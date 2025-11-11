from fastmcp import Client
import asyncio


async def main():
    # async with Client("server.py") as client:
    async with Client("http://127.0.0.1:8080/mcp") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print(f"Result: {result}")
        resources = await client.list_resources()
        print(f"Resources: {resources}")


asyncio.run(main())
