from __future__ import annotations

import asyncio
from google.adk.agents import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams

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


async def wait_for_task(seconds: int = 10) -> str:
    """Wait for the specified number of seconds for background task processing"""
    await asyncio.sleep(seconds)
    return f"{seconds} s has been waited"


def wait_for_task_sync(seconds: int = 10) -> str:
    """Synchronous wait tool (if it doesn't work asynchronously)"""
    import time
    time.sleep(seconds)
    return f"{seconds} s has been waited"


colt_agent = Agent(
    name="colt_agent",
    model="gemini-2.0-flash",
    description="处理采集程序服务相关的业务流程",
    instruction="""
                你是数据采集专家，负责处理用户对采集程序服务的相关请求，并调用对应工具进行处理。
                
                你需要按以下步骤执行：
                1. 对于用户给定输入（包含dataSourceId、dataSourceType、dataSourceName、databaseCodes），首先新增一个采集任务，调用addCollectionTask；
                2. 采集任务新增成功后，根据数据库名称，获取上一步新增的采集任务对应的CollectTaskId，调用getPageOfCollectionTask进行过滤；
                3. 根据上一步得到的CollectTaskId，开启采集任务，调用openCollectionTask；
                4. 采集任务开启后，根据CollectTaskId，执行采集任务，调用executeCollectionTask；
                5. 采集任务完成后，返回dbName供分类。注意，这里的dbName从用户输入中获取，只返回dbName！
                
                重要提示：
                - executeCollectionTask会立即返回200，但是采集任务会在后台运行
                - 你可以等待10秒后再返回dbName
                - 最终输出格式：{"dbName": "实际的数据库名称"}
""",
    tools=[
        sec_collector_mcp_tools,
        wait_for_task_sync,
    ],
)

clft_agent = Agent(
    name="clft_agent",
    model="gemini-2.0-flash",
    description="处理分类分级服务相关的业务流程",
    instruction="""
                你是分类分级专家，负责处理用户对分类分级服务的相关请求，并调用对应工具进行处理。
                
                你的输入是上一个agent传递的dbName，你需要：
                1. 对元数据列表进行全量查询，根据dbName筛选出对应的dbId，调用getMetaDataAllList；
                2. 得到dbId后，对这个数据库进行分类分级打标，调用executeClassifyLevel；
                3. 打标完成后，根据dbName和tbName，查询分类分级结果，调用getClassifyLevelResult, 给出对应的结构化结果！；
                
                重要提示：
                - executeClassifyLevel会立即返回200，但是分类任务会在后台运行
                - 你需要等待15秒后再去查询分类分级结果；或者重复调用getClassifyLevelResult，直到返回结果！
                - 调用getClassifyLevelResult时，position填写0
                - 如果第一次查询没有结果，请等待几秒后重试，最多重试3次
                
                **最重要的要求：**
                - 当你获取到分类分级结果后，必须将完整的结果详细展示给用户
                - 请按以下格式输出结果：
                  ```
                  📊 数据库名称: [数据库名称]
                    🏷️ 分类分级结果汇总：
                    
                    📋 表名: [表名]
                    - 🎯 分类等级: [分类等级]
                    - 🎨 等级颜色: [颜色代码]
                    - 📝 分类名称: [分类名称]
                    - 💾 数据库类型: [数据库类型]

                  
                  [对每个表重复上述格式]
                  ```
                - 不要只说"已经分类完成"，必须显示具体的分类结果数据
""",
    tools=[
        sec_classify_mcp_tools,
        wait_for_task_sync,
    ],
)

root_agent = SequentialAgent(
    name="sec_agent",
    description="数据安全分类分级安全助手",
    sub_agents=[
        colt_agent,
        clft_agent,
    ],
)
