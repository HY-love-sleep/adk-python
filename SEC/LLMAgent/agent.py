from __future__ import annotations
from google.adk.agents import LlmAgent, SequentialAgent

from shared.agents import make_colt_agent, make_clft_agent

# Full pipeline as a reusable sequential workflow
full_pipeline_agent = SequentialAgent(
    name="full_pipeline",
    description="Run collection then classification in order",
    sub_agents=[
        make_colt_agent("colt_for_pipeline"),
        make_clft_agent("clft_for_pipeline"),
    ],
)

# LLM router that intelligently chooses which path to run
root_agent = LlmAgent(
    name="sec_router",
    model="gemini-2.0-flash",
    description="Router that decides between collection-only, classification-only, or full pipeline",
    instruction="""
                You are a smart router. Decide which sub-agent to delegate to based on the user's request:
                - If the user asks to both collect data and then classify, delegate to full_pipeline.
                - If the user only wants data collection, delegate to colt_agent.
                - If the user only wants classification/grading, delegate to clft_agent.

                Use LLM-driven delegation (transfer_to_agent) to hand off to exactly one target agent.
                If the user intent is ambiguous, ask a brief clarifying question.
                """,
    sub_agents=[
        full_pipeline_agent,
        make_colt_agent("colt_for_router"),
        make_clft_agent("clft_for_router"),
    ],
)