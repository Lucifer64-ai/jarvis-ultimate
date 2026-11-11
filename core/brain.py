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
        
        # HUD интерфейс
        self.hud = None
        
        # Информационные модули
        self.weather_module = None
        self.currency_module = None
        self.news_module = None
        
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
        
        # Инициализация HUD
        self._init_hud()
        
        # Инициализация информационных модулей
        self._init_info_modules()
        
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

    def _init_hud(self):
        """Инициализация HUD интерфейса."""
        try:
            from hud.holographic_ui import HolographicHUD
            self.hud = HolographicHUD(self)
            self.logger.info("✓ HUD интерфейс загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки HUD: {e}")
            self.hud = None

    def _init_info_modules(self):
        """Инициализация информационных модулей."""
        # Погода
        try:
            from modules.weather import WeatherModule
            self.weather_module = WeatherModule(self)
            self.logger.info("✓ Модуль погоды загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля погоды: {e}")
            self.weather_module = None
        
        # Валюты
        try:
            from modules.currency import CurrencyModule
            self.currency_module = CurrencyModule(self)
            self.logger.info("✓ Модуль валют загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля валют: {e}")
            self.currency_module = None
        
        # Новости
        try:
            from modules.news import NewsModule
            self.news_module = NewsModule(self)
            self.logger.info("✓ Модуль новостей загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модуля новостей: {e}")
            self.news_module = None


    def _init_avatar_3d(self):
        """Инициализация 3D голографического аватара."""
        try:
            from modules.avatar_3d import AvatarManager
            self.avatar_3d = AvatarManager(self)
            self.avatar_3d.initialize()
            self.logger.info("✓ 3D аватар загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки 3D аватара: {e}")
            self.avatar_3d = None

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
        
        # Обновление HUD статуса
        if self.hud:
            self.hud.set_status("PROCESSING")
            self.hud.set_voice_active(True)
        
        # Обработка через модули обучения
        if self.learning_manager:
            learning_result = self.learning_manager.process_command(text)
            processed_text = learning_result.get("processed", text)
            
            if learning_result.get("learning_suggestion"):
                self.logger.info(f"Предложение обучения: {learning_result['learning_suggestion']}")
        else:
            processed_text = text
            learning_result = {"original": text, "processed": text}
        
        # Выполнение команды
        result = self._execute_command(processed_text)
        
        # Объединение результатов
        result["learning_info"] = learning_result
        
        # Обновление HUD
        if self.hud:
            self.hud.set_status("READY")
            self.hud.set_voice_active(False)
        
        return result

    def _execute_command(self, text: str) -> Dict:
        """Выполнение команды."""
        text_lower = text.lower().strip()
        
        # === ПОГОДА ===
        if any(word in text_lower for word in ["погода", "температура", "прогноз"]):
            return self._handle_weather_command(text_lower)
        
        # === ВАЛЮТЫ ===
        elif any(word in text_lower for word in ["курс", "валют", "доллар", "евро", "рубл", "биткоин", "bitcoin"]):
            return self._handle_currency_command(text_lower)
        
        # === НОВОСТИ ===
        elif any(word in text_lower for word in ["новост", "что случилось", "что произошло", "headline"]):
            return self._handle_news_command(text_lower)
        
        # === HUD команды ===
        elif "покажи hud" in text_lower or "включи интерфейс" in text_lower:
            if self.hud:
                self.hud.show()
                return {"status": "ok", "message": "HUD активирован"}
        
        elif "скрой hud" in text_lower or "выключи интерфейс" in text_lower:
            if self.hud:
                self.hud.hide()
                return {"status": "ok", "message": "HUD деактивирован"}
        
        # === Clean Desktop ===
        elif "чистый рабочий стол" in text_lower or "скрой иконки" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.enable_clean_mode()
        
        elif "покажи иконки" in text_lower or "обычный рабочий стол" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.disable_clean_mode()
        
        # === Запуск приложений ===
        elif "открой" in text_lower or "запусти" in text_lower:
            if self.app_launcher:
                app_name = text_lower.replace("открой", "").replace("запусти", "").strip()
                return self.app_launcher.launch(app_name)
        
        elif "список приложений" in text_lower:
            if self.app_launcher:
                return self.app_launcher.list_apps()
        
        # === Системные команды ===
        elif any(word in text_lower for word in ["выключи", "заверши работу"]):
            if "system" in self.modules:
                return self.modules["system"].shutdown()
        
        elif any(word in text_lower for word in ["перезагрузи", "рестарт"]):
            if "system" in self.modules:
                return self.modules["system"].restart()
        
        elif any(word in text_lower for word in ["заблокируй", "лок"]):
            if "system" in self.modules:
                return self.modules["system"].lock_screen()
        
        # === Информация ===
        elif "час" in text_lower or "время" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_time()
        
        elif "дата" in text_lower or "число" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_date()
        
        # === Статус системы ===
        elif "статус" in text_lower or "состояние" in text_lower:
            if "hardware" in self.modules:
                return self.modules["hardware"].get_system_info()
        
        # === Сеть ===
        elif "ip" in text_lower or "айпи" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].get_ip()
        
        elif "скорость" in text_lower and "интернет" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].speed_test()
        
        # === Windows интеграция ===
        elif "автозапуск" in text_lower:
            if self.windows_integration:
                if "включи" in text_lower:
                    return self.windows_integration.enable_autostart()
                elif "выключи" in text_lower:
                    return self.windows_integration.disable_autostart()
        
        # === Обучение ===
        elif "научись" in text_lower or "запомни" in text_lower:
            return self._handle_learning_command(text)
        
        elif "алиас" in text_lower or "псевдоним" in text_lower:
            return self._handle_alias_command(text)
        
        elif "статус обучения" in text_lower or "чему ты научился" in text_lower:
            return self._get_learning_status()
        

        # === 3D Аватар ===
        elif any(word in text_lower for word in ["покажи аватар", "включи аватар", "аватар покажись"]):
            if self.avatar_3d:
                result = self.avatar_3d.show()
                return {"status": result["status"], "message": result["message"]}

        elif any(word in text_lower for word in ["скрой аватар", "выключи аватар", "аватар исчезни"]):
            if self.avatar_3d:
                result = self.avatar_3d.hide()
                return {"status": result["status"], "message": result["message"]}

        elif "перемести аватар" in text_lower:
            if self.avatar_3d:
                # Парсинг координат (упрощённо)
                return {"status": "ok", "message": "Используйте GUI для перемещения аватара"}

        return {
            "status": "ok",
            "message": "Команда не распознана",
            "text": text
        }

    def _handle_weather_command(self, text: str) -> Dict:
        """Обработка команд погоды."""
        if not self.weather_module:
            return {"status": "error", "message": "Модуль погоды не загружен"}
        
        # Извлечение города
        city = "Москва"  # По умолчанию
        cities = ["москва", "санкт-петербург", "питер", "новосибирск", "екатеринбург", 
                  "казань", "нижний новгород", "самара", "омск", "челябинск", "уфа", "ростов"]
        
        for c in cities:
            if c in text:
                city = c.capitalize()
                if city == "Питер":
                    city = "Санкт-Петербург"
                break
        
        # Прогноз или текущая погода
        if "прогноз" in text:
            forecast = self.weather_module.get_forecast(city)
            message = self.weather_module.format_forecast_message(forecast)
            return {"status": "ok", "message": message, "data": forecast}
        else:
            weather = self.weather_module.get_weather(city)
            message = self.weather_module.format_weather_message(weather)
            return {"status": "ok", "message": message, "data": weather}

    def _handle_currency_command(self, text: str) -> Dict:
        """Обработка команд валют."""
        if not self.currency_module:
            return {"status": "error", "message": "Модуль валют не загружен"}
        
        # Конвертация
        if "конверт" in text or "переведи" in text or "сколько" in text:
            # Простая конвертация
            if "доллар" in text or "usd" in text:
                rate = self.currency_module.get_usd_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"Один доллар стоит {rate['rate']} рублей"}
            elif "евро" in text or "eur" in text:
                rate = self.currency_module.get_eur_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"Одно евро стоит {rate['rate']} рублей"}
            elif "биткоин" in text or "bitcoin" in text or "btc" in text:
                rate = self.currency_module.get_btc_usd()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"Один биткоин стоит ${rate['rate']}"}
        
        # Все курсы
        rates = self.currency_module.get_multiple_rates()
        message = self.currency_module.format_multiple_rates_message(rates)
        return {"status": "ok", "message": message, "data": rates}

    def _handle_news_command(self, text: str) -> Dict:
        """Обработка команд новостей."""
        if not self.news_module:
            return {"status": "error", "message": "Модуль новостей не загружен"}
        
        # Поиск новостей
        if "найди" in text or "поиск" in text or "про" in text:
            # Извлечение запроса
            query = text.replace("найди новости про", "").replace("новости про", "").replace("найди", "").strip()
            if query:
                news = self.news_module.search_news(query)
                message = self.news_module.format_news_message(news)
                return {"status": "ok", "message": message, "data": news}
        
        # Категории
        if "технолог" in text or "tech" in text:
            news = self.news_module.get_tech_news()
        elif "бизнес" in text or "финанс" in text or "эконом" in text:
            news = self.news_module.get_business_news()
        elif "спорт" in text:
            news = self.news_module.get_sports_news()
        else:
            news = self.news_module.get_top_headlines()
        
        message = self.news_module.format_news_message(news)
        return {"status": "ok", "message": message, "data": news}

    def _handle_learning_command(self, text: str) -> Dict:
        """Обработка команд обучения."""
        if not self.learning_manager or not self.learning_manager.adaptive_ml:
            return {"status": "error", "message": "Модуль обучения не загружен"}
        
        return {
            "status": "ok",
            "message": "Команда обучения принята"
        }

    def _handle_alias_command(self, text: str) -> Dict:
        """Обработка команд алиасов."""
        if not self.learning_manager or not self.learning_manager.alias_system:
            return {"status": "error", "message": "Система алиасов не загружена"}
        
        return {
            "status": "ok",
            "message": "Команда алиаса принята"
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
        else:
            greeting = "Здравствуйте, сэр. JARVIS готов к работе."
            self.logger.info(greeting)
        
        # Обновление HUD
        if self.hud:
            self.hud.set_status("ONLINE")
        
        # Автозапуск wake word сервиса если включен
        if self.wake_word_service and self.config.get("windows.wake_word_enabled", False):
            self.wake_word_service.start(callback=self._on_wake_word)
        
        # Включение чистого режима если настроено
        if self.clean_desktop and self.config.get("windows.clean_desktop_on_start", False):
            self.clean_desktop.enable_clean_mode()
        
        # Публикация события запуска
        self.event_bus.publish("jarvis_started", {"timestamp": "now"})

    def _on_wake_word(self, text: str):
        """Обработчик wake word."""
        self.logger.info(f"Wake word активирован: {text}")
        
        if self.hud:
            self.hud.set_status("LISTENING")
            self.hud.set_voice_active(True)

    def stop(self):
        """Остановка JARVIS."""
        self.logger.info("Остановка JARVIS...")
        self.running = False
        
        if self.wake_word_service and self.wake_word_service.is_running():
            self.wake_word_service.stop()
        
        if self.clean_desktop and self.clean_desktop.is_hidden():
            self.clean_desktop.disable_clean_mode()
        
        self.event_bus.publish("jarvis_stopped", {"timestamp": "now"})

    def get_status(self) -> Dict:
        """Получение статуса системы."""
        return {
            "running": self.running,
            "modules_loaded": len(self.modules),
            "plugins_loaded": len(self.plugin_manager.plugins),
            "learning_enabled": self.learning_manager is not None,
            "hud_enabled": self.hud is not None,
            "info_modules": {
                "weather": self.weather_module is not None,
                "currency": self.currency_module is not None,
                "news": self.news_module is not None
            },
            "windows_integration": {
                "enabled": self.windows_integration is not None,
                "toast_enabled": self.toast_notifications is not None,
                "wake_word_enabled": self.wake_word_service is not None and self.wake_word_service.is_running(),
                "clean_desktop": self.clean_desktop is not None and self.clean_desktop.is_hidden(),
                "apps_count": self.app_launcher.get_apps_count() if self.app_launcher else 0
            }
        }
