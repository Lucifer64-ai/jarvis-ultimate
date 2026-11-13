"""
JARVIS - Agents Module
Система специализированных агентов для выполнения задач
"""

from .base_agent import BaseAgent
from .web_developer import WebDeveloperAgent
from .programmer import ProgrammerAgent
from .data_analyst import DataAnalystAgent
from .agent_manager import AgentManager

__all__ = [
    'BaseAgent',
    'WebDeveloperAgent',
    'ProgrammerAgent',
    'DataAnalystAgent',
    'AgentManager'
]
