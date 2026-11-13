"""
JARVIS - Data Analyst Agent
Агент для анализа данных и работы с базами данных
"""

from .base_agent import BaseAgent
from typing import Dict, Optional, Any


class DataAnalystAgent(BaseAgent):
    """Агент для анализа данных."""

    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description="Анализ данных, статистика, визуализация, работа с БД"
        )
        self.capabilities = [
            "Анализ CSV/Excel файлов",
            "Статистический анализ",
            "Создание графиков и визуализаций",
            "Работа с базами данных",
            "Обработка данных (pandas)",
            "Машинное обучение (базовое)",
            "Очистка и подготовка данных"
        ]

    def can_handle(self, task: str) -> bool:
        """Проверить, может ли агент обработать задачу."""
        keywords = [
            "данные", "анализ", "статистика", "график", "визуализация",
            "csv", "excel", "pandas", "numpy", "база данных", "sql",
            "обработка данных", "отчёт", "отчет"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in keywords)

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить задачу по анализу данных."""
        context = context or {}

        if "график" in task.lower() or "визуализация" in task.lower():
            return self._create_visualization(task, context)
        elif "отчёт" in task.lower() or "отчет" in task.lower():
            return self._create_report(task, context)
        else:
            return self._analyze_data(task, context)

    def _create_visualization(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать визуализацию данных."""
        return {
            'status': 'success',
            'type': 'visualization',
            'message': f'Создаю визуализацию: {task}',
            'files': {
                'visualization.py': self._generate_visualization_code(task)
            }
        }

    def _create_report(self, task: str, context: Dict) -> Dict[str, Any]:
        """Создать отчёт."""
        return {
            'status': 'success',
            'type': 'report',
            'message': f'Создаю отчёт: {task}',
            'files': {
                'report.py': self._generate_report_code(task)
            }
        }

    def _analyze_data(self, task: str, context: Dict) -> Dict[str, Any]:
        """Анализировать данные."""
        return {
            'status': 'success',
            'type': 'analysis',
            'message': f'Анализирую данные: {task}',
            'files': {
                'analysis.py': self._generate_analysis_code(task)
            }
        }

    def _generate_visualization_code(self, task: str) -> str:
        """Генерация кода для визуализации."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
Создано JARVIS Data Analyst Agent
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_visualization():
    """Создание визуализации данных."""
    # Пример данных
    data = {{
        'category': ['A', 'B', 'C', 'D'],
        'values': [10, 25, 15, 30]
    }}

    df = pd.DataFrame(data)

    # Создание графика
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='category', y='values')
    plt.title('{task}')
    plt.xlabel('Категория')
    plt.ylabel('Значение')
    plt.tight_layout()
    plt.savefig('chart.png', dpi=300)
    plt.show()

    print("Визуализация сохранена в chart.png")


if __name__ == "__main__":
    create_visualization()
"""

    def _generate_report_code(self, task: str) -> str:
        """Генерация кода для отчёта."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
Создано JARVIS Data Analyst Agent
"""

import pandas as pd
from datetime import datetime


def generate_report():
    """Генерация отчёта."""
    print(f"JARVIS Data Analyst Agent: Генерация отчёта")
    print(f"Задача: {task}")
    print(f"Дата: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")

    # Пример данных
    data = {{
        'metric': ['Продажи', 'Клиенты', 'Конверсия'],
        'value': [1000, 150, 15.5]
    }}

    df = pd.DataFrame(data)

    # Сохранение отчёта
    report_file = 'report.csv'
    df.to_csv(report_file, index=False, encoding='utf-8')

    print(f"\nОтчёт сохранён в {{report_file}}")
    print("\nДанные:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    generate_report()
"""

    def _generate_analysis_code(self, task: str) -> str:
        """Генерация кода для анализа."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
Создано JARVIS Data Analyst Agent
"""

import pandas as pd
import numpy as np


def analyze_data():
    """Анализ данных."""
    print("JARVIS Data Analyst Agent: Анализ данных")
    print(f"Задача: {task}")

    # Пример данных
    data = np.random.randn(100, 3)
    df = pd.DataFrame(data, columns=['A', 'B', 'C'])

    # Статистический анализ
    print("\n=== Статистика ===")
    print(df.describe())

    # Корреляция
    print("\n=== Корреляция ===")
    print(df.corr())

    # Сохранение результатов
    df.to_csv('analysis_results.csv', index=False)
    print("\nРезультаты сохранены в analysis_results.csv")


if __name__ == "__main__":
    analyze_data()
"""
