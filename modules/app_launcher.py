"""
App Launcher - ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹ ÃÃÂµÃÃÂµÃÂ· JARVIS
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging


class AppLauncher:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂºÃÂ¾ÃÂ¼ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.apps_file = Path("data/apps.json")
        self.apps_file.parent.mkdir(exist_ok=True)
        self.apps: Dict[str, str] = self._load_apps()

    def _load_apps(self) -> Dict[str, str]:
        """ÃÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÃÂ¿ÃÂ¸ÃÃÂºÃÂ° ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""
        if self.apps_file.exists():
            with open(self.apps_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # ÃÃÂµÃÃÂ¾ÃÂ»ÃÃÂ½ÃÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã
        return {
            "ÃÂ±ÃÂ»ÃÂ¾ÃÂºÃÂ½ÃÂ¾Ã": "notepad.exe",
            "ÃÂºÃÂ°ÃÂ»ÃÃÂºÃÃÂ»ÃÃÃÂ¾Ã": "calc.exe",
            "ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ´ÃÂ½ÃÂ¸ÃÂº": "explorer.exe",
            "ÃÂ±ÃÃÂ°ÃÃÂ·ÃÂµÃ": "chrome.exe",
            "ÃÃÃÂ¾ÃÂ¼": "chrome.exe",
            "ÃÃÂ°ÃÂ¹ÃÃÃÂ¾ÃÂºÃ": "firefox.exe",
            "edge": "msedge.exe",
            "ÃÃÂµÃÃÂ¼ÃÂ¸ÃÂ½ÃÂ°ÃÂ»": "cmd.exe",
            "ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ½ÃÂ°Ã ÃÃÃÃÂ¾ÃÂºÃÂ°": "cmd.exe",
            "powershell": "powershell.exe",
            "ÃÂ½ÃÂ°ÃÃÃÃÂ¾ÃÂ¹ÃÂºÃÂ¸": "ms-settings:",
            "ÃÂ´ÃÂ¸ÃÃÂ¿ÃÂµÃÃÃÂµÃ ÃÂ·ÃÂ°ÃÂ´ÃÂ°Ã": "taskmgr.exe",
            "paint": "mspaint.exe",
            "ÃÃÂ¾ÃÃÂ¾ÃÂ³ÃÃÂ°ÃÃÂ¸ÃÂ¸": "ms-photos:",
            "ÃÂ¼ÃÂ°ÃÂ³ÃÂ°ÃÂ·ÃÂ¸ÃÂ½": "ms-windows-store:",
            "ÃÂ¿ÃÂ¾ÃÃÃÂ°": "outlookmail:",
            "ÃÂºÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ´ÃÂ°ÃÃ": "outlookcal:",
            "youtube": "https://youtube.com",
            "ÃÃÃÃÂ±": "https://youtube.com",
            "ÃÂ³ÃÃÂ³ÃÂ»": "https://google.com",
            "github": "https://github.com",
            "ÃÃÂµÃÂ»ÃÂµÃÂ³ÃÃÂ°ÃÂ¼": "telegram.exe",
            "discord": "discord.exe",
            "ÃÃÂ¿ÃÂ¾ÃÃÂ¸ÃÃÂ°ÃÂ¹": "spotify.exe",
            "vlc": "vlc.exe",
        }

    def _save_apps(self):
        """ÃÂ¡ÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂ¿ÃÂ¸ÃÃÂºÃÂ° ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""
        with open(self.apps_file, 'w', encoding='utf-8') as f:
            json.dump(self.apps, f, ensure_ascii=False, indent=2)

    def launch(self, app_name: str) -> Dict:
        """ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        app_name_lower = app_name.lower().strip()
        
        # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ² ÃÃÂ¿ÃÂ¸ÃÃÂºÃÂµ
        if app_name_lower in self.apps:
            app_path = self.apps[app_name_lower]
            
            try:
                # ÃÃÃÂ»ÃÂ¸ ÃÃÃÂ¾ URL
                if app_path.startswith("http://") or app_path.startswith("https://"):
                    subprocess.Popen(["start", app_path], shell=True)
                    return {"status": "ok", "message": f"ÃÃÃÂºÃÃÃÂ²ÃÂ°Ã {app_name}..."}
                
                # ÃÃÃÂ»ÃÂ¸ ÃÃÃÂ¾ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ° Windows
                elif app_path.startswith("ms-"):
                    subprocess.Popen(["start", app_path], shell=True)
                    return {"status": "ok", "message": f"ÃÃÃÂºÃÃÃÂ²ÃÂ°Ã {app_name}..."}
                
                # ÃÃÃÂ»ÃÂ¸ ÃÃÃÂ¾ exe ÃÃÂ°ÃÂ¹ÃÂ»
                else:
                    subprocess.Popen(app_path, shell=True)
                    return {"status": "ok", "message": f"ÃÃÂ°ÃÂ¿ÃÃÃÂºÃÂ°Ã {app_name}..."}
            
            except Exception as e:
                self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂºÃÂ° {app_name}: {e}")
                return {"status": "error", "message": f"ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÃÂ¸ÃÃ {app_name}: {e}"}
        
        return {"status": "error", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{app_name}' ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ¾. ÃÂ¡ÃÂºÃÂ°ÃÂ¶ÃÂ¸ÃÃÂµ 'ÃÂ´ÃÂ¾ÃÂ±ÃÂ°ÃÂ²Ã ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ {app_name}'"}

    def add_app(self, name: str, path: str) -> Dict:
        """ÃÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ¸ÃÃ ÃÂ½ÃÂ¾ÃÂ²ÃÂ¾ÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        name_lower = name.lower().strip()
        self.apps[name_lower] = path
        self._save_apps()
        
        self.logger.info(f"ÃÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ: {name} Ã¢ {path}")
        return {"status": "ok", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{name}' ÃÂ´ÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾"}

    def remove_app(self, name: str) -> Dict:
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        name_lower = name.lower().strip()
        
        if name_lower in self.apps:
            del self.apps[name_lower]
            self._save_apps()
            return {"status": "ok", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{name}' ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¾"}
        
        return {"status": "error", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{name}' ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ¾"}

    def list_apps(self) -> Dict:
        """ÃÂ¡ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÂ²ÃÃÂµÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""
        apps_list = [f"Ã¢Â¢ {name}" for name in sorted(self.apps.keys())]
        return {
            "status": "ok",
            "message": f"ÃÃÂ¾ÃÃÃÃÂ¿ÃÂ½ÃÂ¾ {len(self.apps)} ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹:\n" + "\n".join(apps_list[:20]) + ("\n..." if len(apps_list) > 20 else "")
        }

    def get_apps_count(self) -> int:
        """ÃÃÂ¾ÃÂ»ÃÂ¸ÃÃÂµÃÃÃÂ²ÃÂ¾ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""
        return len(self.apps)
