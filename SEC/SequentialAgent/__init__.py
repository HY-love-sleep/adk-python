"""Sequential execution pattern for SEC agents

This module implements a sequential agent that executes data collection
followed by classification and grading in a fixed order.
"""

from .agent import root_agent

__all__ = ["root_agent"]
