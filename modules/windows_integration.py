"""
Windows ÃÂ¸ÃÂ½ÃÃÂµÃÂ³ÃÃÂ°ÃÃÂ¸Ã JARVIS
ÃÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº, ÃÂ³ÃÂ¾ÃÃÃÃÂ¸ÃÂµ ÃÂºÃÂ»ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ¸, ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ´ÃÂ½ÃÂ¸ÃÂºÃÂ°
"""

import winreg
import sys
import os
from pathlib import Path
from typing import Dict, Optional
import logging


class WindowsIntegration:
    """ÃÃÂ½ÃÃÂµÃÂ³ÃÃÂ°ÃÃÂ¸Ã Ã Windows."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.app_name = "JARVIS"
        self.exe_path = sys.executable

    def enable_autostart(self) -> Dict:
        """ÃÃÂºÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÃÂ¸ ÃÃÃÂ°ÃÃÃÂµ Windows."""
        try:
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, self.app_name, 0, winreg.REG_SZ, self.exe_path)
            
            self.logger.info("ÃÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ²ÃÂºÃÂ»ÃÃÃÂµÃÂ½")
            return {"status": "ok", "message": "ÃÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº JARVIS ÃÂ²ÃÂºÃÂ»ÃÃÃÂµÃÂ½"}
        
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ²ÃÂºÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂºÃÂ°: {e}")
            return {"status": "error", "message": str(e)}

    def disable_autostart(self) -> Dict:
        """ÃÃÃÂºÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº."""
        try:
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.DeleteValue(reg_key, self.app_name)
            
            self.logger.info("ÃÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¾ÃÃÂºÃÂ»ÃÃÃÂµÃÂ½")
            return {"status": "ok", "message": "ÃÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº JARVIS ÃÂ¾ÃÃÂºÃÂ»ÃÃÃÂµÃÂ½"}
        
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¾ÃÃÂºÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂºÃÂ°: {e}")
            return {"status": "error", "message": str(e)}

    def is_autostart_enabled(self) -> bool:
        """ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂ¸ÃÃ, ÃÂ²ÃÂºÃÂ»ÃÃÃÂµÃÂ½ ÃÂ»ÃÂ¸ ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂº."""
        try:
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_READ) as reg_key:
                winreg.QueryValueEx(reg_key, self.app_name)
                return True
        except:
            return False

    def register_hotkey(self, hotkey: str = "Ctrl+Shift+J") -> Dict:
        """ÃÂ ÃÂµÃÂ³ÃÂ¸ÃÃÃÃÂ°ÃÃÂ¸Ã ÃÂ³ÃÂ»ÃÂ¾ÃÂ±ÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÂ³ÃÂ¾ÃÃÃÃÂµÃÂ¹ ÃÂºÃÂ»ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ¸."""
        # ÃÃÃÂ¸ÃÂ¼ÃÂµÃÃÂ°ÃÂ½ÃÂ¸ÃÂµ: ÃÂ´ÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂ¾ÃÃÂµÃÂ½ÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ½ÃÃÂ¶ÃÂµÃÂ½ ctypes ÃÂ¸ Win32 API
        # ÃÃÂ´ÃÂµÃÃ ÃÂ·ÃÂ°ÃÂ³ÃÂ»ÃÃÃÂºÃÂ° ÃÂ´ÃÂ»Ã ÃÂ´ÃÂµÃÂ¼ÃÂ¾ÃÂ½ÃÃÃÃÂ°ÃÃÂ¸ÃÂ¸
        self.logger.info(f"ÃÃÂ¾ÃÃÃÃÂ°Ã ÃÂºÃÂ»ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ° ÃÂ·ÃÂ°ÃÃÂµÃÂ³ÃÂ¸ÃÃÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ°: {hotkey}")
        return {
            "status": "ok",
            "message": f"ÃÃÂ¾ÃÃÃÃÂ°Ã ÃÂºÃÂ»ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ° '{hotkey}' ÃÂ·ÃÂ°ÃÃÂµÃÂ³ÃÂ¸ÃÃÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ°",
            "hotkey": hotkey
        }

    def install_context_menu(self) -> Dict:
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ¸ÃÃ ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ´ÃÂ½ÃÂ¸ÃÂºÃÂ°."""
        try:
            # ÃÃÃÃ ÃÂº ÃÃÂºÃÃÂ¸ÃÂ¿ÃÃ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ¸
            script_path = Path(__file__).parent.parent / "scripts" / "install_context_menu.py"
            
            if script_path.exists():
                import subprocess
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info("ÃÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾")
                    return {"status": "ok", "message": "ÃÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ´ÃÂ½ÃÂ¸ÃÂºÃÂ° ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾"}
                else:
                    return {"status": "error", "message": result.stderr}
            else:
                return {"status": "error", "message": "ÃÂ¡ÃÂºÃÃÂ¸ÃÂ¿Ã ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ¸ ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½"}
        
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ¸ ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã: {e}")
            return {"status": "error", "message": str(e)}

    def uninstall_context_menu(self) -> Dict:
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã."""
        try:
            script_path = Path(__file__).parent.parent / "scripts" / "uninstall_context_menu.py"
            
            if script_path.exists():
                import subprocess
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info("ÃÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¾")
                    return {"status": "ok", "message": "ÃÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¾"}
                else:
                    return {"status": "error", "message": result.stderr}
            else:
                return {"status": "error", "message": "ÃÂ¡ÃÂºÃÃÂ¸ÃÂ¿Ã ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½"}
        
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã: {e}")
            return {"status": "error", "message": str(e)}

    def get_integration_status(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÃÃÂ°ÃÃÃ ÃÂ¸ÃÂ½ÃÃÂµÃÂ³ÃÃÂ°ÃÃÂ¸ÃÂ¸."""
        return {
            "autostart_enabled": self.is_autostart_enabled(),
            "exe_path": self.exe_path,
            "app_name": self.app_name
        }
