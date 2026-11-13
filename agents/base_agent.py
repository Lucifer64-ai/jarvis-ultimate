"""
JARVIS - Base Agent Class
Базовый класс для всех специализированных агентов
"""

from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import json
from datetime import datetime


class BaseAgent(ABC):
    """Базовый класс для всех агентов JARVIS."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.capabilities: List[str] = []
        self.task_history: List[Dict] = []
        self.is_active = False

    @abstractmethod
    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить задачу. Должен быть реализован в наследниках."""
        pass

    @abstractmethod
    def can_handle(self, task: str) -> bool:
        """Проверить, может ли агент обработать задачу."""
        pass

    def log_task(self, task: str, result: Dict[str, Any]):
        """Логирование выполненной задачи."""
        self.task_history.append({
            'task': task,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'agent': self.name
        })

    def get_status(self) -> Dict[str, Any]:
        """Получить статус агента."""
        return {
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'capabilities': self.capabilities,
            'tasks_completed': len(self.task_history)
        }

    def __repr__(self):
        return f"<{self.name}: {self.description}>"
