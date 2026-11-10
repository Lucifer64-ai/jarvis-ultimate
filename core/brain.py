"""
JARVIS Brain - Главный контроллер системы
"""

import logging
from typing import Dict, Optional, Any
from core.config import Config
from core.event_bus import EventBus
from core.plugin_manager import PluginManager


class JarvisBrain:
    """Центральный контроллер JARVIS."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("Инициализация JARVIS Brain...")
        
        # Конфигурация
        self.config = Config()
        
        # Шина событий
        self.event_bus = EventBus()
        
        # Менеджер плагинов
        self.plugin_manager = PluginManager(self)
        
        # Модули обучения
        self.learning_manager = None
        
        # Windows интеграция
        self.windows_integration = None
        self.toast_notifications = None
        self.wake_word_service = None
        self.clean_desktop = None
        self.app_launcher = None
        self.hud = None
        
        # Системные модули
        self.modules = {}
        
        # Состояние
        self.running = False
        
        self.logger.info("JARVIS Brain инициализирован")

    def _setup_logging(self) -> logging.Logger:
        """Настройка логирования."""
        logger = logging.getLogger("JARVIS")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def initialize(self):
        """Инициализация всех модулей."""
        self.logger.info("Запуск инициализации модулей...")
        
        # Инициализация модулей обучения
        self._init_learning_modules()
        
        # Инициализация Windows интеграции
        self._init_windows_integration()
        
        # Инициализация системных модулей
        self._init_system_modules()
        
        # Загрузка плагинов
        self.plugin_manager.load_plugins()
        
        self.logger.info("Все модули инициализированы")

    def _init_learning_modules(self):
        """Инициализация модулей обучения."""
        try:
            from ai.learning_manager import LearningManager
            self.learning_manager = LearningManager(self)
            self.logger.info("✓ Модули обучения загружены")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модулей обучения: {e}")
            self.learning_manager = None

    def _init_windows_integration(self):
        """Инициализация Windows интеграции."""
        # Windows интеграция
        try:
            from modules.windows_integration import WindowsIntegration
            self.windows_integration = WindowsIntegration(self)
            self.logger.info("✓ Windows интеграция загружена")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки Windows интеграции: {e}")
            self.windows_integration = None
        
        # Toast уведомления
        try:
            from modules.toast_notifications import ToastNotifications
            self.toast_notifications = ToastNotifications(self)
            self.logger.info("✓ Toast уведомления загружены")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки toast уведомлений: {e}")
            self.toast_notifications = None
        
        # Wake word сервис
        try:
            from modules.wake_word_service import WakeWordService
            self.wake_word_service = WakeWordService(self)
            self.logger.info("✓ Wake word сервис загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки wake word сервиса: {e}")
            self.wake_word_service = None
        
        # Clean Desktop
        try:
            from modules.clean_desktop import CleanDesktop
            self.clean_desktop = CleanDesktop(self)
            self.logger.info("✓ Clean Desktop загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки Clean Desktop: {e}")
            self.clean_desktop = None
        
        # App Launcher
        try:
            from modules.app_launcher import AppLauncher
            self.app_launcher = AppLauncher(self)
            self.logger.info("✓ App Launcher загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки App Launcher: {e}")
            self.app_launcher = None
        
        # HUD
        try:
            from modules.hud import JarvisHUD
            self.hud = JarvisHUD(self)
            self.logger.info("✓ JARVIS HUD загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки HUD: {e}")
            self.hud = None

    def _init_system_modules(self):
        """Инициализация системных модулей."""
        # Системные операции
        try:
            from modules.system import SystemModule
            self.modules["system"] = SystemModule(self)
            self.logger.info("✓ Системный модуль загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки системного модуля: {e}")
        
        # Управление процессами
        try:
            from modules.processes import ProcessModule
            self.modules["processes"] = ProcessModule(self)
            self.logger.info("✓ Модуль процессов загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля процессов: {e}")
        
        # Работа с файлами
        try:
            from modules.files import FileModule
            self.modules["files"] = FileModule(self)
            self.logger.info("✓ Модуль файлов загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля файлов: {e}")
        
        # Управление окнами
        try:
            from modules.windows import WindowModule
            self.modules["windows"] = WindowModule(self)
            self.logger.info("✓ Модуль окон загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля окон: {e}")
        
        # Сетевые операции
        try:
            from modules.network import NetworkModule
            self.modules["network"] = NetworkModule(self)
            self.logger.info("✓ Сетевой модуль загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки сетевого модуля: {e}")
        
        # Мониторинг оборудования
        try:
            from modules.hardware import HardwareModule
            self.modules["hardware"] = HardwareModule(self)
            self.logger.info("✓ Модуль оборудования загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля оборудования: {e}")
        
        # Управление питанием
        try:
            from modules.power import PowerModule
            self.modules["power"] = PowerModule(self)
            self.logger.info("✓ Модуль питания загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля питания: {e}")

    def process_command(self, text: str) -> Dict:
        """Обработка команды с использованием модулей обучения."""
        self.logger.info(f"Обработка команды: {text}")
        
        # Обновление HUD
        if self.hud:
            self.hud.update_command(text)
        
        # Обработка через модули обучения
        if self.learning_manager:
            learning_result = self.learning_manager.process_command(text)
            processed_text = learning_result.get("processed", text)
            
            # Если есть предложение обучения
            if learning_result.get("learning_suggestion"):
                self.logger.info(f"Предложение обучения: {learning_result['learning_suggestion']}")
        else:
            processed_text = text
            learning_result = {"original": text, "processed": text}
        
        # Выполнение команды
        result = self._execute_command(processed_text)
        
        # Объединение результатов
        result["learning_info"] = learning_result
        
        return result

    def _execute_command(self, text: str) -> Dict:
        """Выполнение команды."""
        text_lower = text.lower().strip()
        
        # HUD команды
        if "покажи hud" in text_lower or "включи hud" in text_lower:
            if self.hud:
                self.hud.show_hud()
                return {"status": "ok", "message": "HUD включен"}
        
        elif "скрой hud" in text_lower or "выключи hud" in text_lower:
            if self.hud:
                self.hud.hide_hud()
                return {"status": "ok", "message": "HUD выключен"}
        
        elif "переключи hud" in text_lower:
            if self.hud:
                self.hud.toggle_hud()
                return {"status": "ok", "message": "HUD переключен"}
        
        # Clean Desktop режим
        if "чистый рабочий стол" in text_lower or "скрой иконки" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.enable_clean_mode()
        
        elif "покажи иконки" in text_lower or "обычный рабочий стол" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.disable_clean_mode()
        
        elif "скрой панель задач" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.hide_taskbar()
        
        elif "покажи панель задач" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.show_taskbar()
        
        # Запуск приложений
        elif "открой" in text_lower or "запусти" in text_lower:
            if self.app_launcher:
                # Извлекаем имя приложения
                app_name = text_lower.replace("открой", "").replace("запусти", "").strip()
                return self.app_launcher.launch(app_name)
        
        elif "добавь приложение" in text_lower:
            if self.app_launcher:
                return {"status": "ok", "message": "Используйте: добавь приложение [имя] для [путь]"}
        
        elif "список приложений" in text_lower:
            if self.app_launcher:
                return self.app_launcher.list_apps()
        
        # Системные команды
        elif any(word in text_lower for word in ["выключи", "заверши работу"]):
            if "system" in self.modules:
                return self.modules["system"].shutdown()
        
        elif any(word in text_lower for word in ["перезагрузи", "рестарт"]):
            if "system" in self.modules:
                return self.modules["system"].restart()
        
        elif any(word in text_lower for word in ["заблокируй", "лок"]):
            if "system" in self.modules:
                return self.modules["system"].lock_screen()
        
        # Информация
        elif "час" in text_lower or "время" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_time()
        
        elif "дата" in text_lower or "число" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_date()
        
        # Статус системы
        elif "статус" in text_lower or "состояние" in text_lower:
            if "hardware" in self.modules:
                return self.modules["hardware"].get_system_info()
        
        # Сеть
        elif "ip" in text_lower or "айпи" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].get_ip()
        
        elif "скорость" in text_lower and "интернет" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].speed_test()
        
        # Windows интеграция
        elif "автозапуск" in text_lower:
            if self.windows_integration:
                if "включи" in text_lower:
                    return self.windows_integration.enable_autostart()
                elif "выключи" in text_lower:
                    return self.windows_integration.disable_autostart()
                elif "статус" in text_lower:
                    status = self.windows_integration.get_integration_status()
                    return {"status": "ok", "message": f"Автозапуск: {'включен' if status['autostart_enabled'] else 'отключен'}"}
        
        elif "wake word" in text_lower or "пробуждение" in text_lower:
            if self.wake_word_service:
                if "включи" in text_lower or "запусти" in text_lower:
                    return self.wake_word_service.start()
                elif "выключи" in text_lower or "останови" in text_lower:
                    return self.wake_word_service.stop()
        
        # Обучение - новые команды
        elif "научись" in text_lower or "запомни" in text_lower:
            return self._handle_learning_command(text)
        
        # Алиасы
        elif "алиас" in text_lower or "псевдоним" in text_lower:
            return self._handle_alias_command(text)
        
        # Статус обучения
        elif "статус обучения" in text_lower or "чему ты научился" in text_lower:
            return self._get_learning_status()
        
        return {
            "status": "ok",
            "message": "Команда не распознана",
            "text": text
        }

    def _handle_learning_command(self, text: str) -> Dict:
        """Обработка команд обучения."""
        if not self.learning_manager or not self.learning_manager.adaptive_ml:
            return {"status": "error", "message": "Модуль обучения не загружен"}
        
        return {
            "status": "ok",
            "message": "Команда обучения принята. Используйте: научись [команда] это [категория]"
        }

    def _handle_alias_command(self, text: str) -> Dict:
        """Обработка команд алиасов."""
        if not self.learning_manager or not self.learning_manager.alias_system:
            return {"status": "error", "message": "Система алиасов не загружена"}
        
        return {
            "status": "ok",
            "message": "Команда алиаса принята. Используйте: создай алиас [алиас] для [команда]"
        }

    def _get_learning_status(self) -> Dict:
        """Получение статуса обучения."""
        if not self.learning_manager:
            return {"status": "error", "message": "Модули обучения не загружены"}
        
        return self.learning_manager.get_learning_status()

    def start(self):
        """Запуск JARVIS."""
        self.logger.info("Запуск JARVIS...")
        self.running = True
        
        # Приветствие
        if self.learning_manager:
            greeting = self.learning_manager.get_greeting()
            self.logger.info(greeting)
            
            # Toast уведомление
            if self.toast_notifications:
                self.toast_notifications.show_info(greeting)
        else:
            self.logger.info("Здравствуйте, сэр. JARVIS готов к работе.")
        
        # Автозапуск wake word сервиса если включен
        if self.wake_word_service and self.config.get("windows.wake_word_enabled", False):
            self.wake_word_service.start(callback=self._on_wake_word)
        
        # Включение чистого режима если настроено
        if self.clean_desktop and self.config.get("windows.clean_desktop_on_start", False):
            self.clean_desktop.enable_clean_mode()
        
        # Показ HUD если настроено
        if self.hud and self.config.get("windows.hud_on_start", False):
            self.hud.show_hud()
        
        # Публикация события запуска
        self.event_bus.publish("jarvis_started", {"timestamp": "now"})

    def _on_wake_word(self, text: str):
        """Обработчик wake word."""
        self.logger.info(f"Wake word активирован: {text}")
        
        # Уведомление
        if self.toast_notifications:
            self.toast_notifications.show_info("Слушаю...")
        
        # Анимация HUD
        if self.hud:
            self.hud.set_voice_level(0.8)

    def stop(self):
        """Остановка JARVIS."""
        self.logger.info("Остановка JARVIS...")
        self.running = False
        
        # Остановка wake word сервиса
        if self.wake_word_service and self.wake_word_service.is_running():
            self.wake_word_service.stop()
        
        # Восстановление рабочего стола если был чистый режим
        if self.clean_desktop and self.clean_desktop.is_hidden():
            self.clean_desktop.disable_clean_mode()
        
        self.event_bus.publish("jarvis_stopped", {"timestamp": "now"})

    def get_status(self) -> Dict:
        """Получение статуса системы."""
        status = {
            "running": self.running,
            "modules_loaded": len(self.modules),
            "plugins_loaded": len(self.plugin_manager.plugins),
            "learning_enabled": self.learning_manager is not None,
            "windows_integration": {
                "enabled": self.windows_integration is not None,
                "toast_enabled": self.toast_notifications is not None,
                "wake_word_enabled": self.wake_word_service is not None and self.wake_word_service.is_running(),
                "clean_desktop": self.clean_desktop is not None and self.clean_desktop.is_hidden(),
                "apps_count": self.app_launcher.get_apps_count() if self.app_launcher else 0,
                "hud_enabled": self.hud is not None
            }
        }
        
        if self.windows_integration:
            status["windows_integration"]["autostart"] = self.windows_integration.is_autostart_enabled()
        
        return status
