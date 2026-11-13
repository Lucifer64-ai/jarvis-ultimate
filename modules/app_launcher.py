"""
App Launcher - ÐÐ°Ð¿ÑÑÐº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ ÑÐµÑÐµÐ· JARVIS
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging


class AppLauncher:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð·Ð°Ð¿ÑÑÐºÐ¾Ð¼ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.apps_file = Path("data/apps.json")
        self.apps_file.parent.mkdir(exist_ok=True)
        self.apps: Dict[str, str] = self._load_apps()

    def _load_apps(self) -> Dict[str, str]:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° ÑÐ¿Ð¸ÑÐºÐ° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        if self.apps_file.exists():
            with open(self.apps_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # ÐÐµÑÐ¾Ð»ÑÐ½ÑÐµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ
        return {
            "Ð±Ð»Ð¾ÐºÐ½Ð¾Ñ": "notepad.exe",
            "ÐºÐ°Ð»ÑÐºÑÐ»ÑÑÐ¾Ñ": "calc.exe",
            "Ð¿ÑÐ¾Ð²Ð¾Ð´Ð½Ð¸Ðº": "explorer.exe",
            "Ð±ÑÐ°ÑÐ·ÐµÑ": "chrome.exe",
            "ÑÑÐ¾Ð¼": "chrome.exe",
            "ÑÐ°Ð¹ÑÑÐ¾ÐºÑ": "firefox.exe",
            "edge": "msedge.exe",
            "ÑÐµÑÐ¼Ð¸Ð½Ð°Ð»": "cmd.exe",
            "ÐºÐ¾Ð¼Ð°Ð½Ð´Ð½Ð°Ñ ÑÑÑÐ¾ÐºÐ°": "cmd.exe",
            "powershell": "powershell.exe",
            "Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ¸": "ms-settings:",
            "Ð´Ð¸ÑÐ¿ÐµÑÑÐµÑ Ð·Ð°Ð´Ð°Ñ": "taskmgr.exe",
            "paint": "mspaint.exe",
            "ÑÐ¾ÑÐ¾Ð³ÑÐ°ÑÐ¸Ð¸": "ms-photos:",
            "Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½": "ms-windows-store:",
            "Ð¿Ð¾ÑÑÐ°": "outlookmail:",
            "ÐºÐ°Ð»ÐµÐ½Ð´Ð°ÑÑ": "outlookcal:",
            "youtube": "https://youtube.com",
            "ÑÑÑÐ±": "https://youtube.com",
            "Ð³ÑÐ³Ð»": "https://google.com",
            "github": "https://github.com",
            "ÑÐµÐ»ÐµÐ³ÑÐ°Ð¼": "telegram.exe",
            "discord": "discord.exe",
            "ÑÐ¿Ð¾ÑÐ¸ÑÐ°Ð¹": "spotify.exe",
            "vlc": "vlc.exe",
        }

    def _save_apps(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ ÑÐ¿Ð¸ÑÐºÐ° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        with open(self.apps_file, 'w', encoding='utf-8') as f:
            json.dump(self.apps, f, ensure_ascii=False, indent=2)

    def launch(self, app_name: str) -> Dict:
        """ÐÐ°Ð¿ÑÑÐº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        app_name_lower = app_name.lower().strip()
        
        # ÐÐ¾Ð¸ÑÐº Ð² ÑÐ¿Ð¸ÑÐºÐµ
        if app_name_lower in self.apps:
            app_path = self.apps[app_name_lower]
            
            try:
                # ÐÑÐ»Ð¸ ÑÑÐ¾ URL
                if app_path.startswith("http://") or app_path.startswith("https://"):
                    subprocess.Popen(["start", app_path], shell=True)
                    return {"status": "ok", "message": f"ÐÑÐºÑÑÐ²Ð°Ñ {app_name}..."}
                
                # ÐÑÐ»Ð¸ ÑÑÐ¾ ÐºÐ¾Ð¼Ð°Ð½Ð´Ð° Windows
                elif app_path.startswith("ms-"):
                    subprocess.Popen(["start", app_path], shell=True)
                    return {"status": "ok", "message": f"ÐÑÐºÑÑÐ²Ð°Ñ {app_name}..."}
                
                # ÐÑÐ»Ð¸ ÑÑÐ¾ exe ÑÐ°Ð¹Ð»
                else:
                    subprocess.Popen(app_path, shell=True)
                    return {"status": "ok", "message": f"ÐÐ°Ð¿ÑÑÐºÐ°Ñ {app_name}..."}
            
            except Exception as e:
                self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð¿ÑÑÐºÐ° {app_name}: {e}")
                return {"status": "error", "message": f"ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð·Ð°Ð¿ÑÑÑÐ¸ÑÑ {app_name}: {e}"}
        
        return {"status": "error", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{app_name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾. Ð¡ÐºÐ°Ð¶Ð¸ÑÐµ 'Ð´Ð¾Ð±Ð°Ð²Ñ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ {app_name}'"}

    def add_app(self, name: str, path: str) -> Dict:
        """ÐÐ¾Ð±Ð°Ð²Ð¸ÑÑ Ð½Ð¾Ð²Ð¾Ðµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ."""
        name_lower = name.lower().strip()
        self.apps[name_lower] = path
        self._save_apps()
        
        self.logger.info(f"ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ: {name} â {path}")
        return {"status": "ok", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{name}' Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¾"}

    def remove_app(self, name: str) -> Dict:
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ."""
        name_lower = name.lower().strip()
        
        if name_lower in self.apps:
            del self.apps[name_lower]
            self._save_apps()
            return {"status": "ok", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{name}' ÑÐ´Ð°Ð»ÐµÐ½Ð¾"}
        
        return {"status": "error", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}

    def list_apps(self) -> Dict:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð²ÑÐµÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        apps_list = [f"â¢ {name}" for name in sorted(self.apps.keys())]
        return {
            "status": "ok",
            "message": f"ÐÐ¾ÑÑÑÐ¿Ð½Ð¾ {len(self.apps)} Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹:\n" + "\n".join(apps_list[:20]) + ("\n..." if len(apps_list) > 20 else "")
        }

    def get_apps_count(self) -> int:
        """ÐÐ¾Ð»Ð¸ÑÐµÑÑÐ²Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        return len(self.apps)
