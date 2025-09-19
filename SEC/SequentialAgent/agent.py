from __future__ import annotations
from google.adk.agents import SequentialAgent

try:
  from SEC.shared import colt_agent, clft_agent
except ModuleNotFoundError:
  from shared import colt_agent, clft_agent

root_agent = SequentialAgent(
    name="sec_sequential_agent",
    description="Sequential execution of data collection and classification",
    sub_agents=[colt_agent, clft_agent],
)