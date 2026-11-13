"""
JARVIS - Agent Manager
     
"""

from typing import Dict, List, Optional, Any
from .base_agent import BaseAgent
from .web_developer import WebDeveloperAgent
from .programmer import ProgrammerAgent
from .data_analyst import DataAnalystAgent
from .designer import DesignerAgent
from .devops import DevOpsAgent


class AgentManager:
    """    JARVIS."""

    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self._register_default_agents()

    def _register_default_agents(self):
        """  ."""
        self.register_agent(WebDeveloperAgent())
        self.register_agent(ProgrammerAgent())
        self.register_agent(DataAnalystAgent())
        self.register_agent(DesignerAgent())
        self.register_agent(DevOpsAgent())

    def register_agent(self, agent):
        """  ."""
        self.agents[agent.name] = agent

    def get_agent(self, name: str):
        """   ."""
        return self.agents.get(name)

    def find_suitable_agent(self, task: str):
        """    ."""
        for agent in self.agents.values():
            if agent.can_handle(task):
                return agent
        return None

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """     ."""
        agent = self.find_suitable_agent(task)

        if not agent:
            return {
                'status': 'error',
                'message': f'     : {task}'
            }

        print(f"JARVIS:    {agent.name}")
        result = agent.execute_task(task, context)
        agent.log_task(task, result)

        return result

    def list_agents(self) -> List[Dict[str, Any]]:
        """   ."""
        return [agent.get_status() for agent in self.agents.values()]

    def get_agent_capabilities(self, name: str) -> List[str]:
        """   ."""
        agent = self.get_agent(name)
        return agent.capabilities if agent else []

    def get_task_history(self, agent_name: Optional[str] = None) -> List[Dict]:
        """  ."""
        if agent_name:
            agent = self.get_agent(agent_name)
            return agent.task_history if agent else []

        #   
        all_history = []
        for agent in self.agents.values():
            all_history.extend(agent.task_history)

        return sorted(all_history, key=lambda x: x['timestamp'], reverse=True)
