"""JARVIS Brain - Ð³Ð»Ð°Ð²Ð½ÑÐ¹ ÐºÐ¾Ð½ÑÑÐ¾Ð»Ð»ÐµÑ ÑÐ¸ÑÑÐµÐ¼Ñ"""

import logging
from typing import Dict

from core.config import Config
from core.event_bus import EventBus
from core.plugin_manager import PluginManager


class JarvisBrain:
    """Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½ÑÐ¹ ÐºÐ¾Ð½ÑÑÐ¾Ð»Ð»ÐµÑ JARVIS."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ JARVIS Brain...")
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
        self.logger.info("JARVIS Brain Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½")

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("JARVIS")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
        return logger

    def initialize(self):
        self.logger.info("ÐÐ°Ð¿ÑÑÐº Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹...")
        self._init_learning_modules()
        self._init_windows_integration()
        self._init_hud()
        self._init_info_modules()
        self._init_system_modules()
        self.plugin_manager.load_plugins()
        self.logger.info("ÐÑÐµ Ð¼Ð¾Ð´ÑÐ»Ð¸ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ")

    def _init_learning_modules(self):
        try:
            from ai.learning_manager import LearningManager
            self.learning_manager = LearningManager(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ: %s", e)
            self.learning_manager = None

    def _init_windows_integration(self):
        try:
            from modules.windows_integration import WindowsIntegration
            self.windows_integration = WindowsIntegration(self)
            self.logger.info("â Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ð¸: %s", e)
            self.windows_integration = None
        try:
            from modules.toast_notifications import ToastNotifications
            self.toast_notifications = ToastNotifications(self)
            self.logger.info("â Toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ð¹: %s", e)
            self.toast_notifications = None
        try:
            from modules.wake_word_service import WakeWordService
            self.wake_word_service = WakeWordService(self)
            self.logger.info("â Wake word ÑÐµÑÐ²Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ wake word ÑÐµÑÐ²Ð¸ÑÐ°: %s", e)
            self.wake_word_service = None
        try:
            from modules.clean_desktop import CleanDesktop
            self.clean_desktop = CleanDesktop(self)
            self.logger.info("â Clean Desktop Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Clean Desktop: %s", e)
            self.clean_desktop = None
        try:
            from modules.app_launcher import AppLauncher
            self.app_launcher = AppLauncher(self)
            self.logger.info("â App Launcher Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ App Launcher: %s", e)
            self.app_launcher = None

    def _init_voice(self):
        try:
            from voice.speaker import VoiceSpeaker
            self.voice_speaker = VoiceSpeaker(self)
            self.logger.info("â ÐÐ¾Ð»Ð¾ÑÐ¾Ð²Ð¾Ð¹ Ð¼Ð¾Ð´ÑÐ»Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²Ð¾Ð³Ð¾ Ð¼Ð¾Ð´ÑÐ»Ñ: %s", e)
            self.voice_speaker = None

    def _init_hud(self):
        try:
            from hud.holographic_ui import HolographicHUD
            self.hud = HolographicHUD(self)
            self.logger.info("â HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ HUD: %s", e)
            self.hud = None

    def _init_info_modules(self):
        try:
            from modules.weather import WeatherModule
            self.weather_module = WeatherModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ: %s", e)
            self.weather_module = None
        try:
            from modules.currency import CurrencyModule
            self.currency_module = CurrencyModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð²Ð°Ð»ÑÑ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð²Ð°Ð»ÑÑ: %s", e)
            self.currency_module = None
        try:
            from modules.news import NewsModule
            self.news_module = NewsModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹: %s", e)
            self.news_module = None

    def reload_api_integrations(self):
        """ÐÐµÑÐµÑÐ¸ÑÐ°ÑÑ ÐºÐ»ÑÑÐ¸ Ð¸ Ð¿ÐµÑÐµÑÐ¾Ð·Ð´Ð°ÑÑ Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ð¸, Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÑÑÐ¸Ðµ API-ÐºÐ»ÑÑÐ¸."""
        self.config.reload_secrets()
        self._init_info_modules()
        self.logger.info("API-Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð¿ÐµÑÐµÑÐ¸ÑÐ°Ð½Ñ; ÐºÐ»ÑÑÐ¸ OpenWeather Ð¸ NewsAPI Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ñ")

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
                self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ %s Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½", key)
            except Exception as e:
                self.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ %s: %s", key, e)

    def process_command(self, text: str) -> Dict:
        self.logger.info("ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ: %s", text)
        if self.hud:
            self.hud.set_status("PROCESSING")
            self.hud.set_voice_active(True)
        if self.learning_manager:
            learning_result = self.learning_manager.process_command(text)
            processed_text = learning_result.get("processed", text)
            if learning_result.get("learning_suggestion"):
                self.logger.info("ÐÑÐµÐ´Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ: %s", learning_result['learning_suggestion'])
            optimization_result = self.learning_manager.optimize_runtime(text)
            if optimization_result.get("recommendations"):
                self.logger.info("Ð ÐµÐºÐ¾Ð¼ÐµÐ½Ð´Ð°ÑÐ¸Ð¸ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸: %s", optimization_result['recommendations'])
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
        """ÐÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        text_lower = text.lower().strip()
        if any(word in text_lower for word in ["Ð¿Ð¾Ð³Ð¾Ð´Ð°", "ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÐ°", "Ð¿ÑÐ¾Ð³Ð½Ð¾Ð·"]):
            return self._handle_weather_command(text_lower)
        elif any(word in text_lower for word in ["ÐºÑÑÑ", "Ð²Ð°Ð»ÑÑ", "Ð´Ð¾Ð»Ð»Ð°Ñ", "ÐµÐ²ÑÐ¾", "ÑÑÐ±Ð»", "Ð±Ð¸ÑÐºÐ¾Ð¸Ð½", "btc", "usd", "eur"]):
            return self._handle_currency_command(text_lower)
        elif any(word in text_lower for word in ["Ð½Ð¾Ð²Ð¾ÑÑ", "ÑÑÐ¾ ÑÐ»ÑÑÐ¸Ð»Ð¾ÑÑ", "ÑÑÐ¾ Ð¿ÑÐ¾Ð¸Ð·Ð¾ÑÐ»Ð¾", "headline"]):
            return self._handle_news_command(text_lower)
        elif "Ð¿Ð¾ÐºÐ°Ð¶Ð¸ hud" in text_lower or "Ð²ÐºÐ»ÑÑÐ¸ Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ" in text_lower:
            if self.hud:
                self.hud.show()
                return {"status": "ok", "message": "HUD Ð°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½"}
        elif "ÑÐºÑÐ¾Ð¹ hud" in text_lower or "Ð²ÑÐºÐ»ÑÑÐ¸ Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ" in text_lower:
            if self.hud:
                self.hud.hide()
                return {"status": "ok", "message": "HUD Ð´ÐµÐ°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½"}
        elif "ÑÐ¸ÑÑÑÐ¹ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»" in text_lower or "ÑÐºÑÐ¾Ð¹ Ð¸ÐºÐ¾Ð½ÐºÐ¸" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.enable_clean_mode()
        elif "Ð¿Ð¾ÐºÐ°Ð¶Ð¸ Ð¸ÐºÐ¾Ð½ÐºÐ¸" in text_lower or "Ð¾Ð±ÑÑÐ½ÑÐ¹ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.disable_clean_mode()
        elif "Ð¾ÑÐºÑÐ¾Ð¹" in text_lower or "Ð·Ð°Ð¿ÑÑÑÐ¸" in text_lower:
            if self.app_launcher:
                app_name = text_lower.replace("Ð¾ÑÐºÑÐ¾Ð¹", "").replace("Ð·Ð°Ð¿ÑÑÑÐ¸", "").strip()
                return self.app_launcher.launch(app_name)
        elif "ÑÐ¿Ð¸ÑÐ¾Ðº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹" in text_lower:
            if self.app_launcher:
                return self.app_launcher.list_apps()
        elif any(word in text_lower for word in ["Ð²ÑÐºÐ»ÑÑÐ¸", "Ð·Ð°Ð²ÐµÑÑÐ¸ ÑÐ°Ð±Ð¾ÑÑ"]):
            if "system" in self.modules:
                return self.modules["system"].shutdown()
        elif any(word in text_lower for word in ["Ð¿ÐµÑÐµÐ·Ð°Ð³ÑÑÐ·Ð¸", "ÑÐµÑÑÐ°ÑÑ"]):
            if "system" in self.modules:
                return self.modules["system"].restart()
        elif any(word in text_lower for word in ["Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹", "Ð»Ð¾Ðº"]):
            if "system" in self.modules:
                return self.modules["system"].lock_screen()
        elif "ÑÐ°Ñ" in text_lower or "Ð²ÑÐµÐ¼Ñ" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_time()
        elif "Ð´Ð°ÑÐ°" in text_lower or "ÑÐ¸ÑÐ»Ð¾" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_date()
        elif "ÑÑÐ°ÑÑÑ" in text_lower or "ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ" in text_lower:
            if "hardware" in self.modules:
                return self.modules["hardware"].get_system_info()
        elif "ip" in text_lower or "Ð°Ð¹Ð¿Ð¸" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].get_ip()
        elif "ÑÐºÐ¾ÑÐ¾ÑÑÑ" in text_lower and "Ð¸Ð½ÑÐµÑÐ½ÐµÑ" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].speed_test()
        elif "Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº" in text_lower and self.windows_integration:
            if "Ð²ÐºÐ»ÑÑÐ¸" in text_lower:
                return self.windows_integration.enable_autostart()
            if "Ð²ÑÐºÐ»ÑÑÐ¸" in text_lower:
                return self.windows_integration.disable_autostart()
        elif "Ð½Ð°ÑÑÐ¸ÑÑ" in text_lower or "Ð·Ð°Ð¿Ð¾Ð¼Ð½Ð¸" in text_lower:
            return self._handle_learning_command(text)
        elif "Ð°Ð»Ð¸Ð°Ñ" in text_lower or "Ð¿ÑÐµÐ²Ð´Ð¾Ð½Ð¸Ð¼" in text_lower:
            return self._handle_alias_command(text)
        elif "ÑÑÐ°ÑÑÑ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ" in text_lower or "ÑÐµÐ¼Ñ ÑÑ Ð½Ð°ÑÑÐ¸Ð»ÑÑ" in text_lower:
            return self._get_learning_status()
        return {"status": "ok", "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð½Ðµ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð½Ð°", "text": text}

    def _handle_weather_command(self, text: str) -> Dict:
        if not self.weather_module:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        city = "ÐÐ¾ÑÐºÐ²Ð°"
        cities = ["Ð¼Ð¾ÑÐºÐ²Ð°", "ÑÐ°Ð½ÐºÑ-Ð¿ÐµÑÐµÑÐ±ÑÑÐ³", "Ð¿Ð¸ÑÐµÑ", "Ð½Ð¾Ð²Ð¾ÑÐ¸Ð±Ð¸ÑÑÐº", "ÐµÐºÐ°ÑÐµÑÐ¸Ð½Ð±ÑÑÐ³", "ÐºÐ°Ð·Ð°Ð½Ñ", "Ð½Ð¸Ð¶Ð½Ð¸Ð¹ Ð½Ð¾Ð²Ð³Ð¾ÑÐ¾Ð´", "ÑÐ°Ð¼Ð°ÑÐ°"]
        for city_name in cities:
            if city_name in text:
                city = "Ð¡Ð°Ð½ÐºÑ-ÐÐµÑÐµÑÐ±ÑÑÐ³" if city_name == "Ð¿Ð¸ÑÐµÑ" else city_name.capitalize()
                break
        if "Ð¿ÑÐ¾Ð³Ð½Ð¾Ð·" in text:
            data = self.weather_module.get_forecast(city)
            return {"status": "ok", "message": self.weather_module.format_forecast_message(data), "data": data}
        data = self.weather_module.get_weather(city)
        return {"status": "ok", "message": self.weather_module.format_weather_message(data), "data": data}

    def _handle_currency_command(self, text: str) -> Dict:
        if not self.currency_module:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð²Ð°Ð»ÑÑ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        if any(word in text for word in ["ÐºÐ¾Ð½Ð²ÐµÑÑ", "Ð¿ÐµÑÐµÐ²ÐµÐ´Ð¸", "ÑÐºÐ¾Ð»ÑÐºÐ¾"]):
            if "Ð´Ð¾Ð»Ð»Ð°Ñ" in text or "usd" in text:
                rate = self.currency_module.get_usd_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÐÐ´Ð¸Ð½ Ð´Ð¾Ð»Ð»Ð°Ñ ÑÑÐ¾Ð¸Ñ {rate['rate']} ÑÑÐ±Ð»ÐµÐ¹"}
            elif "ÐµÐ²ÑÐ¾" in text or "eur" in text:
                rate = self.currency_module.get_eur_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÐÐ´Ð½Ð¾ ÐµÐ²ÑÐ¾ ÑÑÐ¾Ð¸Ñ {rate['rate']} ÑÑÐ±Ð»ÐµÐ¹"}
            elif "Ð±Ð¸ÑÐºÐ¾Ð¸Ð½" in text or "bitcoin" in text or "btc" in text:
                rate = self.currency_module.get_btc_usd()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÐÐ´Ð¸Ð½ Ð±Ð¸ÑÐºÐ¾Ð¸Ð½ ÑÑÐ¾Ð¸Ñ ${rate['rate']}"}
        rates = self.currency_module.get_multiple_rates()
        return {"status": "ok", "message": self.currency_module.format_multiple_rates_message(rates), "data": rates}

    def _handle_news_command(self, text: str) -> Dict:
        if not self.news_module:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        if "Ð½Ð°Ð¹Ð´Ð¸" in text or "Ð¿Ð¾Ð¸ÑÐº" in text or "Ð¿ÑÐ¾" in text:
            query = text.replace("Ð½Ð°Ð¹Ð´Ð¸ Ð½Ð¾Ð²Ð¾ÑÑÐ¸ Ð¿ÑÐ¾", "").replace("Ð½Ð¾Ð²Ð¾ÑÑÐ¸ Ð¿ÑÐ¾", "").replace("Ð½Ð°Ð¹Ð´Ð¸", "").strip()
            if query:
                data = self.news_module.search_news(query)
                return {"status": "ok", "message": self.news_module.format_news_message(data), "data": data}
        if "ÑÐµÑÐ½Ð¾Ð»Ð¾Ð³" in text or "tech" in text:
            data = self.news_module.get_tech_news()
        elif "Ð±Ð¸Ð·Ð½ÐµÑ" in text or "ÑÐ¸Ð½Ð°Ð½Ñ" in text or "ÑÐºÐ¾Ð½Ð¾Ð¼" in text:
            data = self.news_module.get_business_news()
        elif "ÑÐ¿Ð¾ÑÑ" in text:
            data = self.news_module.get_sports_news()
        else:
            data = self.news_module.get_top_headlines()
        return {"status": "ok", "message": self.news_module.format_news_message(data), "data": data}

    def _handle_learning_command(self, text: str) -> Dict:
        if not self.learning_manager or not self.learning_manager.adaptive_ml:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        return {"status": "ok", "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð¿ÑÐ¸Ð½ÑÑÐ°"}

    def _handle_alias_command(self, text: str) -> Dict:
        if not self.learning_manager or not self.learning_manager.alias_system:
            return {"status": "error", "message": "Ð¡Ð¸ÑÑÐµÐ¼Ð° Ð°Ð»Ð¸Ð°ÑÐ¾Ð² Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°"}
        return {"status": "ok", "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð°Ð»Ð¸Ð°ÑÐ° Ð¿ÑÐ¸Ð½ÑÑÐ°"}

    def _get_learning_status(self) -> Dict:
        if not self.learning_manager:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ"}
        return self.learning_manager.get_learning_status()

    def start(self):
        self.logger.info("ÐÐ°Ð¿ÑÑÐº JARVIS...")
        self.running = True
        greeting = self.learning_manager.get_greeting() if self.learning_manager else "ÐÐ´ÑÐ°Ð²ÑÑÐ²ÑÐ¹ÑÐµ, ÑÑÑ. JARVIS Ð³Ð¾ÑÐ¾Ð² Ðº ÑÐ°Ð±Ð¾ÑÐµ."
        self.logger.info(greeting)
        if self.hud:
            self.hud.set_status("ONLINE")
        if self.wake_word_service and self.config.get("windows.wake_word_enabled", False):
            self.wake_word_service.start(callback=self._on_wake_word)
        if self.clean_desktop and self.config.get("windows.clean_desktop_on_start", False):
            self.clean_desktop.enable_clean_mode()
        self.event_bus.publish("jarvis_started", {"timestamp": "now"})

    def _on_wake_word(self, text: str):
        self.logger.info("Wake word Ð°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½: %s", text)
        if self.hud:
            self.hud.set_status("LISTENING")
            self.hud.set_voice_active(True)

    def stop(self):
        self.logger.info("ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° JARVIS...")
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
