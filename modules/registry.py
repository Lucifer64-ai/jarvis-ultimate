"""
Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐµÐµÑÑÑÐ¾Ð¼ Windows JARVIS
"""

import winreg
from typing import Dict, Optional


class RegistryModule:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐµÐµÑÑÑÐ¾Ð¼ Windows."""

    def __init__(self, brain):
        self.brain = brain

    def read_value(self, path: str, name: str) -> Dict:
        """ÐÑÐ¾ÑÐ¸ÑÐ°ÑÑ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ Ð¸Ð· ÑÐµÐµÑÑÑÐ°."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
            value, reg_type = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return {"status": "ok", "value": value, "type": reg_type}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def write_value(self, path: str, name: str, value, reg_type=winreg.REG_SZ) -> Dict:
        """ÐÐ°Ð¿Ð¸ÑÐ°ÑÑ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ Ð² ÑÐµÐµÑÑÑ."""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
            winreg.SetValueEx(key, name, 0, reg_type, value)
            winreg.CloseKey(key)
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_value(self, path: str, name: str) -> Dict:
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ Ð¸Ð· ÑÐµÐµÑÑÑÐ°."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
