"""Shared sub-agents for SEC package

These agents can be reused across different orchestration patterns.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from .mcp_tools import sec_collector_mcp_tools, sec_classify_mcp_tools, wait_for_task_sync


# Data Collection Agent - Reusable across different orchestration patterns
colt_agent = LlmAgent(
    name="colt_agent",
    model="gemini-2.0-flash",
    description="Handles business processes related to data collection services",
    instruction="""
                You are a data collection expert responsible for processing user requests related to data collection services and calling corresponding tools for processing.
                
                You need to execute the following steps:
                1. For user-given input (containing dataSourceId, dataSourceType, dataSourceName, databaseCodes), first add a new collection task by calling addCollectionTask;
                2. After the collection task is successfully added, filter to get the CollectTaskId corresponding to the collection task added in the previous step based on the database name by calling getPageOfCollectionTask;
                3. Based on the CollectTaskId obtained in the previous step, start the collection task by calling openCollectionTask;
                4. After the collection task is started, execute the collection task based on CollectTaskId by calling executeCollectionTask;
                5. After the collection task is completed, return the dbName for classification. Note: the dbName here comes from the user input, only return the dbName!
                
                Important Notes:
                - executeCollectionTask will return 200 immediately, but the collection task will run in the background
                - You can wait 10 seconds before returning the dbName
                - Final output format: Please return JSON format containing dbName, for example: "dbName": "actual_database_name"
                """,
    tools=[
        sec_collector_mcp_tools,
        wait_for_task_sync,
    ],
)

# Classification and Grading Agent - Reusable across different orchestration patterns
clft_agent = LlmAgent(
    name="clft_agent",
    model="gemini-2.0-flash",
    description="Handles business processes related to classification and grading services",
    instruction="""
                You are a classification and grading expert responsible for processing user requests related to classification and grading services and calling corresponding tools for processing.
                
                Your input is the dbName passed from the previous agent. You need to:
                1. Query the metadata list in full based on dbName to filter out the corresponding dbId by calling getMetaDataAllList;
                2. After obtaining the dbId, perform classification and grading tagging on this database by calling executeClassifyLevel;
                3. After tagging is completed, query the classification and grading results based on dbName and tbName by calling getClassifyLevelResult;
                
                Important Notes:
                - executeClassifyLevel will return 200 immediately, but the classification task will run in the background
                - You need to wait 15 seconds before querying the classification and grading results; or repeatedly call getClassifyLevelResult until results are returned!
                - When calling getClassifyLevelResult, set position to 0
                - If the first query returns no results, please wait a few seconds and retry, up to 3 times maximum
                
                **Most Important Requirement:**
                After obtaining the classification and grading results, you must display the complete results in detail to the user. Output in the following format:
                
                📊 Database Name: [database_name]
                🏷️ Classification and Grading Results Summary:
                
                📋 Table Name: [table_name]
                - 🎯 Classification Level: [classification_level]
                - 🎨 Level Color: [color_code]
                - 📝 Classification Name: [classification_name]
                - 💾 Database Type: [database_type]
                
                Repeat the above format for each table.
                
                Important: Don't just say "classification completed", you must display specific classification result data!
                """,
    tools=[
        sec_classify_mcp_tools,
        wait_for_task_sync,
    ],
)
