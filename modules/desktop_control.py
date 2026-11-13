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
                "ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂ¸ÃÂ¼ ÃÃÃÂ¾ÃÂ»ÃÂ¾ÃÂ¼ ÃÂ½ÃÂµÃÂ´ÃÂ¾ÃÃÃÃÂ¿ÃÂ½ÃÂ¾; ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÃÃÂµ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃ pyautogui ÃÂ¸ ÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂ½ÃÃ ÃÃÂµÃÃÃÂ¸Ã"
            ) from error

    def minimize_all(self) -> Dict:
        try:
            self._pyautogui().hotkey("win", "d")
            return {"status": "ok", "message": "ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÂ½ ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂ¸ÃÂ¹ ÃÃÃÂ¾ÃÂ»"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def show_desktop(self) -> Dict:
        return self.minimize_all()

    def volume_up(self, steps: int = 3) -> Dict:
        return self._volume_key("volumeup", steps, "ÃÃÃÂ¾ÃÂ¼ÃÂºÃÂ¾ÃÃÃ ÃÃÂ²ÃÂµÃÂ»ÃÂ¸ÃÃÂµÃÂ½ÃÂ°")

    def volume_down(self, steps: int = 3) -> Dict:
        return self._volume_key("volumedown", steps, "ÃÃÃÂ¾ÃÂ¼ÃÂºÃÂ¾ÃÃÃ ÃÃÂ¼ÃÂµÃÂ½ÃÃÃÂµÃÂ½ÃÂ°")

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
            return {"status": "ok", "message": "ÃÃÂ²ÃÃÂº ÃÂ¿ÃÂµÃÃÂµÃÂºÃÂ»ÃÃÃÃÂ½"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def lock_screen(self) -> Dict:
        try:
            import ctypes
            if not hasattr(ctypes, "windll"):
                return {"status": "error", "message": "ÃÃÂ»ÃÂ¾ÃÂºÃÂ¸ÃÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÃÂºÃÃÂ°ÃÂ½ÃÂ° ÃÂ¿ÃÂ¾ÃÂ´ÃÂ´ÃÂµÃÃÂ¶ÃÂ¸ÃÂ²ÃÂ°ÃÂµÃÃÃ ÃÃÂ¾ÃÂ»ÃÃÂºÃÂ¾ ÃÂ² Windows"}
            ctypes.windll.user32.LockWorkStation()
            return {"status": "ok", "message": "ÃÂ­ÃÂºÃÃÂ°ÃÂ½ ÃÂ·ÃÂ°ÃÂ±ÃÂ»ÃÂ¾ÃÂºÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½"}
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
            return {"status": "error", "message": "ÃÂ­ÃÃÂ° ÃÂºÃÂ¾ÃÂ¼ÃÂ±ÃÂ¸ÃÂ½ÃÂ°ÃÃÂ¸Ã ÃÂºÃÂ»ÃÂ°ÃÂ²ÃÂ¸Ã ÃÂ½ÃÂµ ÃÃÂ°ÃÂ·ÃÃÂµÃÃÂµÃÂ½ÃÂ°"}
        try:
            pyautogui = self._pyautogui()
            if len(keys) == 1:
                pyautogui.press(keys[0])
            else:
                pyautogui.hotkey(*keys)
            return {"status": "ok", "message": f"ÃÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂµÃÂ½ÃÂ° ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ° ÃÂºÃÂ»ÃÂ°ÃÂ²ÃÂ¸ÃÂ°ÃÃÃÃ: {name}"}
        except Exception as error:
            return {"status": "error", "message": str(error)}
