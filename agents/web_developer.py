"""
JARVIS - Web Developer Agent
Агент для создания сайтов и веб-приложений
"""

from .base_agent import BaseAgent
from typing import Dict, Optional, Any
import json


class WebDeveloperAgent(BaseAgent):
    """Агент для создания сайтов и веб-приложений."""

    def __init__(self):
        super().__init__(
            name="Web Developer",
            description="Создание сайтов, лендингов, веб-приложений"
        )
        self.capabilities = [
            "Создание HTML/CSS сайтов",
            "Генерация React компонентов",
            "Создание лендингов",
            "Генерация JavaScript кода",
            "Создание форм и валидация",
            "Адаптивный дизайн",
            "SEO оптимизация"
        ]

    def can_handle(self, task: str) -> bool:
        """Проверить, может ли агент обработать задачу."""
        keywords = [
            "сайт", "лендинг", "веб", "html", "css", "javascript",
            "react", "страница", "web", "frontend", "вёрстка", "верстка"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in keywords)

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить задачу по созданию сайта."""
        context = context or {}

        # Определяем тип задачи
        if "лендинг" in task.lower() or "landing" in task.lower():
            return self._create_landing(task, context)
        elif "react" in task.lower():
            return self._create_react_component(task, context)
        elif "форма" in task.lower() or "form" in task.lower():
            return self._create_form(task, context)
        else:
            return self._create_basic_site(task, context)

    def _create_landing(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать лендинг."""
        return {
            'status': 'success',
            'type': 'landing',
            'message': f'Создаю лендинг: {task}',
            'files': {
                'index.html': self._generate_html_template(task),
                'style.css': self._generate_css_template(),
                'script.js': self._generate_js_template()
            }
        }

    def _create_react_component(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать React компонент."""
        return {
            'status': 'success',
            'type': 'react_component',
            'message': f'Создаю React компонент: {task}',
            'files': {
                'Component.jsx': self._generate_react_template(task)
            }
        }

    def _create_form(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать форму."""
        return {
            'status': 'success',
            'type': 'form',
            'message': f'Создаю форму: {task}',
            'files': {
                'form.html': self._generate_form_template(task),
                'validation.js': self._generate_validation_template()
            }
        }

    def _create_basic_site(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать базовый сайт."""
        return {
            'status': 'success',
            'type': 'basic_site',
            'message': f'Создаю сайт: {task}',
            'files': {
                'index.html': self._generate_html_template(task),
                'style.css': self._generate_css_template()
            }
        }

    def _generate_html_template(self, task: str) -> str:
        """Генерация HTML шаблона."""
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{task}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{task}</h1>
    </header>
    <main>
        <p>Сайт создан JARVIS Web Developer Agent</p>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    def _generate_css_template(self) -> str:
        """Генерация CSS шаблона."""
        return """/* Стили созданы JARVIS Web Developer Agent */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    text-align: center;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}
"""

    def _generate_js_template(self) -> str:
        """Генерация JavaScript шаблона."""
        return """// JavaScript создан JARVIS Web Developer Agent
console.log('JARVIS Web Developer Agent: Сайт загружен');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM готов к работе');
});
"""

    def _generate_react_template(self, task: str) -> str:
        """Генерация React компонента."""
        component_name = ''.join(word.capitalize() for word in task.split()[:2])
        return f"""import React from 'react';

const {component_name} = () => {{
    return (
        <div className="{component_name.lower()}">
            <h2>{task}</h2>
            <p>Компонент создан JARVIS Web Developer Agent</p>
        </div>
    );
}};

export default {component_name};
"""

    def _generate_form_template(self, task: str) -> str:
        """Генерация формы."""
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{task}</title>
    <style>
        .form-container {{
            max-width: 500px;
            margin: 2rem auto;
            padding: 2rem;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        .form-group {{
            margin-bottom: 1rem;
        }}
        label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }}
        input, textarea {{
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        button {{
            background: #667eea;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        button:hover {{
            background: #764ba2;
        }}
    </style>
</head>
<body>
    <div class="form-container">
        <h2>{task}</h2>
        <form id="mainForm">
            <div class="form-group">
                <label for="name">Имя:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <button type="submit">Отправить</button>
        </form>
    </div>
    <script src="validation.js"></script>
</body>
</html>"""

    def _generate_validation_template(self) -> str:
        """Генерация валидации формы."""
        return """// Валидация формы создана JARVIS Web Developer Agent
document.getElementById('mainForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    if (!name || !email) {
        alert('Пожалуйста, заполните все поля');
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Пожалуйста, введите корректный email');
        return;
    }

    alert('Форма успешно отправлена!');
    console.log('Данные формы:', { name, email });
});
"""
