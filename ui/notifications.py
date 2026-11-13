"""
ÃÃÂ¡ÃÃÂ¸ÃÃÃÃÂµÃÃÂ¼ÃÃÂ° ÃÃÃÂ²ÃÃÂµÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂ¹ JARVIS
"""

from plyer import notification
from typing import Optional
import threading


class NotificationManager:
    """ÃÃÂ£ÃÃÂ¿ÃÃÃÂ°ÃÃÂ²ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÃÂ²ÃÃÂµÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÃÂ¼ÃÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain

    def show(self, title: str, message: str, timeout: int = 10):
        """ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ ÃÃÃÂ²ÃÃÂµÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ."""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="JARVIS",
                timeout=timeout
            )
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÂ¿ÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ° ÃÃÃÂ²ÃÃÂµÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸Ã: {e}")

    def show_async(self, title: str, message: str, timeout: int = 10):
        """ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ ÃÃÃÂ²ÃÃÂµÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ°ÃÃÃÂ¸ÃÃÂ½ÃÃÃÃÂ¾ÃÃÂ½ÃÃÂ½ÃÃÂ¾."""
        thread = threading.Thread(
            target=self.show,
            args=(title, message, timeout),
            daemon=True
        )
        thread.start()

    def alert(self, message: str, level: str = "info"):
        """ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ ÃÃÂ¿ÃÃÃÂµÃÃÂ´ÃÃÃÂ¿ÃÃÃÂµÃÃÂ¶ÃÃÂ´ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ."""
        icons = {
            "info": "ÃÂ¢ÃÂ¹ÃÂ¯ÃÂ¸",
            "warning": "ÃÂ¢ÃÂ ÃÂ¯ÃÂ¸",
            "error": "ÃÂ¢",
            "success": "ÃÂ¢"
        }
        icon = icons.get(level, "ÃÂ¢ÃÂ¹ÃÂ¯ÃÂ¸")
        self.show(f"{icon} JARVIS", message)
