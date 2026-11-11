"""
JARVIS Brain - ÐÐ»Ð°Ð²Ð½ÑÐ¹ ÐºÐ¾Ð½ÑÑÐ¾Ð»Ð»ÐµÑ ÑÐ¸ÑÑÐµÐ¼Ñ
"""

import logging
from typing import Dict, Optional, Any
from core.config import Config
from core.event_bus import EventBus
from core.plugin_manager import PluginManager


class JarvisBrain:
    """Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½ÑÐ¹ ÐºÐ¾Ð½ÑÑÐ¾Ð»Ð»ÐµÑ JARVIS."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ JARVIS Brain...")
        
        # ÐÐ¾Ð½ÑÐ¸Ð³ÑÑÐ°ÑÐ¸Ñ
        self.config = Config()
        
        # Ð¨Ð¸Ð½Ð° ÑÐ¾Ð±ÑÑÐ¸Ð¹
        self.event_bus = EventBus()
        
        # ÐÐµÐ½ÐµÐ´Ð¶ÐµÑ Ð¿Ð»Ð°Ð³Ð¸Ð½Ð¾Ð²
        self.plugin_manager = PluginManager(self)
        
        # ÐÐ¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ
        self.learning_manager = None
        
        # Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ
        self.windows_integration = None
        self.toast_notifications = None
        self.wake_word_service = None
        self.clean_desktop = None
        self.app_launcher = None
        
        # HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ
        self.hud = None
        
        # ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¾Ð½Ð½ÑÐµ Ð¼Ð¾Ð´ÑÐ»Ð¸
        self.weather_module = None
        self.currency_module = None
        self.news_module = None
        
        # Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐµ Ð¼Ð¾Ð´ÑÐ»Ð¸
        self.modules = {}
        
        # Ð¡Ð¾ÑÑÐ¾ÑÐ½Ð¸Ðµ
        self.running = False
        
        self.logger.info("JARVIS Brain Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½")

    def _setup_logging(self) -> logging.Logger:
        """ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° Ð»Ð¾Ð³Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ñ."""
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
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð²ÑÐµÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹."""
        self.logger.info("ÐÐ°Ð¿ÑÑÐº Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹...")
        
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ
        self._init_learning_modules()
        
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ð¸
        self._init_windows_integration()
        
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ HUD
        self._init_hud()
        
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¾Ð½Ð½ÑÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹
        self._init_info_modules()
        
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ ÑÐ¸ÑÑÐµÐ¼Ð½ÑÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹
        self._init_system_modules()
        
        # ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¿Ð»Ð°Ð³Ð¸Ð½Ð¾Ð²
        self.plugin_manager.load_plugins()
        
        self.logger.info("ÐÑÐµ Ð¼Ð¾Ð´ÑÐ»Ð¸ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ")

    def _init_learning_modules(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ."""
        try:
            from ai.learning_manager import LearningManager
            self.learning_manager = LearningManager(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ: {e}")
            self.learning_manager = None

    def _init_windows_integration(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ð¸."""
        # Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ
        try:
            from modules.windows_integration import WindowsIntegration
            self.windows_integration = WindowsIntegration(self)
            self.logger.info("â Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ð¸: {e}")
            self.windows_integration = None
        
        # Toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ
        try:
            from modules.toast_notifications import ToastNotifications
            self.toast_notifications = ToastNotifications(self)
            self.logger.info("â Toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ð¹: {e}")
            self.toast_notifications = None
        
        # Wake word ÑÐµÑÐ²Ð¸Ñ
        try:
            from modules.wake_word_service import WakeWordService
            self.wake_word_service = WakeWordService(self)
            self.logger.info("â Wake word ÑÐµÑÐ²Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ wake word ÑÐµÑÐ²Ð¸ÑÐ°: {e}")
            self.wake_word_service = None
        
        # Clean Desktop
        try:
            from modules.clean_desktop import CleanDesktop
            self.clean_desktop = CleanDesktop(self)
            self.logger.info("â Clean Desktop Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Clean Desktop: {e}")
            self.clean_desktop = None
        
        # App Launcher
        try:
            from modules.app_launcher import AppLauncher
            self.app_launcher = AppLauncher(self)
            self.logger.info("â App Launcher Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ App Launcher: {e}")
            self.app_launcher = None

    def _init_voice(self):
        """Инициализация голосового модуля."""
        try:
            from voice.speaker import VoiceSpeaker
            self.voice_speaker = VoiceSpeaker(self)
            self.logger.info("✓ Голосовой модуль загружен")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки голосового модуля: {e}")
            self.voice_speaker = None

    def _init_hud(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹ÑÐ°."""
        try:
            from hud.holographic_ui import HolographicHUD
            self.hud = HolographicHUD(self)
            self.logger.info("â HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ HUD: {e}")
            self.hud = None

    def _init_info_modules(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¾Ð½Ð½ÑÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹."""
        # ÐÐ¾Ð³Ð¾Ð´Ð°
        try:
            from modules.weather import WeatherModule
            self.weather_module = WeatherModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ: {e}")
            self.weather_module = None
        
        # ÐÐ°Ð»ÑÑÑ
        try:
            from modules.currency import CurrencyModule
            self.currency_module = CurrencyModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð²Ð°Ð»ÑÑ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð²Ð°Ð»ÑÑ: {e}")
            self.currency_module = None
        
        # ÐÐ¾Ð²Ð¾ÑÑÐ¸
        try:
            from modules.news import NewsModule
            self.news_module = NewsModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹: {e}")
            self.news_module = None


    def _init_avatar_3d(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ 3D Ð³Ð¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¾Ð³Ð¾ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        try:
            from modules.avatar_3d import AvatarManager
            self.avatar_3d = AvatarManager(self)
            self.avatar_3d.initialize()
            self.logger.info("â 3D Ð°Ð²Ð°ÑÐ°Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ 3D Ð°Ð²Ð°ÑÐ°ÑÐ°: {e}")
            self.avatar_3d = None

    def _init_system_modules(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ ÑÐ¸ÑÑÐµÐ¼Ð½ÑÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹."""
        # Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐµ Ð¾Ð¿ÐµÑÐ°ÑÐ¸Ð¸
        try:
            from modules.system import SystemModule
            self.modules["system"] = SystemModule(self)
            self.logger.info("â Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐ¹ Ð¼Ð¾Ð´ÑÐ»Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ ÑÐ¸ÑÑÐµÐ¼Ð½Ð¾Ð³Ð¾ Ð¼Ð¾Ð´ÑÐ»Ñ: {e}")
        
        # Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿ÑÐ¾ÑÐµÑÑÐ°Ð¼Ð¸
        try:
            from modules.processes import ProcessModule
            self.modules["processes"] = ProcessModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð¿ÑÐ¾ÑÐµÑÑÐ¾Ð² Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð¿ÑÐ¾ÑÐµÑÑÐ¾Ð²: {e}")
        
        # Ð Ð°Ð±Ð¾ÑÐ° Ñ ÑÐ°Ð¹Ð»Ð°Ð¼Ð¸
        try:
            from modules.files import FileModule
            self.modules["files"] = FileModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ ÑÐ°Ð¹Ð»Ð¾Ð² Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ ÑÐ°Ð¹Ð»Ð¾Ð²: {e}")
        
        # Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¾ÐºÐ½Ð°Ð¼Ð¸
        try:
            from modules.windows import WindowModule
            self.modules["windows"] = WindowModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð¾ÐºÐ¾Ð½ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð¾ÐºÐ¾Ð½: {e}")
        
        # Ð¡ÐµÑÐµÐ²ÑÐµ Ð¾Ð¿ÐµÑÐ°ÑÐ¸Ð¸
        try:
            from modules.network import NetworkModule
            self.modules["network"] = NetworkModule(self)
            self.logger.info("â Ð¡ÐµÑÐµÐ²Ð¾Ð¹ Ð¼Ð¾Ð´ÑÐ»Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ ÑÐµÑÐµÐ²Ð¾Ð³Ð¾ Ð¼Ð¾Ð´ÑÐ»Ñ: {e}")
        
        # ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ Ð¾Ð±Ð¾ÑÑÐ´Ð¾Ð²Ð°Ð½Ð¸Ñ
        try:
            from modules.hardware import HardwareModule
            self.modules["hardware"] = HardwareModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð¾Ð±Ð¾ÑÑÐ´Ð¾Ð²Ð°Ð½Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð¾Ð±Ð¾ÑÑÐ´Ð¾Ð²Ð°Ð½Ð¸Ñ: {e}")
        
        # Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿Ð¸ÑÐ°Ð½Ð¸ÐµÐ¼
        try:
            from modules.power import PowerModule
            self.modules["power"] = PowerModule(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ: {e}")

        # ÐÐ½Ð°Ð»Ð¸Ð· Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹
        try:
            from modules.app_analyzer import AppAnalyzer
            self.modules["app_analyzer"] = AppAnalyzer(self)
            self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð°Ð½Ð°Ð»Ð¸Ð·Ð° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÑÐ»Ñ Ð°Ð½Ð°Ð»Ð¸Ð·Ð° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹: {e}")

    def process_command(self, text: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ñ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°Ð½Ð¸ÐµÐ¼ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ."""
        self.logger.info(f"ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ: {text}")
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ HUD ÑÑÐ°ÑÑÑÐ°
        if self.hud:
            self.hud.set_status("PROCESSING")
            self.hud.set_voice_active(True)
        
        # ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÑÐµÑÐµÐ· Ð¼Ð¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ
        if self.learning_manager:
            learning_result = self.learning_manager.process_command(text)
            processed_text = learning_result.get("processed", text)
            
            if learning_result.get("learning_suggestion"):
                self.logger.info(f"ÐÑÐµÐ´Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ: {learning_result['learning_suggestion']}")
        else:
            processed_text = text
            learning_result = {"original": text, "processed": text}
        
        # ÐÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
        result = self._execute_command(processed_text)
        
        # ÐÐ±ÑÐµÐ´Ð¸Ð½ÐµÐ½Ð¸Ðµ ÑÐµÐ·ÑÐ»ÑÑÐ°ÑÐ¾Ð²
        result["learning_info"] = learning_result
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ HUD
        if self.hud:
            self.hud.set_status("READY")
            self.hud.set_voice_active(False)
        
        return result

    def _execute_command(self, text: str) -> Dict:
        """ÐÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        text_lower = text.lower().strip()
        
        # === ÐÐÐÐÐÐ ===
        if any(word in text_lower for word in ["Ð¿Ð¾Ð³Ð¾Ð´Ð°", "ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÐ°", "Ð¿ÑÐ¾Ð³Ð½Ð¾Ð·"]):
            return self._handle_weather_command(text_lower)
        
        # === ÐÐÐÐ®Ð¢Ð« ===
        elif any(word in text_lower for word in ["ÐºÑÑÑ", "Ð²Ð°Ð»ÑÑ", "Ð´Ð¾Ð»Ð»Ð°Ñ", "ÐµÐ²ÑÐ¾", "ÑÑÐ±Ð»", "Ð±Ð¸ÑÐºÐ¾Ð¸Ð½", "bitcoin"]):
            return self._handle_currency_command(text_lower)
        
        # === ÐÐÐÐÐ¡Ð¢Ð ===
        elif any(word in text_lower for word in ["Ð½Ð¾Ð²Ð¾ÑÑ", "ÑÑÐ¾ ÑÐ»ÑÑÐ¸Ð»Ð¾ÑÑ", "ÑÑÐ¾ Ð¿ÑÐ¾Ð¸Ð·Ð¾ÑÐ»Ð¾", "headline"]):
            return self._handle_news_command(text_lower)
        
        # === HUD ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ ===
        elif "Ð¿Ð¾ÐºÐ°Ð¶Ð¸ hud" in text_lower or "Ð²ÐºÐ»ÑÑÐ¸ Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ" in text_lower:
            if self.hud:
                self.hud.show()
                return {"status": "ok", "message": "HUD Ð°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        elif "ÑÐºÑÐ¾Ð¹ hud" in text_lower or "Ð²ÑÐºÐ»ÑÑÐ¸ Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ" in text_lower:
            if self.hud:
                self.hud.hide()
                return {"status": "ok", "message": "HUD Ð´ÐµÐ°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        # === Clean Desktop ===
        elif "ÑÐ¸ÑÑÑÐ¹ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»" in text_lower or "ÑÐºÑÐ¾Ð¹ Ð¸ÐºÐ¾Ð½ÐºÐ¸" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.enable_clean_mode()
        
        elif "Ð¿Ð¾ÐºÐ°Ð¶Ð¸ Ð¸ÐºÐ¾Ð½ÐºÐ¸" in text_lower or "Ð¾Ð±ÑÑÐ½ÑÐ¹ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»" in text_lower:
            if self.clean_desktop:
                return self.clean_desktop.disable_clean_mode()
        
        # === ÐÐ°Ð¿ÑÑÐº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ ===
        elif "Ð¾ÑÐºÑÐ¾Ð¹" in text_lower or "Ð·Ð°Ð¿ÑÑÑÐ¸" in text_lower:
            if self.app_launcher:
                app_name = text_lower.replace("Ð¾ÑÐºÑÐ¾Ð¹", "").replace("Ð·Ð°Ð¿ÑÑÑÐ¸", "").strip()
                return self.app_launcher.launch(app_name)
        
        elif "ÑÐ¿Ð¸ÑÐ¾Ðº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹" in text_lower:
            if self.app_launcher:
                return self.app_launcher.list_apps()
        
        # === Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ ===
        elif any(word in text_lower for word in ["Ð²ÑÐºÐ»ÑÑÐ¸", "Ð·Ð°Ð²ÐµÑÑÐ¸ ÑÐ°Ð±Ð¾ÑÑ"]):
            if "system" in self.modules:
                return self.modules["system"].shutdown()
        
        elif any(word in text_lower for word in ["Ð¿ÐµÑÐµÐ·Ð°Ð³ÑÑÐ·Ð¸", "ÑÐµÑÑÐ°ÑÑ"]):
            if "system" in self.modules:
                return self.modules["system"].restart()
        
        elif any(word in text_lower for word in ["Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹", "Ð»Ð¾Ðº"]):
            if "system" in self.modules:
                return self.modules["system"].lock_screen()
        
        # === ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ ===
        elif "ÑÐ°Ñ" in text_lower or "Ð²ÑÐµÐ¼Ñ" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_time()
        
        elif "Ð´Ð°ÑÐ°" in text_lower or "ÑÐ¸ÑÐ»Ð¾" in text_lower:
            if "system" in self.modules:
                return self.modules["system"].get_date()
        
        # === Ð¡ÑÐ°ÑÑÑ ÑÐ¸ÑÑÐµÐ¼Ñ ===
        elif "ÑÑÐ°ÑÑÑ" in text_lower or "ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ" in text_lower:
            if "hardware" in self.modules:
                return self.modules["hardware"].get_system_info()
        
        # === Ð¡ÐµÑÑ ===
        elif "ip" in text_lower or "Ð°Ð¹Ð¿Ð¸" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].get_ip()
        
        elif "ÑÐºÐ¾ÑÐ¾ÑÑÑ" in text_lower and "Ð¸Ð½ÑÐµÑÐ½ÐµÑ" in text_lower:
            if "network" in self.modules:
                return self.modules["network"].speed_test()
        
        # === Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ ===
        elif "Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº" in text_lower:
            if self.windows_integration:
                if "Ð²ÐºÐ»ÑÑÐ¸" in text_lower:
                    return self.windows_integration.enable_autostart()
                elif "Ð²ÑÐºÐ»ÑÑÐ¸" in text_lower:
                    return self.windows_integration.disable_autostart()
        
        # === ÐÐ±ÑÑÐµÐ½Ð¸Ðµ ===
        elif "Ð½Ð°ÑÑÐ¸ÑÑ" in text_lower or "Ð·Ð°Ð¿Ð¾Ð¼Ð½Ð¸" in text_lower:
            return self._handle_learning_command(text)
        
        elif "Ð°Ð»Ð¸Ð°Ñ" in text_lower or "Ð¿ÑÐµÐ²Ð´Ð¾Ð½Ð¸Ð¼" in text_lower:
            return self._handle_alias_command(text)
        
        elif "ÑÑÐ°ÑÑÑ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ" in text_lower or "ÑÐµÐ¼Ñ ÑÑ Ð½Ð°ÑÑÐ¸Ð»ÑÑ" in text_lower:
            return self._get_learning_status()
        

        # === 3D ÐÐ²Ð°ÑÐ°Ñ ===
        elif any(word in text_lower for word in ["Ð¿Ð¾ÐºÐ°Ð¶Ð¸ Ð°Ð²Ð°ÑÐ°Ñ", "Ð²ÐºÐ»ÑÑÐ¸ Ð°Ð²Ð°ÑÐ°Ñ", "Ð°Ð²Ð°ÑÐ°Ñ Ð¿Ð¾ÐºÐ°Ð¶Ð¸ÑÑ"]):
            if self.avatar_3d:
                result = self.avatar_3d.show()
                return {"status": result["status"], "message": result["message"]}

        elif any(word in text_lower for word in ["ÑÐºÑÐ¾Ð¹ Ð°Ð²Ð°ÑÐ°Ñ", "Ð²ÑÐºÐ»ÑÑÐ¸ Ð°Ð²Ð°ÑÐ°Ñ", "Ð°Ð²Ð°ÑÐ°Ñ Ð¸ÑÑÐµÐ·Ð½Ð¸"]):
            if self.avatar_3d:
                result = self.avatar_3d.hide()
                return {"status": result["status"], "message": result["message"]}

        elif "Ð¿ÐµÑÐµÐ¼ÐµÑÑÐ¸ Ð°Ð²Ð°ÑÐ°Ñ" in text_lower:
            if self.avatar_3d:
                # ÐÐ°ÑÑÐ¸Ð½Ð³ ÐºÐ¾Ð¾ÑÐ´Ð¸Ð½Ð°Ñ (ÑÐ¿ÑÐ¾ÑÑÐ½Ð½Ð¾)
                return {"status": "ok", "message": "ÐÑÐ¿Ð¾Ð»ÑÐ·ÑÐ¹ÑÐµ GUI Ð´Ð»Ñ Ð¿ÐµÑÐµÐ¼ÐµÑÐµÐ½Ð¸Ñ Ð°Ð²Ð°ÑÐ°ÑÐ°"}

        return {
            "status": "ok",
            "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð½Ðµ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð½Ð°",
            "text": text
        }

    def _handle_weather_command(self, text: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð¿Ð¾Ð³Ð¾Ð´Ñ."""
        if not self.weather_module:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        
        # ÐÐ·Ð²Ð»ÐµÑÐµÐ½Ð¸Ðµ Ð³Ð¾ÑÐ¾Ð´Ð°
        city = "ÐÐ¾ÑÐºÐ²Ð°"  # ÐÐ¾ ÑÐ¼Ð¾Ð»ÑÐ°Ð½Ð¸Ñ
        cities = ["Ð¼Ð¾ÑÐºÐ²Ð°", "ÑÐ°Ð½ÐºÑ-Ð¿ÐµÑÐµÑÐ±ÑÑÐ³", "Ð¿Ð¸ÑÐµÑ", "Ð½Ð¾Ð²Ð¾ÑÐ¸Ð±Ð¸ÑÑÐº", "ÐµÐºÐ°ÑÐµÑÐ¸Ð½Ð±ÑÑÐ³", 
                  "ÐºÐ°Ð·Ð°Ð½Ñ", "Ð½Ð¸Ð¶Ð½Ð¸Ð¹ Ð½Ð¾Ð²Ð³Ð¾ÑÐ¾Ð´", "ÑÐ°Ð¼Ð°ÑÐ°", "Ð¾Ð¼ÑÐº", "ÑÐµÐ»ÑÐ±Ð¸Ð½ÑÐº", "ÑÑÐ°", "ÑÐ¾ÑÑÐ¾Ð²"]
        
        for c in cities:
            if c in text:
                city = c.capitalize()
                if city == "ÐÐ¸ÑÐµÑ":
                    city = "Ð¡Ð°Ð½ÐºÑ-ÐÐµÑÐµÑÐ±ÑÑÐ³"
                break
        
        # ÐÑÐ¾Ð³Ð½Ð¾Ð· Ð¸Ð»Ð¸ ÑÐµÐºÑÑÐ°Ñ Ð¿Ð¾Ð³Ð¾Ð´Ð°
        if "Ð¿ÑÐ¾Ð³Ð½Ð¾Ð·" in text:
            forecast = self.weather_module.get_forecast(city)
            message = self.weather_module.format_forecast_message(forecast)
            return {"status": "ok", "message": message, "data": forecast}
        else:
            weather = self.weather_module.get_weather(city)
            message = self.weather_module.format_weather_message(weather)
            return {"status": "ok", "message": message, "data": weather}

    def _handle_currency_command(self, text: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð²Ð°Ð»ÑÑ."""
        if not self.currency_module:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð²Ð°Ð»ÑÑ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        
        # ÐÐ¾Ð½Ð²ÐµÑÑÐ°ÑÐ¸Ñ
        if "ÐºÐ¾Ð½Ð²ÐµÑÑ" in text or "Ð¿ÐµÑÐµÐ²ÐµÐ´Ð¸" in text or "ÑÐºÐ¾Ð»ÑÐºÐ¾" in text:
            # ÐÑÐ¾ÑÑÐ°Ñ ÐºÐ¾Ð½Ð²ÐµÑÑÐ°ÑÐ¸Ñ
            if "Ð´Ð¾Ð»Ð»Ð°Ñ" in text or "usd" in text:
                rate = self.currency_module.get_usd_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÐÐ´Ð¸Ð½ Ð´Ð¾Ð»Ð»Ð°Ñ ÑÑÐ¾Ð¸Ñ {rate['rate']} ÑÑÐ±Ð»ÐµÐ¹"}
            elif "ÐµÐ²ÑÐ¾" in text or "eur" in text:
                rate = self.currency_module.get_eur_rub()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÐÐ´Ð½Ð¾ ÐµÐ²ÑÐ¾ ÑÑÐ¾Ð¸Ñ {rate['rate']} ÑÑÐ±Ð»ÐµÐ¹"}
            elif "Ð±Ð¸ÑÐºÐ¾Ð¸Ð½" in text or "bitcoin" in text or "btc" in text:
                rate = self.currency_module.get_btc_usd()
                if rate["status"] == "ok":
                    return {"status": "ok", "message": f"ÐÐ´Ð¸Ð½ Ð±Ð¸ÑÐºÐ¾Ð¸Ð½ ÑÑÐ¾Ð¸Ñ ${rate['rate']}"}
        
        # ÐÑÐµ ÐºÑÑÑÑ
        rates = self.currency_module.get_multiple_rates()
        message = self.currency_module.format_multiple_rates_message(rates)
        return {"status": "ok", "message": message, "data": rates}

    def _handle_news_command(self, text: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹."""
        if not self.news_module:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        
        # ÐÐ¾Ð¸ÑÐº Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹
        if "Ð½Ð°Ð¹Ð´Ð¸" in text or "Ð¿Ð¾Ð¸ÑÐº" in text or "Ð¿ÑÐ¾" in text:
            # ÐÐ·Ð²Ð»ÐµÑÐµÐ½Ð¸Ðµ Ð·Ð°Ð¿ÑÐ¾ÑÐ°
            query = text.replace("Ð½Ð°Ð¹Ð´Ð¸ Ð½Ð¾Ð²Ð¾ÑÑÐ¸ Ð¿ÑÐ¾", "").replace("Ð½Ð¾Ð²Ð¾ÑÑÐ¸ Ð¿ÑÐ¾", "").replace("Ð½Ð°Ð¹Ð´Ð¸", "").strip()
            if query:
                news = self.news_module.search_news(query)
                message = self.news_module.format_news_message(news)
                return {"status": "ok", "message": message, "data": news}
        
        # ÐÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¸
        if "ÑÐµÑÐ½Ð¾Ð»Ð¾Ð³" in text or "tech" in text:
            news = self.news_module.get_tech_news()
        elif "Ð±Ð¸Ð·Ð½ÐµÑ" in text or "ÑÐ¸Ð½Ð°Ð½Ñ" in text or "ÑÐºÐ¾Ð½Ð¾Ð¼" in text:
            news = self.news_module.get_business_news()
        elif "ÑÐ¿Ð¾ÑÑ" in text:
            news = self.news_module.get_sports_news()
        else:
            news = self.news_module.get_top_headlines()
        
        message = self.news_module.format_news_message(news)
        return {"status": "ok", "message": message, "data": news}

    def _handle_learning_command(self, text: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ."""
        if not self.learning_manager or not self.learning_manager.adaptive_ml:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ñ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        
        return {
            "status": "ok",
            "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð¿ÑÐ¸Ð½ÑÑÐ°"
        }

    def _handle_alias_command(self, text: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð°Ð»Ð¸Ð°ÑÐ¾Ð²."""
        if not self.learning_manager or not self.learning_manager.alias_system:
            return {"status": "error", "message": "Ð¡Ð¸ÑÑÐµÐ¼Ð° Ð°Ð»Ð¸Ð°ÑÐ¾Ð² Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°"}
        
        return {
            "status": "ok",
            "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð°Ð»Ð¸Ð°ÑÐ° Ð¿ÑÐ¸Ð½ÑÑÐ°"
        }

    def _get_learning_status(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ ÑÑÐ°ÑÑÑÐ° Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ."""
        if not self.learning_manager:
            return {"status": "error", "message": "ÐÐ¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ"}
        
        return self.learning_manager.get_learning_status()

    def start(self):
        """ÐÐ°Ð¿ÑÑÐº JARVIS."""
        self.logger.info("ÐÐ°Ð¿ÑÑÐº JARVIS...")
        self.running = True
        
        # ÐÑÐ¸Ð²ÐµÑÑÑÐ²Ð¸Ðµ
        if self.learning_manager:
            greeting = self.learning_manager.get_greeting()
            self.logger.info(greeting)
        else:
            greeting = "ÐÐ´ÑÐ°Ð²ÑÑÐ²ÑÐ¹ÑÐµ, ÑÑÑ. JARVIS Ð³Ð¾ÑÐ¾Ð² Ðº ÑÐ°Ð±Ð¾ÑÐµ."
            self.logger.info(greeting)
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ HUD
        if self.hud:
            self.hud.set_status("ONLINE")
        
        # ÐÐ²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº wake word ÑÐµÑÐ²Ð¸ÑÐ° ÐµÑÐ»Ð¸ Ð²ÐºÐ»ÑÑÐµÐ½
        if self.wake_word_service and self.config.get("windows.wake_word_enabled", False):
            self.wake_word_service.start(callback=self._on_wake_word)
        
        # ÐÐºÐ»ÑÑÐµÐ½Ð¸Ðµ ÑÐ¸ÑÑÐ¾Ð³Ð¾ ÑÐµÐ¶Ð¸Ð¼Ð° ÐµÑÐ»Ð¸ Ð½Ð°ÑÑÑÐ¾ÐµÐ½Ð¾
        if self.clean_desktop and self.config.get("windows.clean_desktop_on_start", False):
            self.clean_desktop.enable_clean_mode()
        
        # ÐÑÐ±Ð»Ð¸ÐºÐ°ÑÐ¸Ñ ÑÐ¾Ð±ÑÑÐ¸Ñ Ð·Ð°Ð¿ÑÑÐºÐ°
        self.event_bus.publish("jarvis_started", {"timestamp": "now"})

    def _on_wake_word(self, text: str):
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÑÐ¸Ðº wake word."""
        self.logger.info(f"Wake word Ð°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½: {text}")
        
        if self.hud:
            self.hud.set_status("LISTENING")
            self.hud.set_voice_active(True)

    def stop(self):
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° JARVIS."""
        self.logger.info("ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° JARVIS...")
        self.running = False
        
        if self.wake_word_service and self.wake_word_service.is_running():
            self.wake_word_service.stop()
        
        if self.clean_desktop and self.clean_desktop.is_hidden():
            self.clean_desktop.disable_clean_mode()
        
        self.event_bus.publish("jarvis_stopped", {"timestamp": "now"})

    def get_status(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ ÑÑÐ°ÑÑÑÐ° ÑÐ¸ÑÑÐµÐ¼Ñ."""
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
