"""JARVIS Brain - ÃÂ³ÃÂ»ÃÂ°ÃÂ²ÃÂ½ÃÃÂ¹ ÃÂºÃÂ¾ÃÂ½ÃÃÃÂ¾ÃÂ»ÃÂ»ÃÂµÃ ÃÃÂ¸ÃÃÃÂµÃÂ¼Ã"""

import logging
from typing import Dict

from core.config import Config
from core.event_bus import EventBus
from core.plugin_manager import PluginManager
from agents.agent_manager import AgentManager



    def _handle_agent_task(self, text: str) -> Dict:
        """Обработка задачи через систему агентов."""
        self.logger.info(f"Передача задачи агенту: {text}")

        try:
            result = self.agent_manager.execute_task(text)

            if result.get('status') == 'success':
                # Уведомляем пользователя
                if self.toast_notifications:
                    agent_name = result.get('agent', 'Агент')
                    self.toast_notifications.show_toast(
                        "JARVIS Agent",
                        f"Задача выполнена: {result.get('message', 'Успешно')}",
                        duration=5000
                    )

                # Сохраняем файлы если есть
                files = result.get('files', {})
                if files:
                    self.logger.info(f"Создано файлов: {len(files)}")
                    # Здесь можно добавить сохранение файлов на диск

                return {
                    "status": "success",
                    "message": result.get('message', 'Задача выполнена'),
                    "agent": result.get('agent', 'Unknown'),
                    "files_created": len(files)
                }
            else:
                return {
                    "status": "error",
                    "message": result.get('message', 'Ошибка выполнения задачи')
                }

        except Exception as e:
            self.logger.error(f"Ошибка при обработке задачи агентом: {e}")
            return {
                "status": "error",
                "message": f"Ошибка: {str(e)}"
            }

