"""
Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¾ÐºÐ½Ð°Ð¼Ð¸ JARVIS
"""

import win32gui
import win32con
from typing import Dict, List


class WindowModule:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¾ÐºÐ½Ð°Ð¼Ð¸ Windows."""

    def __init__(self, brain):
        self.brain = brain

    def list_windows(self) -> List[Dict]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð¾ÑÐºÑÑÑÑÑ Ð¾ÐºÐ¾Ð½."""
        windows = []

        def callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    results.append({
                        "hwnd": hwnd,
                        "title": title
                    })

        win32gui.EnumWindows(callback, windows)
        return windows

    def minimize_all(self) -> Dict:
        """Ð¡Ð²ÐµÑÐ½ÑÑÑ Ð²ÑÐµ Ð¾ÐºÐ½Ð°."""
        try:
            import pyautogui
            pyautogui.hotkey('win', 'd')
            return {"status": "ok", "message": "ÐÑÐµ Ð¾ÐºÐ½Ð° ÑÐ²ÑÑÐ½ÑÑÑ"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def show_desktop(self) -> Dict:
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»."""
        return self.minimize_all()

    def close_window(self, title: str) -> Dict:
        """ÐÐ°ÐºÑÑÑÑ Ð¾ÐºÐ½Ð¾ Ð¿Ð¾ Ð·Ð°Ð³Ð¾Ð»Ð¾Ð²ÐºÑ."""
        def callback(hwnd, target):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if target.lower() in window_title.lower():
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    return True
            return False

        try:
            win32gui.EnumWindows(lambda hwnd, _: callback(hwnd, title), None)
            return {"status": "ok", "message": f"ÐÐºÐ½Ð¾ '{title}' Ð·Ð°ÐºÑÑÑÐ¾"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
