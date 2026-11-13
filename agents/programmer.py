"""
JARVIS - Programmer Agent
Агент для написания кода на различных языках программирования с AI
"""

from .base_agent import BaseAgent
from .ai_service import get_ai_service
from typing import Dict, Optional, Any


class ProgrammerAgent(BaseAgent):
    """Агент для написания кода."""

    def __init__(self):
        super().__init__(
            name="Programmer",
            description="Написание кода на Python, JavaScript, C++, Java и других языках с AI"
        )
        self.capabilities = [
            "Написание Python кода",
            "Создание JavaScript/TypeScript",
            "Генерация C++ кода",
            "Создание Java приложений",
            "Написание SQL запросов",
            "Создание скриптов автоматизации",
            "Рефакторинг кода",
            "Оптимизация производительности",
            "AI-генерация кода"
        ]
        self.ai_service = get_ai_service()

    def can_handle(self, task: str) -> bool:
        """Проверить, может ли агент обработать задачу."""
        keywords = [
            "код", "программа", "скрипт", "python", "javascript", "c++", "java",
            "функция", "класс", "алгоритм", "написать код", "разработка",
            "программирование", "sql", "база данных"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in keywords)

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить задачу по написанию кода."""
        context = context or {}

        # Пытаемся использовать AI для генерации
        if self.ai_service.client:
            return self._execute_with_ai(task, context)
        else:
            # Fallback на шаблоны если AI недоступен
            return self._execute_with_templates(task, context)

    def _execute_with_ai(self, task: str, context: Dict) -> Dict[str, Any]:
        """Выполнить задачу с помощью AI."""
        # Определяем язык программирования
        language = self._detect_language(task)

        result = self.ai_service.generate_code(
            task=task,
            agent_type="programmer",
            context=context,
            language=language
        )

        if result['status'] == 'success':
            # Парсим блоки кода из ответа AI
            files = self.ai_service.parse_code_blocks(result['code'])

            return {
                'status': 'success',
                'type': 'ai_generated',
                'message': f'AI написал код: {task}',
                'files': files,
                'language': language,
                'tokens_used': result.get('tokens_used', 0),
                'model': result.get('model', 'unknown')
            }
        else:
            # Если AI ошибка, используем шаблоны
            return self._execute_with_templates(task, context)

    def _execute_with_templates(self, task: str, context: Dict) -> Dict[str, Any]:
        """Выполнить задачу с помощью шаблонов (fallback)."""
        # Определяем язык программирования
        if "python" in task.lower():
            return self._create_python(task, context)
        elif "javascript" in task.lower() or "js" in task.lower():
            return self._create_javascript(task, context)
        elif "sql" in task.lower() or "запрос" in task.lower():
            return self._create_sql(task, context)
        else:
            return self._create_generic_code(task, context)

    def _detect_language(self, task: str) -> str:
        """Определить язык программирования из задачи."""
        task_lower = task.lower()

        if "python" in task_lower:
            return "python"
        elif "javascript" in task_lower or "js" in task_lower:
            return "javascript"
        elif "typescript" in task_lower or "ts" in task_lower:
            return "typescript"
        elif "c++" in task_lower or "cpp" in task_lower:
            return "cpp"
        elif "java" in task_lower:
            return "java"
        elif "sql" in task_lower or "запрос" in task_lower:
            return "sql"
        else:
            return "python"  # По умолчанию

    def _create_python(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать Python код."""
        return {
            'status': 'success',
            'type': 'python_code',
            'message': f'Создаю Python код: {task}',
            'files': {
                'main.py': self._generate_python_template(task)
            }
        }

    def _create_javascript(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать JavaScript код."""
        return {
            'status': 'success',
            'type': 'javascript_code',
            'message': f'Создаю JavaScript код: {task}',
            'files': {
                'script.js': self._generate_javascript_template(task)
            }
        }

    def _create_sql(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать SQL запрос."""
        return {
            'status': 'success',
            'type': 'sql_query',
            'message': f'Создаю SQL запрос: {task}',
            'files': {
                'query.sql': self._generate_sql_template(task)
            }
        }

    def _create_generic_code(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать универсальный код."""
        return {
            'status': 'success',
            'type': 'generic_code',
            'message': f'Создаю код: {task}',
            'files': {
                'code.txt': self._generate_generic_template(task)
            }
        }

    def _generate_python_template(self, task: str) -> str:
        """Генерация Python шаблона."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
Создано JARVIS Programmer Agent
"""

import sys
from typing import List, Dict, Optional


def main():
    """Главная функция."""
    print("JARVIS Programmer Agent: Запуск программы")
    print("Задача: {task}")

    # Здесь будет основная логика
    pass


if __name__ == "__main__":
    main()
"""

    def _generate_javascript_template(self, task: str) -> str:
        """Генерация JavaScript шаблона."""
        return f"""// {task}
// Создано JARVIS Programmer Agent

'use strict';

class TaskExecutor {{
    constructor() {{
        this.task = '{task}';
        console.log('JARVIS Programmer Agent: Инициализация');
    }}

    execute() {{
        console.log(`Выполняю задачу: ${{this.task}}`);
        // Здесь будет основная логика
    }}
}}

// Запуск
const executor = new TaskExecutor();
executor.execute();
"""

    def _generate_sql_template(self, task: str) -> str:
        """Генерация SQL шаблона."""
        return f"""-- {task}
-- Создано JARVIS Programmer Agent

-- Пример SELECT запроса
SELECT *
FROM users
WHERE active = true
ORDER BY created_at DESC
LIMIT 100;

-- Пример INSERT запроса
INSERT INTO tasks (name, description, status)
VALUES ('{task}', 'Автоматически созданная задача', 'pending');

-- Пример UPDATE запроса
UPDATE tasks
SET status = 'completed',
    updated_at = NOW()
WHERE id = 1;
"""

    def _generate_generic_template(self, task: str) -> str:
        """Генерация универсального шаблона."""
        return f"""// {task}
// Создано JARVIS Programmer Agent

// Укажите язык программирования и требования
// для более точной генерации кода

function main() {{
    console.log('JARVIS Programmer Agent');
    console.log('Задача: {task}');
}}

main();
"""
