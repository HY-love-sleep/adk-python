"""Shared MCP tools and utility functions for SEC agents"""

from __future__ import annotations

from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams


# Data Collection MCP Toolset
sec_collector_mcp_tools = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://172.16.22.18:8081/mcp/sec-collector-management/sse",
        headers={
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache',
        },
        timeout=50.0,
        sse_read_timeout=120.0,
    ),
    tool_filter=[
        "addCollectionTask",
        "getPageOfCollectionTask",
        "openCollectionTask",
        "executeCollectionTask"
    ]
)

# Classification and Grading MCP Toolset  
sec_classify_mcp_tools = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://172.16.22.18:8081/mcp/sec-classify-level/sse",
        headers={
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache',
        },
        timeout=50.0,
        sse_read_timeout=120.0,
    ),
    tool_filter=[
        "getMetaDataAllList",
        "executeClassifyLevel",
        "getClassifyLevelResult"
    ]
)


def wait_for_task_sync(seconds: int = 10) -> str:
    """Synchronous wait tool for background task processing
    
    Args:
        seconds: Number of seconds to wait
        
    Returns:
        Status message indicating wait completion
    """
    import time
    time.sleep(seconds)
    return f"Waited for {seconds} seconds"
