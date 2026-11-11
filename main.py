"""
JARVIS Ultimate - Точка входа
"""

import sys
import time

# Явные импорты для PyInstaller (чтобы все модули попали в EXE)
import dotenv
import openai
import requests
import aiohttp
import websockets
import psutil
import pyautogui
import schedule
import pystray
import PIL
import plyer
import speedtest
import cpuinfo
import sklearn
import joblib
import numpy

from core.brain import JarvisBrain


def main():
    """Главная функция."""
    print("=" * 50)
    print("  JARVIS Ultimate v2.0.0")
    print("  AI Assistant with Learning Capabilities")
    print("=" * 50)
    print()

    # Инициализация
    brain = JarvisBrain()

    try:
        # Инициализация всех модулей
        brain.initialize()

        # Запуск
        brain.start()

        # Главный цикл
        print("\nJARVIS готов к работе. Введите команду или 'выход' для завершения.\n")

        while brain.running:
            try:
                # Ввод команды
                command = input("Вы: ").strip()

                if not command:
                    continue

                # Выход
                if command.lower() in ["выход", "exit", "quit", "стоп"]:
                    print("Завершение работы...")
                    break

                # Обработка команды
                result = brain.process_command(command)

                # Вывод результата
                if result.get("status") == "ok":
                    if "message" in result:
                        print(f"JARVIS: {result['message']}")
                    elif "response" in result:
                        print(f"JARVIS: {result['response']}")
                    else:
                        print(f"JARVIS: Команда выполнена")
                else:
                    print(f"JARVIS: Ошибка - {result.get('message', 'Неизвестная ошибка')}")

                # Информация об обучении
                if "learning_info" in result:
                    learning = result["learning_info"]
                    if learning.get("learning_suggestion"):
                        print(f"\n💡 {learning['learning_suggestion']}\n")

                print()

            except KeyboardInterrupt:
                print("\n\nПрервано пользователем")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

    finally:
        # Остановка
        brain.stop()
        print("\nДо свидания!")


if __name__ == "__main__":
    main()
