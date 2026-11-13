"""
JARVIS - DevOps Agent
Агент для CI/CD, автоматизации развёртывания и инфраструктуры
"""

from .base_agent import BaseAgent
from .ai_service import get_ai_service
from typing import Dict, Optional, Any


class DevOpsAgent(BaseAgent):
    """Агент для DevOps задач."""

    def __init__(self):
        super().__init__(
            name="DevOps",
            description="CI/CD, Docker, автоматизация развёртывания с AI"
        )
        self.capabilities = [
            "Создание Docker файлов",
            "Генерация CI/CD конфигов",
            "Автоматизация развёртывания",
            "Создание bash скриптов",
            "Конфигурация серверов",
            "Мониторинг и логирование",
            "AI-генерация инфраструктуры"
        ]
        self.ai_service = get_ai_service()

    def can_handle(self, task: str) -> bool:
        """Проверить, может ли агент обработать задачу."""
        keywords = [
            "docker", "ci/cd", "развёртывание", "деплой", "deploy",
            "автоматизация", "bash", "скрипт", "сервер", "nginx",
            "github actions", "gitlab ci", "инфраструктура"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in keywords)

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить DevOps задачу."""
        context = context or {}

        if self.ai_service.client:
            return self._execute_with_ai(task, context)
        else:
            return self._execute_with_templates(task, context)

    def _execute_with_ai(self, task: str, context: Dict) -> Dict[str, Any]:
        """Выполнить задачу с помощью AI."""
        result = self.ai_service.generate_code(
            task=task,
            agent_type="devops",
            context=context,
            language="yaml"
        )

        if result['status'] == 'success':
            files = self.ai_service.parse_code_blocks(result['code'])

            return {
                'status': 'success',
                'type': 'ai_generated',
                'message': f'AI создал DevOps конфигурацию: {task}',
                'files': files,
                'tokens_used': result.get('tokens_used', 0),
                'model': result.get('model', 'unknown')
            }
        else:
            return self._execute_with_templates(task, context)

    def _execute_with_templates(self, task: str, context: Dict) -> Dict[str, Any]:
        """Выполнить задачу с помощью шаблонов."""
        if "docker" in task.lower():
            return self._create_docker(task, context)
        elif "ci" in task.lower() or "cd" in task.lower() or "github actions" in task.lower():
            return self._create_cicd(task, context)
        else:
            return self._create_deployment(task, context)

    def _create_docker(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать Docker конфигурацию."""
        return {
            'status': 'success',
            'type': 'docker',
            'message': f'Создаю Docker конфигурацию: {task}',
            'files': {
                'Dockerfile': self._generate_dockerfile(task),
                'docker-compose.yml': self._generate_docker_compose(task)
            }
        }

    def _create_cicd(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать CI/CD конфигурацию."""
        return {
            'status': 'success',
            'type': 'cicd',
            'message': f'Создаю CI/CD конфигурацию: {task}',
            'files': {
                '.github/workflows/ci.yml': self._generate_github_actions(task)
            }
        }

    def _create_deployment(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать скрипт развёртывания."""
        return {
            'status': 'success',
            'type': 'deployment',
            'message': f'Создаю скрипт развёртывания: {task}',
            'files': {
                'deploy.sh': self._generate_deploy_script(task)
            }
        }

    def _generate_dockerfile(self, task: str) -> str:
        """Генерация Dockerfile."""
        return f"""# Dockerfile для: {task}
# Создано JARVIS DevOps Agent

FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Экспорт порта
EXPOSE 8000

# Команда запуска
CMD ["python", "main.py"]
"""

    def _generate_docker_compose(self, task: str) -> str:
        """Генерация docker-compose.yml."""
        return f"""# Docker Compose для: {task}
# Создано JARVIS DevOps Agent

version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=jarvis
      - POSTGRES_USER=jarvis
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
"""

    def _generate_github_actions(self, task: str) -> str:
        """Генерация GitHub Actions workflow."""
        return f"""# GitHub Actions CI/CD для: {task}
# Создано JARVIS DevOps Agent

name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest

    - name: Lint
      run: |
        flake8 .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Добавьте команды развёртывания
"""

    def _generate_deploy_script(self, task: str) -> str:
        """Генерация скрипта развёртывания."""
        return f"""#!/bin/bash
# Скрипт развёртывания для: {task}
# Создано JARVIS DevOps Agent

set -e

echo "🚀 Начало развёртывания: {task}"

# Обновление кода
echo "📥 Обновление кода..."
git pull origin main

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip install -r requirements.txt

# Перезапуск сервиса
echo "🔄 Перезапуск сервиса..."
systemctl restart jarvis

echo "✅ Развёртывание завершено!"
"""
