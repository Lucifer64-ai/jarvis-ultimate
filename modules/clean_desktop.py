"""
Clean Desktop Mode - Ð¡ÐºÑÑÑÐ¸Ðµ Ð¸ÐºÐ¾Ð½Ð¾Ðº ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°
"""

import ctypes
import win32gui
import win32con
from typing import Dict, Optional
import logging


class CleanDesktop:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð²Ð¸Ð´Ð¸Ð¼Ð¾ÑÑÑÑ Ð¸ÐºÐ¾Ð½Ð¾Ðº ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.icons_hidden = False

    def hide_icons(self) -> Dict:
        """Ð¡ÐºÑÑÑÑ Ð²ÑÐµ Ð¸ÐºÐ¾Ð½ÐºÐ¸ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°."""
        try:
            # ÐÐ¾Ð»ÑÑÐ°ÐµÐ¼ Ð¾ÐºÐ½Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°
            progman = win32gui.FindWindow("Progman", None)
            defview = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
            sys_listview = win32gui.FindWindowEx(defview, 0, "SysListView32", None)
            
            if sys_listview:
                # Ð¡ÐºÑÑÐ²Ð°ÐµÐ¼ Ð¾ÐºÐ½Ð¾ Ñ Ð¸ÐºÐ¾Ð½ÐºÐ°Ð¼Ð¸
                win32gui.ShowWindow(sys_listview, win32con.SW_HIDE)
                self.icons_hidden = True
                self.logger.info("ÐÐºÐ¾Ð½ÐºÐ¸ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð° ÑÐºÑÑÑÑ")
                return {"status": "ok", "message": "ÐÐºÐ¾Ð½ÐºÐ¸ ÑÐºÑÑÑÑ. Ð Ð°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð» ÑÐ¸ÑÑ."}
            else:
                return {"status": "error", "message": "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð½Ð°Ð¹ÑÐ¸ Ð¾ÐºÐ½Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐºÑÑÑÐ¸Ñ Ð¸ÐºÐ¾Ð½Ð¾Ðº: {e}")
            return {"status": "error", "message": str(e)}

    def show_icons(self) -> Dict:
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ Ð¸ÐºÐ¾Ð½ÐºÐ¸ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°."""
        try:
            progman = win32gui.FindWindow("Progman", None)
            defview = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
            sys_listview = win32gui.FindWindowEx(defview, 0, "SysListView32", None)
            
            if sys_listview:
                win32gui.ShowWindow(sys_listview, win32con.SW_SHOW)
                self.icons_hidden = False
                self.logger.info("ÐÐºÐ¾Ð½ÐºÐ¸ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð° Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½Ñ")
                return {"status": "ok", "message": "ÐÐºÐ¾Ð½ÐºÐ¸ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½Ñ."}
            else:
                return {"status": "error", "message": "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð½Ð°Ð¹ÑÐ¸ Ð¾ÐºÐ½Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾ÐºÐ°Ð·Ð° Ð¸ÐºÐ¾Ð½Ð¾Ðº: {e}")
            return {"status": "error", "message": str(e)}

    def toggle_icons(self) -> Dict:
        """ÐÐµÑÐµÐºÐ»ÑÑÐ¸ÑÑ Ð²Ð¸Ð´Ð¸Ð¼Ð¾ÑÑÑ Ð¸ÐºÐ¾Ð½Ð¾Ðº."""
        if self.icons_hidden:
            return self.show_icons()
        else:
            return self.hide_icons()

    def is_hidden(self) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ, ÑÐºÑÑÑÑ Ð»Ð¸ Ð¸ÐºÐ¾Ð½ÐºÐ¸."""
        return self.icons_hidden

    def hide_taskbar(self) -> Dict:
        """Ð¡ÐºÑÑÑÑ Ð¿Ð°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ."""
        try:
            taskbar = win32gui.FindWindow("Shell_traywnd", None)
            if taskbar:
                win32gui.ShowWindow(taskbar, win32con.SW_HIDE)
                self.logger.info("ÐÐ°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ ÑÐºÑÑÑÐ°")
                return {"status": "ok", "message": "ÐÐ°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ ÑÐºÑÑÑÐ°."}
            return {"status": "error", "message": "ÐÐ°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐºÑÑÑÐ¸Ñ Ð¿Ð°Ð½ÐµÐ»Ð¸ Ð·Ð°Ð´Ð°Ñ: {e}")
            return {"status": "error", "message": str(e)}

    def show_taskbar(self) -> Dict:
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ Ð¿Ð°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ."""
        try:
            taskbar = win32gui.FindWindow("Shell_traywnd", None)
            if taskbar:
                win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
                self.logger.info("ÐÐ°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½Ð°")
                return {"status": "ok", "message": "ÐÐ°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½Ð°."}
            return {"status": "error", "message": "ÐÐ°Ð½ÐµÐ»Ñ Ð·Ð°Ð´Ð°Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾ÐºÐ°Ð·Ð° Ð¿Ð°Ð½ÐµÐ»Ð¸ Ð·Ð°Ð´Ð°Ñ: {e}")
            return {"status": "error", "message": str(e)}

    def enable_clean_mode(self) -> Dict:
        """ÐÐºÐ»ÑÑÐ¸ÑÑ ÑÐµÐ¶Ð¸Ð¼ ÑÐ¸ÑÑÐ¾Ð³Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°."""
        result1 = self.hide_icons()
        result2 = self.hide_taskbar()
        
        if result1["status"] == "ok" and result2["status"] == "ok":
            return {"status": "ok", "message": "Ð ÐµÐ¶Ð¸Ð¼ ÑÐ¸ÑÑÐ¾Ð³Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð° Ð²ÐºÐ»ÑÑÐµÐ½. ÐÑÐ¿Ð¾Ð»ÑÐ·ÑÐ¹ÑÐµ JARVIS Ð´Ð»Ñ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ñ."}
        else:
            return {"status": "partial", "message": "Ð§Ð°ÑÑÐ¸ÑÐ½Ð¾ Ð²ÐºÐ»ÑÑÐµÐ½Ð¾", "icons": result1, "taskbar": result2}

    def disable_clean_mode(self) -> Dict:
        """ÐÑÐºÐ»ÑÑÐ¸ÑÑ ÑÐµÐ¶Ð¸Ð¼ ÑÐ¸ÑÑÐ¾Ð³Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°."""
        result1 = self.show_icons()
        result2 = self.show_taskbar()
        
        if result1["status"] == "ok" and result2["status"] == "ok":
            return {"status": "ok", "message": "Ð ÐµÐ¶Ð¸Ð¼ ÑÐ¸ÑÑÐ¾Ð³Ð¾ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð° Ð¾ÑÐºÐ»ÑÑÐµÐ½."}
        else:
            return {"status": "partial", "message": "Ð§Ð°ÑÑÐ¸ÑÐ½Ð¾ Ð¾ÑÐºÐ»ÑÑÐµÐ½Ð¾", "icons": result1, "taskbar": result2}
