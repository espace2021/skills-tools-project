from fastmcp import FastMCP
from mcpServer import tools_cars,tools_emails
import asyncio
from fastapi import FastAPI


mcp_server = FastMCP("Research MCP Server")
tools_cars.register_tools(mcp_server)
tools_emails.register_tools(mcp_server)


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}


async def main():
    # Lancer le serveur (bloquant)
    await mcp_server.run_async(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
        path="/mcp",
    )


if __name__ == "__main__":
    asyncio.run(main())