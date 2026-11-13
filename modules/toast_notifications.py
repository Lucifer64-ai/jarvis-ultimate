"""
Windows Toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ
"""

from typing import Dict, Optional
import logging


class ToastNotifications:
    """ÐÐ°ÑÐ¸Ð²Ð½ÑÐµ Windows ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.app_name = "JARVIS"

    def show_toast(self, title: str, message: str, icon: str = None) -> Dict:
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ toast ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ðµ."""
        try:
            from win10toast import ToastNotifier
            
            toaster = ToastNotifier()
            toaster.show_toast(
                title,
                message,
                icon_path=icon,
                duration=5,
                threaded=True
            )
            
            self.logger.info(f"Toast: {title} - {message}")
            return {"status": "ok", "message": "Ð£Ð²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ðµ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½Ð¾"}
        
        except ImportError:
            self.logger.warning("win10toast Ð½Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½. Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÐµ: pip install win10toast")
            return {"status": "error", "message": "win10toast Ð½Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾ÐºÐ°Ð·Ð° ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ñ: {e}")
            return {"status": "error", "message": str(e)}

    def show_info(self, message: str) -> Dict:
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¾Ð½Ð½Ð¾Ðµ ÑÐ²ÐµÐ´Ð¾Ð¼Ð»ÐµÐ½Ð¸Ðµ."""
        return self.show_toast("JARVIS", message)

    def show_warning(self, message: str) -> Dict:
        """ÐÑÐµÐ´ÑÐ¿ÑÐµÐ¶Ð´ÐµÐ½Ð¸Ðµ."""
        return self.show_toast("JARVIS - ÐÑÐµÐ´ÑÐ¿ÑÐµÐ¶Ð´ÐµÐ½Ð¸Ðµ", message)

    def show_error(self, message: str) -> Dict:
        """ÐÑÐ¸Ð±ÐºÐ°."""
        return self.show_toast("JARVIS - ÐÑÐ¸Ð±ÐºÐ°", message)

    def show_success(self, message: str) -> Dict:
        """Ð£ÑÐ¿ÐµÑ."""
        return self.show_toast("JARVIS - Ð£ÑÐ¿ÐµÑÐ½Ð¾", message)
