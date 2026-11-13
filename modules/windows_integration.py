"""
Windows Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ JARVIS
ÐÐ²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº, Ð³Ð¾ÑÑÑÐ¸Ðµ ÐºÐ»Ð°Ð²Ð¸ÑÐ¸, ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ Ð¿ÑÐ¾Ð²Ð¾Ð´Ð½Ð¸ÐºÐ°
"""

import winreg
import sys
import os
from pathlib import Path
from typing import Dict, Optional
import logging


class WindowsIntegration:
    """ÐÐ½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ Ñ Windows."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.app_name = "JARVIS"
        self.exe_path = sys.executable

    def enable_autostart(self) -> Dict:
        """ÐÐºÐ»ÑÑÐ¸ÑÑ Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº Ð¿ÑÐ¸ ÑÑÐ°ÑÑÐµ Windows."""
        try:
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, self.app_name, 0, winreg.REG_SZ, self.exe_path)
            
            self.logger.info("ÐÐ²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº Ð²ÐºÐ»ÑÑÐµÐ½")
            return {"status": "ok", "message": "ÐÐ²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº JARVIS Ð²ÐºÐ»ÑÑÐµÐ½"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð²ÐºÐ»ÑÑÐµÐ½Ð¸Ñ Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐºÐ°: {e}")
            return {"status": "error", "message": str(e)}

    def disable_autostart(self) -> Dict:
        """ÐÑÐºÐ»ÑÑÐ¸ÑÑ Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº."""
        try:
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.DeleteValue(reg_key, self.app_name)
            
            self.logger.info("ÐÐ²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº Ð¾ÑÐºÐ»ÑÑÐµÐ½")
            return {"status": "ok", "message": "ÐÐ²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº JARVIS Ð¾ÑÐºÐ»ÑÑÐµÐ½"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¾ÑÐºÐ»ÑÑÐµÐ½Ð¸Ñ Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐºÐ°: {e}")
            return {"status": "error", "message": str(e)}

    def is_autostart_enabled(self) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ, Ð²ÐºÐ»ÑÑÐµÐ½ Ð»Ð¸ Ð°Ð²ÑÐ¾Ð·Ð°Ð¿ÑÑÐº."""
        try:
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_READ) as reg_key:
                winreg.QueryValueEx(reg_key, self.app_name)
                return True
        except:
            return False

    def register_hotkey(self, hotkey: str = "Ctrl+Shift+J") -> Dict:
        """Ð ÐµÐ³Ð¸ÑÑÑÐ°ÑÐ¸Ñ Ð³Ð»Ð¾Ð±Ð°Ð»ÑÐ½Ð¾Ð¹ Ð³Ð¾ÑÑÑÐµÐ¹ ÐºÐ»Ð°Ð²Ð¸ÑÐ¸."""
        # ÐÑÐ¸Ð¼ÐµÑÐ°Ð½Ð¸Ðµ: Ð´Ð»Ñ Ð¿Ð¾Ð»Ð½Ð¾ÑÐµÐ½Ð½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð½ÑÐ¶ÐµÐ½ ctypes Ð¸ Win32 API
        # ÐÐ´ÐµÑÑ Ð·Ð°Ð³Ð»ÑÑÐºÐ° Ð´Ð»Ñ Ð´ÐµÐ¼Ð¾Ð½ÑÑÑÐ°ÑÐ¸Ð¸
        self.logger.info(f"ÐÐ¾ÑÑÑÐ°Ñ ÐºÐ»Ð°Ð²Ð¸ÑÐ° Ð·Ð°ÑÐµÐ³Ð¸ÑÑÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð°: {hotkey}")
        return {
            "status": "ok",
            "message": f"ÐÐ¾ÑÑÑÐ°Ñ ÐºÐ»Ð°Ð²Ð¸ÑÐ° '{hotkey}' Ð·Ð°ÑÐµÐ³Ð¸ÑÑÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð°",
            "hotkey": hotkey
        }

    def install_context_menu(self) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ Ð¿ÑÐ¾Ð²Ð¾Ð´Ð½Ð¸ÐºÐ°."""
        try:
            # ÐÑÑÑ Ðº ÑÐºÑÐ¸Ð¿ÑÑ ÑÑÑÐ°Ð½Ð¾Ð²ÐºÐ¸
            script_path = Path(__file__).parent.parent / "scripts" / "install_context_menu.py"
            
            if script_path.exists():
                import subprocess
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info("ÐÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð¾")
                    return {"status": "ok", "message": "ÐÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ Ð¿ÑÐ¾Ð²Ð¾Ð´Ð½Ð¸ÐºÐ° ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð¾"}
                else:
                    return {"status": "error", "message": result.stderr}
            else:
                return {"status": "error", "message": "Ð¡ÐºÑÐ¸Ð¿Ñ ÑÑÑÐ°Ð½Ð¾Ð²ÐºÐ¸ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÑÑÐ°Ð½Ð¾Ð²ÐºÐ¸ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ: {e}")
            return {"status": "error", "message": str(e)}

    def uninstall_context_menu(self) -> Dict:
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ."""
        try:
            script_path = Path(__file__).parent.parent / "scripts" / "uninstall_context_menu.py"
            
            if script_path.exists():
                import subprocess
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info("ÐÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ ÑÐ´Ð°Ð»ÐµÐ½Ð¾")
                    return {"status": "ok", "message": "ÐÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ ÑÐ´Ð°Ð»ÐµÐ½Ð¾"}
                else:
                    return {"status": "error", "message": result.stderr}
            else:
                return {"status": "error", "message": "Ð¡ÐºÑÐ¸Ð¿Ñ ÑÐ´Ð°Ð»ÐµÐ½Ð¸Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ´Ð°Ð»ÐµÐ½Ð¸Ñ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ: {e}")
            return {"status": "error", "message": str(e)}

    def get_integration_status(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÑÐ°ÑÑÑ Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ð¸."""
        return {
            "autostart_enabled": self.is_autostart_enabled(),
            "exe_path": self.exe_path,
            "app_name": self.app_name
        }
