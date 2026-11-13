"""
JARVIS - Agent Manager
Менеджер для координации работы специализированных агентов
"""

from typing import Dict, List, Optional, Any
from .web_developer import WebDeveloperAgent
from .programmer import ProgrammerAgent
from .data_analyst import DataAnalystAgent


class AgentManager:
    """Менеджер для управления агентами JARVIS."""

    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self._register_default_agents()

    def _register_default_agents(self):
        """Регистрация стандартных агентов."""
        self.register_agent(WebDeveloperAgent())
        self.register_agent(ProgrammerAgent())
        self.register_agent(DataAnalystAgent())

    def register_agent(self, agent):
        """Зарегистрировать нового агента."""
        self.agents[agent.name] = agent

    def get_agent(self, name: str):
        """Получить агента по имени."""
        return self.agents.get(name)

    def find_suitable_agent(self, task: str):
        """Найти подходящего агента для задачи."""
        for agent in self.agents.values():
            if agent.can_handle(task):
                return agent
        return None

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить задачу с помощью подходящего агента."""
        agent = self.find_suitable_agent(task)

        if not agent:
            return {
                'status': 'error',
                'message': f'Не найден подходящий агент для задачи: {task}'
            }

        print(f"JARVIS: Передаю задачу агенту {agent.name}")
        result = agent.execute_task(task, context)
        agent.log_task(task, result)

        return result

    def list_agents(self) -> List[Dict[str, Any]]:
        """Получить список всех агентов."""
        return [agent.get_status() for agent in self.agents.values()]

    def get_agent_capabilities(self, name: str) -> List[str]:
        """Получить возможности конкретного агента."""
        agent = self.get_agent(name)
        return agent.capabilities if agent else []

    def get_task_history(self, agent_name: Optional[str] = None) -> List[Dict]:
        """Получить историю задач."""
        if agent_name:
            agent = self.get_agent(agent_name)
            return agent.task_history if agent else []

        # История всех агентов
        all_history = []
        for agent in self.agents.values():
            all_history.extend(agent.task_history)

        return sorted(all_history, key=lambda x: x['timestamp'], reverse=True)
