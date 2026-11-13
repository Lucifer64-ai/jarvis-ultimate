"""Safe, allowlisted desktop controls for JARVIS.

Only fixed keyboard shortcuts and system controls are exposed. Laptop Fn-key
layers are handled by firmware/vendor software and generally cannot be emitted
as a normal software key; F1-F12 are exposed as standard keys instead.
"""

from typing import Dict


class DesktopControlModule:
    """Basic keyboard and system controls for the local interactive desktop."""

    def __init__(self, brain):
        self.brain = brain

    @staticmethod
    def _pyautogui():
        try:
            import pyautogui
            return pyautogui
        except Exception as error:
            raise RuntimeError(
                "Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ°Ð±Ð¾ÑÐ¸Ð¼ ÑÑÐ¾Ð»Ð¾Ð¼ Ð½ÐµÐ´Ð¾ÑÑÑÐ¿Ð½Ð¾; Ð¿ÑÐ¾Ð²ÐµÑÑÑÐµ ÑÑÑÐ°Ð½Ð¾Ð²ÐºÑ pyautogui Ð¸ Ð°ÐºÑÐ¸Ð²Ð½ÑÑ ÑÐµÑÑÐ¸Ñ"
            ) from error

    def minimize_all(self) -> Dict:
        try:
            self._pyautogui().hotkey("win", "d")
            return {"status": "ok", "message": "ÐÐ¾ÐºÐ°Ð·Ð°Ð½ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def show_desktop(self) -> Dict:
        return self.minimize_all()

    def volume_up(self, steps: int = 3) -> Dict:
        return self._volume_key("volumeup", steps, "ÐÑÐ¾Ð¼ÐºÐ¾ÑÑÑ ÑÐ²ÐµÐ»Ð¸ÑÐµÐ½Ð°")

    def volume_down(self, steps: int = 3) -> Dict:
        return self._volume_key("volumedown", steps, "ÐÑÐ¾Ð¼ÐºÐ¾ÑÑÑ ÑÐ¼ÐµÐ½ÑÑÐµÐ½Ð°")

    def _volume_key(self, key: str, steps: int, message: str) -> Dict:
        try:
            count = max(1, min(int(steps), 10))
            self._pyautogui().press(key, presses=count, interval=0.05)
            return {"status": "ok", "message": message}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def mute(self) -> Dict:
        try:
            self._pyautogui().press("volumemute")
            return {"status": "ok", "message": "ÐÐ²ÑÐº Ð¿ÐµÑÐµÐºÐ»ÑÑÑÐ½"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def lock_screen(self) -> Dict:
        try:
            import ctypes
            if not hasattr(ctypes, "windll"):
                return {"status": "error", "message": "ÐÐ»Ð¾ÐºÐ¸ÑÐ¾Ð²ÐºÐ° ÑÐºÑÐ°Ð½Ð° Ð¿Ð¾Ð´Ð´ÐµÑÐ¶Ð¸Ð²Ð°ÐµÑÑÑ ÑÐ¾Ð»ÑÐºÐ¾ Ð² Windows"}
            ctypes.windll.user32.LockWorkStation()
            return {"status": "ok", "message": "Ð­ÐºÑÐ°Ð½ Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÐ¾Ð²Ð°Ð½"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def shortcut(self, name: str) -> Dict:
        """Execute a supported non-destructive keyboard shortcut."""
        shortcuts = {
            "copy": ("ctrl", "c"),
            "paste": ("ctrl", "v"),
            "undo": ("ctrl", "z"),
            "select_all": ("ctrl", "a"),
            "print_screen": ("printscreen",),
            "snipping_tool": ("win", "shift", "s"),
            "num_lock": ("numlock",),
            "escape": ("esc",),
            "alt_tab": ("alt", "tab"),
            "task_manager": ("ctrl", "shift", "esc"),
            "refresh": ("f5",),
            "f1": ("f1",), "f2": ("f2",), "f3": ("f3",),
            "f4": ("f4",), "f5": ("f5",), "f6": ("f6",),
            "f7": ("f7",), "f8": ("f8",), "f9": ("f9",),
            "f10": ("f10",), "f11": ("f11",), "f12": ("f12",),
        }
        keys = shortcuts.get(name)
        if not keys:
            return {"status": "error", "message": "Ð­ÑÐ° ÐºÐ¾Ð¼Ð±Ð¸Ð½Ð°ÑÐ¸Ñ ÐºÐ»Ð°Ð²Ð¸Ñ Ð½Ðµ ÑÐ°Ð·ÑÐµÑÐµÐ½Ð°"}
        try:
            pyautogui = self._pyautogui()
            if len(keys) == 1:
                pyautogui.press(keys[0])
            else:
                pyautogui.hotkey(*keys)
            return {"status": "ok", "message": f"ÐÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð° ÐºÐ¾Ð¼Ð°Ð½Ð´Ð° ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ: {name}"}
        except Exception as error:
            return {"status": "error", "message": str(error)}
