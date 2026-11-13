"""
ÃÂ¡ÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂ¹ JARVIS
"""

from plyer import notification
from typing import Optional
import threading


class NotificationManager:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÃÂ¼ÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain

    def show(self, title: str, message: str, timeout: int = 10):
        """ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="JARVIS",
                timeout=timeout
            )
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¿ÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ° ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã: {e}")

    def show_async(self, title: str, message: str, timeout: int = 10):
        """ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ ÃÃÂ²ÃÂµÃÂ´ÃÂ¾ÃÂ¼ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ°ÃÃÂ¸ÃÂ½ÃÃÃÂ¾ÃÂ½ÃÂ½ÃÂ¾."""
        thread = threading.Thread(
            target=self.show,
            args=(title, message, timeout),
            daemon=True
        )
        thread.start()

    def alert(self, message: str, level: str = "info"):
        """ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ ÃÂ¿ÃÃÂµÃÂ´ÃÃÂ¿ÃÃÂµÃÂ¶ÃÂ´ÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        icons = {
            "info": "Ã¢Â¹Ã¯Â¸",
            "warning": "Ã¢Â Ã¯Â¸",
            "error": "Ã¢",
            "success": "Ã¢"
        }
        icon = icons.get(level, "Ã¢Â¹Ã¯Â¸")
        self.show(f"{icon} JARVIS", message)
