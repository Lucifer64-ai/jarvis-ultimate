#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS - Тестирование системы агентов
"""

import sys
import os
import json
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

from agents.agent_manager import AgentManager
from agents.file_saver import get_file_saver


def test_agent_manager():
    """Тестирование AgentManager."""
    print("=" * 60)
    print("ТЕСТ 1: Инициализация AgentManager")
    print("=" * 60)

    manager = AgentManager()

    # Проверяем регистрацию агентов
    agents = manager.list_agents()
    print(f"\n✅ Зарегистрировано агентов: {len(agents)}")

    for agent in agents:
        print(f"  • {agent['name']}: {agent['description']}")
        print(f"    Возможностей: {len(agent['capabilities'])}")

    return manager


def test_can_handle(manager):
    """Тестирование метода can_handle."""
    print("\n" + "=" * 60)
    print("ТЕСТ 2: Проверка распознавания задач")
    print("=" * 60)

    test_tasks = [
        ("Создай лендинг для кофейни", "Web Developer"),
        ("Напиши Python скрипт для парсинга", "Programmer"),
        ("Проанализируй данные из CSV", "Data Analyst"),
        ("Создай дизайн мобильного приложения", "Designer"),
        ("Создай Docker файл для проекта", "DevOps"),
    ]

    for task, expected_agent in test_tasks:
        agent = manager.find_suitable_agent(task)
        if agent:
            status = "✅" if agent.name == expected_agent else "⚠️"
            print(f"{status} '{task[:40]}...' → {agent.name}")
        else:
            print(f"❌ '{task[:40]}...' → Агент не найден")


def test_execute_tasks(manager):
    """Тестирование выполнения задач."""
    print("\n" + "=" * 60)
    print("ТЕСТ 3: Выполнение задач (без AI)")
    print("=" * 60)

    test_tasks = [
        "Создай лендинг для кофейни",
        "Напиши Python скрипт для парсинга",
        "Создай цветовую схему для сайта",
        "Создай Docker файл для проекта",
    ]

    for task in test_tasks:
        print(f"\n📋 Задача: {task}")
        result = manager.execute_task(task)

        if result.get('status') == 'success':
            print(f"  ✅ Статус: {result.get('type', 'unknown')}")
            print(f"  📁 Файлов создано: {len(result.get('files', {}))}")

            # Показываем имена файлов
            for filename in list(result.get('files', {}).keys())[:3]:
                print(f"     • {filename}")
        else:
            print(f"  ❌ Ошибка: {result.get('message', 'Неизвестная ошибка')}")


def test_file_saver():
    """Тестирование FileSaver."""
    print("\n" + "=" * 60)
    print("ТЕСТ 4: Сохранение файлов на диск")
    print("=" * 60)

    file_saver = get_file_saver()

    # Тестовые файлы
    test_files = {
        'test.html': '<!DOCTYPE html><html><body><h1>Test</h1></body></html>',
        'test.css': 'body { margin: 0; padding: 0; }',
        'test.js': 'console.log("Hello from JARVIS!");'
    }

    result = file_saver.save_files(
        files=test_files,
        project_name="Тестовый проект",
        agent_name="Test Agent"
    )

    if result.get('status') == 'success':
        print(f"✅ Проект создан: {result.get('project_dir')}")
        print(f"📁 Сохранено файлов: {result.get('files_saved')}")

        for file_info in result.get('files', []):
            print(f"  • {file_info['filename']} ({file_info['size']} байт)")
    else:
        print(f"❌ Ошибка: {result.get('message')}")


def test_voice_commands(manager):
    """Тестирование голосовых команд."""
    print("\n" + "=" * 60)
    print("ТЕСТ 5: Голосовые команды")
    print("=" * 60)

    commands = [
        "какие агенты",
        "история задач",
        "возможности агента Web Developer",
        "статус агента Programmer"
    ]

    for command in commands:
        print(f"\n🎤 Команда: '{command}'")

        # Имитируем обработку команды
        if "какие агенты" in command:
            agents = manager.list_agents()
            print(f"  ✅ Найдено агентов: {len(agents)}")
            for agent in agents[:3]:
                print(f"     • {agent['name']}")

        elif "история задач" in command:
            history = manager.get_task_history()
            print(f"  ✅ Задач в истории: {len(history)}")

        elif "возможности" in command:
            agent_name = "Web Developer"
            agent = manager.get_agent(agent_name)
            if agent:
                print(f"  ✅ Возможности {agent_name}:")
                for cap in agent.capabilities[:3]:
                    print(f"     • {cap}")

        elif "статус" in command:
            agent_name = "Programmer"
            agent = manager.get_agent(agent_name)
            if agent:
                status = agent.get_status()
                print(f"  ✅ Статус {agent_name}:")
                print(f"     • Задач выполнено: {status['tasks_completed']}")


def main():
    """Главная функция тестирования."""
    print("\n" + "🤖" * 30)
    print("JARVIS AGENT SYSTEM - ТЕСТИРОВАНИЕ")
    print("🤖" * 30 + "\n")

    try:
        # Тест 1: Инициализация
        manager = test_agent_manager()

        # Тест 2: Распознавание задач
        test_can_handle(manager)

        # Тест 3: Выполнение задач
        test_execute_tasks(manager)

        # Тест 4: Сохранение файлов
        test_file_saver()

        # Тест 5: Голосовые команды
        test_voice_commands(manager)

        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
