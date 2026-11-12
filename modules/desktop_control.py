"""Safe, allowlisted desktop controls for JARVIS.

This module deliberately exposes only fixed actions (volume, desktop/window
shortcuts and screen lock); it does not accept or execute arbitrary shell input.
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
            raise RuntimeError("Управление рабочим столом недоступно; проверьте установку pyautogui и активную сессию") from error

    def minimize_all(self) -> Dict:
        try:
            self._pyautogui().hotkey("win", "d")
            return {"status": "ok", "message": "Показан рабочий стол"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def show_desktop(self) -> Dict:
        return self.minimize_all()

    def volume_up(self, steps: int = 3) -> Dict:
        return self._volume_key("volumeup", steps, "Громкость увеличена")

    def volume_down(self, steps: int = 3) -> Dict:
        return self._volume_key("volumedown", steps, "Громкость уменьшена")

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
            return {"status": "ok", "message": "Звук переключён"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def lock_screen(self) -> Dict:
        try:
            import ctypes
            if not hasattr(ctypes, "windll"):
                return {"status": "error", "message": "Блокировка экрана поддерживается только в Windows"}
            ctypes.windll.user32.LockWorkStation()
            return {"status": "ok", "message": "Экран заблокирован"}
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def shortcut(self, name: str) -> Dict:
        """Run a small allowlist of common, non-destructive shortcuts."""
        shortcuts = {
            "copy": ("ctrl", "c"),
            "paste": ("ctrl", "v"),
            "undo": ("ctrl", "z"),
            "select_all": ("ctrl", "a"),
        }
        keys = shortcuts.get(name)
        if not keys:
            return {"status": "error", "message": "Эта комбинация клавиш не разрешена"}
        try:
            self._pyautogui().hotkey(*keys)
            return {"status": "ok", "message": "Комбинация клавиш выполнена"}
        except Exception as error:
            return {"status": "error", "message": str(error)}
