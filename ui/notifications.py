"""
Ð¡Ð¸ÑÑÐµÐ¼Ð° ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ð¹ JARVIS
"""

from plyer import notification
from typing import Optional
import threading


class NotificationManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸ÑÐ¼Ð¸."""

    def __init__(self, brain):
        self.brain = brain

    def show(self, title: str, message: str, timeout: int = 10):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ðµ."""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="JARVIS",
                timeout=timeout
            )
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾ÐºÐ°Ð·Ð° ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ: {e}")

    def show_async(self, title: str, message: str, timeout: int = 10):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ðµ Ð°ÑÐ¸Ð½ÑÑÐ¾Ð½Ð½Ð¾."""
        thread = threading.Thread(
            target=self.show,
            args=(title, message, timeout),
            daemon=True
        )
        thread.start()

    def alert(self, message: str, level: str = "info"):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ Ð¿ÑÐµÐ´ÑÐ¿ÑÐµÐ¶Ð´ÐµÐ½Ð¸Ðµ."""
        icons = {
            "info": "â¹ï¸",
            "warning": "â ï¸",
            "error": "â",
            "success": "â"
        }
        icon = icons.get(level, "â¹ï¸")
        self.show(f"{icon} JARVIS", message)
