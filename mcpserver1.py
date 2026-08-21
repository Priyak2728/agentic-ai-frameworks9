from mcp.server.fastmcp import FastMCP
import psutil

# Create MCP Server
mcp = FastMCP("System-Monitor-MCP")


@mcp.tool()
def get_cpu_usage() -> str:
    """
    Returns current CPU utilization.
    """
    cpu = psutil.cpu_percent(interval=1)
    return f"Current CPU Usage: {cpu}%"


@mcp.tool()
def get_memory_usage() -> str:
    """
    Returns current memory utilization.
    """
    memory = psutil.virtual_memory()

    return (
        f"Memory Usage: {memory.percent}%\n"
        f"Available Memory: "
        f"{round(memory.available / (1024**3), 2)} GB"
    )


if __name__ == "__main__":

    print("Testing MCP Tools...\n")

    print(get_cpu_usage())
    print()
    print(get_memory_usage())

    print("\nMCP Server Running...")

    mcp.run()