class JarvisBrain:
    """ÃÂ¦ÃÂµÃÂ½ÃÃÃÂ°ÃÂ»ÃÃÂ½ÃÃÂ¹ ÃÂºÃÂ¾ÃÂ½ÃÃÃÂ¾ÃÂ»ÃÂ»ÃÂµÃ JARVIS."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("ÃÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã JARVIS Brain...")
        self.config = Config()
        self.event_bus = EventBus()
        self.plugin_manager = PluginManager(self)
        self.agent_manager = AgentManager()
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
        self.logger.info("JARVIS Brain ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½")

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("JARVIS")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
        return logger

    def initialize(self):
        self.logger.info("ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂµÃÂ¹...")
        self._init_learning_modules()
        self._init_windows_integration()
        self._init_hud()
        self._init_info_modules()
        self._init_system_modules()
        self.plugin_manager.load_plugins()
        self.logger.info("ÃÃÃÂµ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂ¸ ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½Ã")

    def _init_learning_modules(self):
        try:
            from ai.learning_manager import LearningManager
            self.learning_manager = LearningManager(self)
            self.logger.info("Ã¢ ÃÃÂ¾ÃÂ´ÃÃÂ»ÃÂ¸ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½Ã")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂµÃÂ¹ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã: %s", e)
            self.learning_manager = None

    def _init_windows_integration(self):
        try:
            from modules.windows_integration import WindowsIntegration
            self.windows_integration = WindowsIntegration(self)
            self.logger.info("Ã¢ Windows ÃÂ¸ÃÂ½ÃÃÂµÃÂ³ÃÃÂ°ÃÃÂ¸Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½ÃÂ°")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ Windows ÃÂ¸ÃÂ½ÃÃÂµÃÂ³ÃÃÂ°ÃÃÂ¸ÃÂ¸: %s", e)
            self.windows_integration = None
        try:
            from modules.toast_notifications import ToastNotifications
            self.toast_notifications = ToastNotifications(self)
            self.logger.info("Ã¢ Toast ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½Ã")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ toast ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂ¹: %s", e)
            self.toast_notifications = None
        try:
            from modules.wake_word_service import WakeWordService
            self.wake_word_service = WakeWordService(self)
            self.logger.info("Ã¢ Wake word ÃÃÂµÃÃÂ²ÃÂ¸Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ wake word ÃÃÂµÃÃÂ²ÃÂ¸ÃÃÂ°: %s", e)
            self.wake_word_service = None
        try:
            from modules.clean_desktop import CleanDesktop
            self.clean_desktop = CleanDesktop(self)
            self.logger.info("Ã¢ Clean Desktop ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ Clean Desktop: %s", e)
            self.clean_desktop = None
        try:
            from modules.app_launcher import AppLauncher
            self.app_launcher = AppLauncher(self)
            self.logger.info("Ã¢ App Launcher ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ App Launcher: %s", e)
            self.app_launcher = None

    def _init_voice(self):
        try:
            from voice.speaker import VoiceSpeaker
            self.voice_speaker = VoiceSpeaker(self)
            self.logger.info("Ã¢ ÃÃÂ¾ÃÂ»ÃÂ¾ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ¹ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ³ÃÂ¾ÃÂ»ÃÂ¾ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»Ã: %s", e)
            self.voice_speaker = None

    def _init_hud(self):
        try:
            from hud.holographic_ui import HolographicHUD
            self.hud = HolographicHUD(self)
            self.logger.info("Ã¢ HUD ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ HUD: %s", e)
            self.hud = None

    def _init_info_modules(self):
        try:
            from modules.weather import WeatherModule
            self.weather_module = WeatherModule(self)
            self.logger.info("Ã¢ ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã: %s", e)
            self.weather_module = None
        try:
            from modules.currency import CurrencyModule
            self.currency_module = CurrencyModule(self)
            self.logger.info("Ã¢ ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ²ÃÂ°ÃÂ»ÃÃ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ²ÃÂ°ÃÂ»ÃÃ: %s", e)
            self.currency_module = None
        try:
            from modules.news import NewsModule
            self.news_module = NewsModule(self)
            self.logger.info("Ã¢ ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃÃÂµÃÂ¹ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½")
        except Exception as e:
            self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃÃÂµÃÂ¹: %s", e)
            self.news_module = None

    def reload_api_integrations(self):
        """ÃÃÂµÃÃÂµÃÃÂ¸ÃÃÂ°ÃÃ ÃÂºÃÂ»ÃÃÃÂ¸ ÃÂ¸ ÃÂ¿ÃÂµÃÃÂµÃÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÃ ÃÂ¸ÃÂ½ÃÃÂµÃÂ³ÃÃÂ°ÃÃÂ¸ÃÂ¸, ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÃÃÃÂ¸ÃÂµ API-ÃÂºÃÂ»ÃÃÃÂ¸."""
        self.config.reload_secrets()
        self._init_info_modules()
        self.logger.info("API-ÃÂ½ÃÂ°ÃÃÃÃÂ¾ÃÂ¹ÃÂºÃÂ¸ ÃÂ¿ÃÂµÃÃÂµÃÃÂ¸ÃÃÂ°ÃÂ½Ã; ÃÂºÃÂ»ÃÃÃÂ¸ OpenWeather ÃÂ¸ NewsAPI ÃÂ¾ÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½Ã")

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
                self.logger.info("Ã¢ ÃÃÂ¾ÃÂ´ÃÃÂ»Ã %s ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½", key)
            except Exception as e:
                self.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»Ã %s: %s", key, e)

    def process_command(self, text: str) -> Dict:
        self.logger.info("ÃÃÂ±ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂºÃÂ° ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´Ã: %s", text)
        if self.hud:
            self.hud.set_status("PROCESSING")
            self.hud.set_voice_active(True)
        if self.learning_manager:
            learning_result = self.learning_manager.process_command(text)
            processed_text = learning_result.get("processed", text)
            if learning_result.get("learning_suggestion"):
                self.logger.info("ÃÃÃÂµÃÂ´ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã: %s", learning_result['learning_suggestion'])
            optimization_result = self.learning_manager.optimize_runtime(text)
            if optimization_result.get("recommendations"):
                self.logger.info("ÃÂ ÃÂµÃÂºÃÂ¾ÃÂ¼ÃÂµÃÂ½ÃÂ´ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸: %s", optimization_result['recommendations'])
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
        """ÃÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        text_lower = text.lower().strip()
        # Проверка задач для агентов
        agent_keywords = ["создай", "напиши", "разработай", "программа", "код", "сайт", "лендинг", "анализ", "данные"]
        if any(keyword in text_lower for keyword in agent_keywords):
            return self._handle_agent_task(text_lower)

        if any(word in text_lower for word in ["ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´ÃÂ°", "ÃÃÂµÃÂ¼ÃÂ¿ÃÂµÃÃÂ°ÃÃÃÃÂ°", "ÃÂ¿ÃÃÂ¾ÃÂ³ÃÂ½ÃÂ¾ÃÂ·"]):
            return self._handle_weather_command(text_lower)
        elif any(word in text_lower for word in ["ÃÂºÃÃÃ", "ÃÂ²ÃÂ°ÃÂ»ÃÃ", "ÃÂ´ÃÂ¾ÃÂ»ÃÂ»ÃÂ°Ã", "ÃÂµÃÂ²ÃÃÂ¾", "ÃÃÃÂ±ÃÂ»", "ÃÂ±ÃÂ¸ÃÃÂºÃÂ¾ÃÂ¸ÃÂ½", "btc", "usd", "eur"]):
            return self._handle_currency_command(text_lower)
        elif any(word in text_lower for word in ["ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃ", "ÃÃÃÂ¾ ÃÃÂ»ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÃ", "ÃÃÃÂ¾ ÃÂ¿ÃÃÂ¾ÃÂ¸ÃÂ·ÃÂ¾ÃÃÂ»ÃÂ¾", "headline"]):
            return self._handle_news_command(text_lower)
        elif "ÃÂ¿ÃÂ¾ÃÂºÃÂ°ÃÂ¶ÃÂ¸ hud" in text_lower or "ÃÂ²ÃÂºÃÂ»ÃÃÃÂ¸ ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹Ã" in text_lower:
            if self.hud:
                self.hud.show()
                return {"status": "ok", "message": "HUD ÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½"}
        elif "ÃÃÂºÃÃÂ¾ÃÂ¹ hud" in text_lower or "ÃÂ²ÃÃÂºÃÂ»ÃÃÃÂ¸ ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹Ã" in text_lower:
            if self.hud:
                self.hud.hide()
                return {"status": "ok", "message": "HUD ÃÂ´ÃÂµÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½"}
        elif "ÃÃÂ¸ÃÃÃÃÂ¹ ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂ¸ÃÂ¹ ÃÃÃÂ¾ÃÂ»" in text_lower or "ÃÃÂºÃÃÂ¾ÃÂ¹ ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ¸" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.enable_clean_mode()
        elif "ÃÂ¿ÃÂ¾ÃÂºÃÂ°ÃÂ¶ÃÂ¸ ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ¸" in text_lower or "ÃÂ¾ÃÂ±ÃÃÃÂ½ÃÃÂ¹ ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂ¸ÃÂ¹ ÃÃÃÂ¾ÃÂ»" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.disable_clean_mode()
        elif "ÃÂ¾ÃÃÂºÃÃÂ¾ÃÂ¹" in text_lower or "ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÃÂ¸" in text_lower:
            if self.app_launcher:
                app_name = text_lower.replace("ÃÂ¾ÃÃÂºÃÃÂ¾ÃÂ¹", "").replace("ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÃÂ¸", "").strip()
                return self.app_launcher.launch(app_name)
        elif "ÃÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹" in text_lower:
            if self.app_launcher:
                return self.app_launcher.list_apps()
        elif any(word in text_lower for word in ["ÃÂ²ÃÃÂºÃÂ»ÃÃÃÂ¸", "ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÃÃÂ¸ ÃÃÂ°ÃÂ±ÃÂ¾ÃÃ"]):
            if "system" in self.modules:
                return self.modules["system"].shutdown()
        elif any(word in text_lower for word in ["ÃÂ¿ÃÂµÃÃÂµÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂ¸", "ÃÃÂµÃÃÃÂ°ÃÃ"]):
            if "system" in self.modules:
                return self.modules["system"].restart()
        elif any(word in text_lower for word in ["ÃÂ·ÃÂ°ÃÂ±ÃÂ»ÃÂ¾ÃÂºÃÂ¸ÃÃÃÂ¹", "ÃÂ»ÃÂ¾ÃÂº"]):
            if "system" in self.modules:
                return self.modules["system"].lock_screen()
        elif "ÃÃÂ°Ã" in text_lower or "ÃÂ²ÃÃÂµÃÂ¼Ã" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_time()
        elif "ÃÂ´ÃÂ°ÃÃÂ°" in text_lower or "ÃÃÂ¸ÃÃÂ»ÃÂ¾" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_date()
        elif "ÃÃÃÂ°ÃÃÃ" in text_lower or "ÃÃÂ¾ÃÃÃÂ¾ÃÃÂ½ÃÂ¸ÃÂµ" in text_lower:
            if "hardware" in self.modules:
                return self.modules["hardware"].get_system_info()
        elif "ip" in text_lower or "ÃÂ°ÃÂ¹ÃÂ¿ÃÂ¸" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].get_ip()
        elif "ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃ" in text_lower and "ÃÂ¸ÃÂ½ÃÃÂµÃÃÂ½ÃÂµÃ" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].speed_test()
        elif "ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº" in text_lower and self.windows_integration:
            if "ÃÂ²ÃÂºÃÂ»ÃÃÃÂ¸" in text_lower:
                return self.windows_integration.enable_autostart()
            if "ÃÂ²ÃÃÂºÃÂ»ÃÃÃÂ¸" in text_lower:
                return self.windows_integration.disable_autostart()
        elif "ÃÂ½ÃÂ°ÃÃÃÂ¸ÃÃ" in text_lower or "ÃÂ·ÃÂ°ÃÂ¿ÃÂ¾ÃÂ¼ÃÂ½ÃÂ¸" in text_lower:
            return self._handle_learning_command(text)
        elif "ÃÂ°ÃÂ»ÃÂ¸ÃÂ°Ã" in text_lower or "ÃÂ¿ÃÃÂµÃÂ²ÃÂ´ÃÂ¾ÃÂ½ÃÂ¸ÃÂ¼" in text_lower:
            return self._handle_alias_command(text)
        elif "ÃÃÃÂ°ÃÃÃ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã" in text_lower or "ÃÃÂµÃÂ¼Ã ÃÃ ÃÂ½ÃÂ°ÃÃÃÂ¸ÃÂ»ÃÃ" in text_lower:
            return self._get_learning_status()
        return {"status": "ok", "message": "ÃÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ° ÃÂ½ÃÂµ ÃÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ½ÃÂ°", "text": text}

    def _handle_weather_command(self, text: str) -> Dict:
        if not self.weather_module:
            return {"status": "error", "message": "ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½"}
        city = "ÃÃÂ¾ÃÃÂºÃÂ²ÃÂ°"
        cities = ["ÃÂ¼ÃÂ¾ÃÃÂºÃÂ²ÃÂ°", "ÃÃÂ°ÃÂ½ÃÂºÃ-ÃÂ¿ÃÂµÃÃÂµÃÃÂ±ÃÃÃÂ³", "ÃÂ¿ÃÂ¸ÃÃÂµÃ", "ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃÂ¸ÃÂ±ÃÂ¸ÃÃÃÂº", "ÃÂµÃÂºÃÂ°ÃÃÂµÃÃÂ¸ÃÂ½ÃÂ±ÃÃÃÂ³", "ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÂ½Ã", "ÃÂ½ÃÂ¸ÃÂ¶ÃÂ½ÃÂ¸ÃÂ¹ ÃÂ½ÃÂ¾ÃÂ²ÃÂ³ÃÂ¾ÃÃÂ¾ÃÂ´", "ÃÃÂ°ÃÂ¼ÃÂ°ÃÃÂ°"]
        for city_name in cities:
            if city_name in text:
                city = "ÃÂ¡ÃÂ°ÃÂ½ÃÂºÃ-ÃÃÂµÃÃÂµÃÃÂ±ÃÃÃÂ³" if city_name == "ÃÂ¿ÃÂ¸ÃÃÂµÃ" else city_name.capitalize()
                break
        if "ÃÂ¿ÃÃÂ¾ÃÂ³ÃÂ½ÃÂ¾ÃÂ·" in text:
            data = self.weather_module.get_forecast(city)
            return {"status": "ok", "message": self.weather_module.format_forecast_message(data), "data": data}
        data = self.weather_module.get_weather(city)
        return {"status": "ok", "message": self.weather_module.format_weather_message(data), "data": data}

    def _handle_currency_command(self, text: str) -> Dict:
        if not self.currency_module:
            return {"status": "error", "message": "ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ²ÃÂ°ÃÂ»ÃÃ ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½"}
        if any(word in text for word in ["ÃÂºÃÂ¾ÃÂ½ÃÂ²ÃÂµÃÃ", "ÃÂ¿ÃÂµÃÃÂµÃÂ²ÃÂµÃÂ´ÃÂ¸", "ÃÃÂºÃÂ¾ÃÂ»ÃÃÂºÃÂ¾"]):
            if "ÃÂ´ÃÂ¾ÃÂ»ÃÂ»ÃÂ°Ã" in text or "usd" in text:
                rate = self.currency_module.get_usd_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÃÃÂ´ÃÂ¸ÃÂ½ ÃÂ´ÃÂ¾ÃÂ»ÃÂ»ÃÂ°Ã ÃÃÃÂ¾ÃÂ¸Ã {rate['rate']} ÃÃÃÂ±ÃÂ»ÃÂµÃÂ¹"}
            elif "ÃÂµÃÂ²ÃÃÂ¾" in text or "eur" in text:
                rate = self.currency_module.get_eur_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÃÃÂ´ÃÂ½ÃÂ¾ ÃÂµÃÂ²ÃÃÂ¾ ÃÃÃÂ¾ÃÂ¸Ã {rate['rate']} ÃÃÃÂ±ÃÂ»ÃÂµÃÂ¹"}
            elif "ÃÂ±ÃÂ¸ÃÃÂºÃÂ¾ÃÂ¸ÃÂ½" in text or "bitcoin" in text or "btc" in text:
                rate = self.currency_module.get_btc_usd()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÃÃÂ´ÃÂ¸ÃÂ½ ÃÂ±ÃÂ¸ÃÃÂºÃÂ¾ÃÂ¸ÃÂ½ ÃÃÃÂ¾ÃÂ¸Ã ${rate['rate']}"}
        rates = self.currency_module.get_multiple_rates()
        return {"status": "ok", "message": self.currency_module.format_multiple_rates_message(rates), "data": rates}

    def _handle_news_command(self, text: str) -> Dict:
        if not self.news_module:
            return {"status": "error", "message": "ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃÃÂµÃÂ¹ ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½"}
        if "ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂ¸" in text or "ÃÂ¿ÃÂ¾ÃÂ¸ÃÃÂº" in text or "ÃÂ¿ÃÃÂ¾" in text:
            query = text.replace("ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂ¸ ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃÃÂ¸ ÃÂ¿ÃÃÂ¾", "").replace("ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÃÃÂ¸ ÃÂ¿ÃÃÂ¾", "").replace("ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂ¸", "").strip()
            if query:
                data = self.news_module.search_news(query)
                return {"status": "ok", "message": self.news_module.format_news_message(data), "data": data}
        if "ÃÃÂµÃÃÂ½ÃÂ¾ÃÂ»ÃÂ¾ÃÂ³" in text or "tech" in text:
            data = self.news_module.get_tech_news()
        elif "ÃÂ±ÃÂ¸ÃÂ·ÃÂ½ÃÂµÃ" in text or "ÃÃÂ¸ÃÂ½ÃÂ°ÃÂ½Ã" in text or "ÃÃÂºÃÂ¾ÃÂ½ÃÂ¾ÃÂ¼" in text:
            data = self.news_module.get_business_news()
        elif "ÃÃÂ¿ÃÂ¾ÃÃ" in text:
            data = self.news_module.get_sports_news()
        else:
            data = self.news_module.get_top_headlines()
        return {"status": "ok", "message": self.news_module.format_news_message(data), "data": data}

    def _handle_learning_command(self, text: str) -> Dict:
        if not self.learning_manager or not self.learning_manager.adaptive_ml:
            return {"status": "error", "message": "ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½"}
        return {"status": "ok", "message": "ÃÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ° ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ¿ÃÃÂ¸ÃÂ½ÃÃÃÂ°"}

    def _handle_alias_command(self, text: str) -> Dict:
        if not self.learning_manager or not self.learning_manager.alias_system:
            return {"status": "error", "message": "ÃÂ¡ÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÂ°ÃÂ»ÃÂ¸ÃÂ°ÃÃÂ¾ÃÂ² ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½ÃÂ°"}
        return {"status": "ok", "message": "ÃÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ° ÃÂ°ÃÂ»ÃÂ¸ÃÂ°ÃÃÂ° ÃÂ¿ÃÃÂ¸ÃÂ½ÃÃÃÂ°"}

    def _get_learning_status(self) -> Dict:
        if not self.learning_manager:
            return {"status": "error", "message": "ÃÃÂ¾ÃÂ´ÃÃÂ»ÃÂ¸ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½Ã"}
        return self.learning_manager.get_learning_status()

    def start(self):
        self.logger.info("ÃÃÂ°ÃÂ¿ÃÃÃÂº JARVIS...")
        self.running = True
        greeting = self.learning_manager.get_greeting() if self.learning_manager else "ÃÃÂ´ÃÃÂ°ÃÂ²ÃÃÃÂ²ÃÃÂ¹ÃÃÂµ, ÃÃÃ. JARVIS ÃÂ³ÃÂ¾ÃÃÂ¾ÃÂ² ÃÂº ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂµ."
        self.logger.info(greeting)
        if self.hud:
            self.hud.set_status("ONLINE")
        if self.wake_word_service and self.config.get("windows.wake_word_enabled", False):
            self.wake_word_service.start(callback=self._on_wake_word)
        if self.clean_desktop and self.config.get("windows.clean_desktop_on_start", False):
            self.clean_desktop.enable_clean_mode()
        self.event_bus.publish("jarvis_started", {"timestamp": "now"})

    def _on_wake_word(self, text: str):
        self.logger.info("Wake word ÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½: %s", text)
        if self.hud:
            self.hud.set_status("LISTENING")
            self.hud.set_voice_active(True)

    def stop(self):
        self.logger.info("ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° JARVIS...")
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
