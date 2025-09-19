from __future__ import annotations
from google.adk.agents import LlmAgent

try:
  from SEC.shared import colt_agent, clft_agent
except ModuleNotFoundError:
  from shared import colt_agent, clft_agent

root_agent = LlmAgent(
    name="sec_coordinator",
    model="gemini-2.0-flash",
    description="Intelligent coordinator for flexible workflow execution",
    instruction="""
                You are a smart coordinator. Based on user input, decide the execution path:
                - Full pipeline: Use collection_agent then classification_agent
                - Collection only: Use collection_agent only  
                - Classification only: Use classification_agent only
                """,
    sub_agents=[
        colt_agent,
        clft_agent,
    ]
)