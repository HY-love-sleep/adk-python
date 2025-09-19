"""LLM Coordinator pattern for SEC agents

This module implements an intelligent coordinator that can dynamically
route requests to appropriate sub-agents based on user input.
"""

from .agent import root_agent

__all__ = ["root_agent"]
