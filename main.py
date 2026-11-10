"""
JARVIS Ultimate — главный файл приложения
Точка входа для сборки в exe
"""

import sys
import os
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """Путь к ресурсам (для PyInstaller bundle)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def setup_environment():
    """Настройка окружения."""
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent

    os.chdir(app_dir)

    (app_dir / "logs").mkdir(exist_ok=True)
    (app_dir / "macros").mkdir(exist_ok=True)
    (app_dir / "plugins").mkdir(exist_ok=True)
    (app_dir / "data").mkdir(exist_ok=True)
    (app_dir / "models").mkdir(exist_ok=True)
    (app_dir / "assets" / "sounds").mkdir(parents=True, exist_ok=True)


def main():
    """Главная функция."""
    setup_environment()

    try:
        from core.config import Config
        from core.brain import JarvisBrain
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    print("=" * 50)
    print("  JARVIS Ultimate v2.0")
    print("  Инициализация системы...")
    print("=" * 50)

    try:
        config = Config("config.json")

        if config.openai_api_key:
            print("  ✓ OpenAI API подключен")
        else:
            print("  ✗ OpenAI API не настроен (опционально)")

        if config.home_assistant_url:
            print("  ✓ Home Assistant подключен")
        else:
            print("  ✗ Home Assistant не настроен (опционально)")

        brain = JarvisBrain(config)
        brain.start()
    except KeyboardInterrupt:
        print("\nОстановка по запросу пользователя...")
        if "brain" in locals():
            brain.stop()
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    main()
