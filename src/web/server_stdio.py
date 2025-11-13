from src.web.server import mcp

if __name__ == "__main__":
    # Using stdio transport for Claude Desktop
    mcp.run(transport="stdio")
