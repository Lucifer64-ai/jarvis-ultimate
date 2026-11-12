"""
JARVIS Brain - главный контроллер системы
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
        self.config = Config()
        self.event_bus = EventBus()
        self.plugin_manager = PluginManager(self)
        self.learning_manager = None
        self.windows_integration = None
        self.toast_notifications = None
        self.wake_word_service = None
        self.clean_desktop = None
        self.app_launcher = None
        self.hud = None
        self.weather_module = None
        self.currency_module = None
        self.news_module = None
        self.modules = {}
        self.running = False
        self.logger.info("JARVIS Brain инициализирован")

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("JARVIS")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
        return logger

    def initialize(self):
        self.logger.info("Запуск инициализации модулей...")
        self._init_learning_modules()
        self._init_windows_integration()
        self._init_hud()
        self._init_info_modules()
        self._init_system_modules()
        self.plugin_manager.load_plugins()
        self.logger.info("Все модули инициализированы")

    def _init_learning_modules(self):
        try:
            from ai.learning_manager import LearningManager
            self.learning_manager = LearningManager(self)
            self.logger.info("✓ Модули обучения загружены")
        except Exception as e:
            self.logger.error("Ошибка загрузки модулей обучения: %s", e)
            self.learning_manager = None

    def _init_windows_integration(self):
        try:
            from modules.windows_integration import WindowsIntegration
            self.windows_integration = WindowsIntegration(self)
            self.logger.info("✓ Windows интеграция загружена")
        except Exception as e:
            self.logger.error("Ошибка загрузки Windows интеграции: %s", e)
            self.windows_integration = None
        try:
            from modules.toast_notifications import ToastNotifications
            self.toast_notifications = ToastNotifications(self)
            self.logger.info("✓ Toast уведомления загружены")
        except Exception as e:
            self.logger.error("Ошибка загрузки toast уведомлений: %s", e)
            self.toast_notifications = None
        try:
            from modules.wake_word_service import WakeWordService
            self.wake_word_service = WakeWordService(self)
            self.logger.info("✓ Wake word сервис загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки wake word сервиса: %s", e)
            self.wake_word_service = None
        try:
            from modules.clean_desktop import CleanDesktop
            self.clean_desktop = CleanDesktop(self)
            self.logger.info("✓ Clean Desktop загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки Clean Desktop: %s", e)
            self.clean_desktop = None
        try:
            from modules.app_launcher import AppLauncher
            self.app_launcher = AppLauncher(self)
            self.logger.info("✓ App Launcher загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки App Launcher: %s", e)
            self.app_launcher = None

    def _init_voice(self):
        try:
            from voice.speaker import VoiceSpeaker
            self.voice_speaker = VoiceSpeaker(self)
            self.logger.info("✓ Голосовой модуль загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки голосового модуля: %s", e)
            self.voice_speaker = None

    def _init_hud(self):
        try:
            from hud.holographic_ui import HolographicHUD
            self.hud = HolographicHUD(self)
            self.logger.info("✓ HUD интерфейс загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки HUD: %s", e)
            self.hud = None

    def _init_info_modules(self):
        try:
            from modules.weather import WeatherModule
            self.weather_module = WeatherModule(self)
            self.logger.info("✓ Модуль погоды загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки модуля погоды: %s", e)
            self.weather_module = None
        try:
            from modules.currency import CurrencyModule
            self.currency_module = CurrencyModule(self)
            self.logger.info("✓ Модуль валют загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки модуля валют: %s", e)
            self.currency_module = None
        try:
            from modules.news import NewsModule
            self.news_module = NewsModule(self)
            self.logger.info("✓ Модуль новостей загружен")
        except Exception as e:
            self.logger.error("Ошибка загрузки модуля новостей: %s", e)
            self.news_module = None

    def reload_api_integrations(self):
        """Перечитать ключи и пересоздать интеграции, использующие API-ключи."""
        self.config.reload_secrets()
        self._init_info_modules()
        self.logger.info("API-настройки перечитаны; ключи OpenWeather и NewsAPI обновлены")

    def _init_system_modules(self):
        module_specs = [
            ("system", "modules.system", "SystemModule"),
            ("processes", "modules.processes", "ProcessModule"),
            ("files", "modules.files", "FileModule"),
            ("windows", "modules.windows", "WindowModule"),
            ("network", "modules.network", "NetworkModule"),
            ("hardware", "modules.hardware", "HardwareModule"),
            ("power", "modules.power", "PowerModule"),
            ("app_analyzer", "modules.app_analyzer", "AppAnalyzer"),
        ]
        for key, module_name, class_name in module_specs:
            try:
                module = __import__(module_name, fromlist=[class_name])
                self.modules[key] = getattr(module, class_name)(self)
                self.logger.info("✓ Модуль %s загружен", key)
            except Exception as e:
                self.logger.error("Ошибка загрузки модуля %s: %s", key, e)

    def process_command(self, text: str) -> Dict:
        self.logger.info("Обработка команды: %s", text)
        if self.hud:
            self.hud.set_status("PROCESSING")
            self.hud.set_voice_active(True)
        if self.learning_manager:
            learning_result = self.learning_manager.process_command(text)
            processed_text = learning_result.get("processed", text)
            if learning_result.get("learning_suggestion"):
                self.logger.info("Предложение обучения: %s", learning_result['learning_suggestion'])
        else:
            processed_text = text
            learning_result = {"original": text, "processed": text}
        result = self._execute_command(processed_text)
        result["learning_info"] = learning_result
        if self.hud:
            self.hud.set_status("READY")
            self.hud.set_voice_active(False)
        return result

    def _execute_command(self, text: str) -> Dict:
        """Выполнение команд приложения."""
        text_lower = text.lower().strip()
        if any(word in text_lower for word in ["погода", "температура", "прогноз"]):
            return self._handle_weather_command(text_lower)
        elif any(word in text_lower for word in ["курс", "валют", "доллар", "евро", "рубл", "биткоин", "btc", "usd", "eur"]):
            return self._handle_currency_command(text_lower)
        elif any(word in text_lower for word in ["новост", "что случилось", "что произошло", "headline"]):
            return self._handle_news_command(text_lower)
        elif "покажи hud" in text_lower or "включи интерфейс" in text_lower:
            if self.hud:
                self.hud.show()
                return {"status": "ok", "message": "HUD активирован"}
        elif "скрой hud" in text_lower or "выключи интерфейс" in text_lower:
            if self.hud:
                self.hud.hide()
                return {"status": "ok", "message": "HUD деактивирован"}
        elif "чистый рабочий стол" in text_lower or "скрой иконки" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.enable_clean_mode()
        elif "покажи иконки" in text_lower or "обычный рабочий стол" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.disable_clean_mode()
        elif "открой" in text_lower or "запусти" in text_lower:
            if self.app_launcher:
                app_name = text_lower.replace("открой", "").replace("запусти", "").strip()
                return self.app_launcher.launch(app_name)
        elif "список приложений" in text_lower:
            if self.app_launcher:
                return self.app_launcher.list_apps()
        elif any(word in text_lower for word in ["выключи", "заверши работу"]):
            if "system" in self.modules:
                return self.modules["system"].shutdown()
        elif any(word in text_lower for word in ["перезагрузи", "рестарт"]):
            if "system" in self.modules:
                return self.modules["system"].restart()
        elif any(word in text_lower for word in ["заблокируй", "лок"]):
            if "system" in self.modules:
                return self.modules["system"].lock_screen()
        elif "час" in text_lower or "время" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_time()
        elif "дата" in text_lower or "число" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_date()
        elif "статус" in text_lower or "состояние" in text_lower:
            if "hardware" in self.modules:
                return self.modules["hardware"].get_system_info()
        elif "ip" in text_lower or "айпи" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].get_ip()
        elif "скорость" in text_lower and "интернет" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].speed_test()
        elif "автозапуск" in text_lower and self.windows_integration:
            if "включи" in text_lower:
                return self.windows_integration.enable_autostart()
            if "выключи" in text_lower:
                return self.windows_integration.disable_autostart()
        elif "научись" in text_lower or "запомни" in text_lower:
            return self._handle_learning_command(text)
        elif "алиас" in text_lower or "псевдоним" in text_lower:
            return self._handle_alias_command(text)
        elif "статус обучения" in text_lower or "чему ты научился" in text_lower:
            return self._get_learning_status()
        return {"status": "ok", "message": "Команда не распознана", "text": text}

    def _handle_weather_command(self, text: str) -> Dict:
        if not self.weather_module:
            return {"status": "error", "message": "Модуль погоды не загружен"}
        city = "Москва"
        cities = ["москва", "санкт-петербург", "питер", "новосибирск", "екатеринбург", "казань", "нижний новгород", "самара", "омск", "челябинск"]
        for city_name in cities:
            if city_name in text:
                city = "Санкт-Петербург" if city_name == "питер" else city_name.capitalize()
                break
        if "прогноз" in text:
            data = self.weather_module.get_forecast(city)
            return {"status": "ok", "message": self.weather_module.format_forecast_message(data), "data": data}
        data = self.weather_module.get_weather(city)
        return {"status": "ok", "message": self.weather_module.format_weather_message(data), "data": data}

    def _handle_currency_command(self, text: str) -> Dict:
        if not self.currency_module:
            return {"status": "error", "message": "Модуль валют не загружен"}
        if any(word in text for word in ["конверт", "переведи", "сколько"]):
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
        rates = self.currency_module.get_multiple_rates()
        return {"status": "ok", "message": self.currency_module.format_multiple_rates_message(rates), "data": rates}

    def _handle_news_command(self, text: str) -> Dict:
        if not self.news_module:
            return {"status": "error", "message": "Модуль новостей не загружен"}
        if "найди" in text or "поиск" in text or "про" in text:
            query = text.replace("найди новости про", "").replace("новости про", "").replace("найди", "").strip()
            if query:
                data = self.news_module.search_news(query)
                return {"status": "ok", "message": self.news_module.format_news_message(data), "data": data}
        if "технолог" in text or "tech" in text:
            data = self.news_module.get_tech_news()
        elif "бизнес" in text or "финанс" in text or "эконом" in text:
            data = self.news_module.get_business_news()
        elif "спорт" in text:
            data = self.news_module.get_sports_news()
        else:
            data = self.news_module.get_top_headlines()
        return {"status": "ok", "message": self.news_module.format_news_message(data), "data": data}

    def _handle_learning_command(self, text: str) -> Dict:
        if not self.learning_manager or not self.learning_manager.adaptive_ml:
            return {"status": "error", "message": "Модуль обучения не загружен"}
        return {"status": "ok", "message": "Команда обучения принята"}

    def _handle_alias_command(self, text: str) -> Dict:
        if not self.learning_manager or not self.learning_manager.alias_system:
            return {"status": "error", "message": "Система алиасов не загружена"}
        return {"status": "ok", "message": "Команда алиаса принята"}

    def _get_learning_status(self) -> Dict:
        if not self.learning_manager:
            return {"status": "error", "message": "Модули обучения не загружены"}
        return self.learning_manager.get_learning_status()

    def start(self):
        self.logger.info("Запуск JARVIS...")
        self.running = True
        greeting = self.learning_manager.get_greeting() if self.learning_manager else "Здравствуйте, сэр. JARVIS готов к работе."
        self.logger.info(greeting)
        if self.hud:
            self.hud.set_status("ONLINE")
        if self.wake_word_service and self.config.get("windows.wake_word_enabled", False):
            self.wake_word_service.start(callback=self._on_wake_word)
        if self.clean_desktop and self.config.get("windows.clean_desktop_on_start", False):
            self.clean_desktop.enable_clean_mode()
        self.event_bus.publish("jarvis_started", {"timestamp": "now"})

    def _on_wake_word(self, text: str):
        self.logger.info("Wake word активирован: %s", text)
        if self.hud:
            self.hud.set_status("LISTENING")
            self.hud.set_voice_active(True)

    def stop(self):
        self.logger.info("Остановка JARVIS...")
        self.running = False
        if self.wake_word_service and self.wake_word_service.is_running():
            self.wake_word_service.stop()
        if self.clean_desktop and self.clean_desktop.is_hidden():
            self.clean_desktop.disable_clean_mode()
        self.event_bus.publish("jarvis_stopped", {"timestamp": "now"})

    def get_status(self) -> Dict:
        return {
            "running": self.running,
            "modules_loaded": len(self.modules),
            "plugins_loaded": len(self.plugin_manager.plugins),
            "learning_enabled": self.learning_manager is not None,
            "hud_enabled": self.hud is not None,
            "info_modules": {
                "weather": self.weather_module is not None,
                "currency": self.currency_module is not None,
                "news": self.news_module is not None,
            },
            "windows_integration": {
                "enabled": self.windows_integration is not None,
                "toast_enabled": self.toast_notifications is not None,
                "wake_word_enabled": self.wake_word_service is not None and self.wake_word_service.is_running(),
                "clean_desktop": self.clean_desktop is not None and self.clean_desktop.is_hidden(),
                "apps_count": self.app_launcher.get_apps_count() if self.app_launcher else 0,
            },
        }
