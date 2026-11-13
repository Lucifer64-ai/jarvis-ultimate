"""
App Analyzer Module - ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹ ÃÂ½ÃÂ° ÃÃ
JARVIS ÃÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÃÂµÃ, ÃÂ¸ÃÂ·ÃÃÃÂ°ÃÂµÃ ÃÂ¸ ÃÃÂ°ÃÂ·ÃÂ±ÃÂ¸ÃÃÂ°ÃÂµÃÃÃ ÃÂ² ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÃ
"""

import os
import json
import subprocess
import winreg
import psutil
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class AppAnalyzer:
    """ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ° ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹ ÃÂ½ÃÂ° ÃÃ."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.config = brain.config
        
        # ÃÃÂ°ÃÂ·ÃÂ° ÃÂ´ÃÂ°ÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹
        self.apps_db = {}
        self.db_path = Path("data/apps_database.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # ÃÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÃÃÃÂµÃÃÃÂ²ÃÃÃÃÂµÃÂ¹ ÃÃ
        self._load_database()
        
        # ÃÃÃÃÂ¸ ÃÂ´ÃÂ»Ã ÃÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã
        self.scan_paths = [
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")),
            Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")),
            Path(os.environ.get("LOCALAPPDATA", "")),
            Path(os.environ.get("APPDATA", "")),
            Path(os.path.expanduser("~\\Desktop")),
            Path(os.environ.get("USERPROFILE", "")),
        ]
        
        # ÃÂ ÃÂ°ÃÃÃÂ¸ÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÂ¼ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²
        self.executable_extensions = {".exe", ".msi", ".bat", ".cmd", ".ps1", ".com"}
        
        # ÃÂ ÃÂ°ÃÃÃÂ¸ÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ´ÃÂ¾ÃÂºÃÃÂ¼ÃÂµÃÂ½ÃÃÂ¾ÃÂ² ÃÂ´ÃÂ»Ã ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°
        self.document_extensions = {
            ".txt", ".md", ".json", ".xml", ".yaml", ".yml",
            ".ini", ".cfg", ".conf", ".log",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h"
        }
        
        self.logger.info("Ã¢ ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ° ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹ ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½")

    def _load_database(self):
        """ÃÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÂ±ÃÂ°ÃÂ·Ã ÃÂ´ÃÂ°ÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""
        try:
            if self.db_path.exists():
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.apps_db = json.load(f)
                self.logger.info(f"ÃÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½ÃÂ° ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹: {len(self.apps_db)} ÃÂ·ÃÂ°ÃÂ¿ÃÂ¸ÃÃÂµÃÂ¹")
            else:
                self.apps_db = {}
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÃ: {e}")
            self.apps_db = {}

    def _save_database(self):
        """ÃÂ¡ÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ±ÃÂ°ÃÂ·Ã ÃÂ´ÃÂ°ÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹."""
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.apps_db, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸Ã ÃÃ: {e}")

    # === ÃÂ¡ÃÃÃÃÃÂ ÃÃÃÃÃÃ ===

    def scan_installed_apps(self) -> Dict:
        """ÃÂ¡ÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹ ÃÃÂµÃÃÂµÃÂ· ÃÃÂµÃÂµÃÃÃ Windows."""
        self.logger.info("ÃÂ¡ÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹...")
        apps = []
        
        # ÃÃÂ»ÃÃÃÂ¸ ÃÃÂµÃÂµÃÃÃÃÂ° ÃÂ´ÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ¸ÃÃÂºÃÂ°
        registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        
        for hive, path in registry_keys:
            try:
                key = winreg.OpenKey(hive, path)
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        app_info = self._read_registry_app(subkey)
                        if app_info and app_info.get("name"):
                            apps.append(app_info)
                        
                        winreg.CloseKey(subkey)
                        i += 1
                    except OSError:
                        break
                
                winreg.CloseKey(key)
            except Exception as e:
                self.logger.debug(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÃÂµÃÂµÃÃÃÃÂ° {path}: {e}")
        
        # ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃ
        for app in apps:
            app_id = app.get("name", "").lower().replace(" ", "_")
            self.apps_db[app_id] = {
                **app,
                "last_seen": datetime.now().isoformat(),
                "analyzed": self.apps_db.get(app_id, {}).get("analyzed", False)
            }
        
        self._save_database()
        
        self.logger.info(f"ÃÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ¾ {len(apps)} ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹")
        return {
            "status": "ok",
            "count": len(apps),
            "apps": apps
        }

    def _read_registry_app(self, key) -> Optional[Dict]:
        """ÃÂ§ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÂ½ÃÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¸ ÃÂ¸ÃÂ· ÃÃÂµÃÂµÃÃÃÃÂ°."""
        try:
            name = winreg.QueryValueEx(key, "DisplayName")[0]
        except (OSError, FileNotFoundError):
            return None
        
        app_info = {"name": name}
        
        # ÃÃÂ¾ÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂ¸ÃÃÂµÃÂ»ÃÃÂ½ÃÃÂµ ÃÂ¿ÃÂ¾ÃÂ»Ã
        fields = {
            "DisplayVersion": "version",
            "Publisher": "publisher",
            "InstallDate": "install_date",
            "InstallLocation": "install_path",
            "UninstallString": "uninstall_string",
            "DisplayIcon": "icon_path",
            "EstimatedSize": "size_kb",
            "URLInfoAbout": "website",
            "HelpLink": "help_link",
        }
        
        for reg_name, field_name in fields.items():
            try:
                value = winreg.QueryValueEx(key, reg_name)[0]
                app_info[field_name] = value
            except (OSError, FileNotFoundError):
                pass
        
        return app_info

    def scan_executables(self, directory: str = None) -> Dict:
        """ÃÂ¡ÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÂ¼ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ² ÃÂ² ÃÂ´ÃÂ¸ÃÃÂµÃÂºÃÃÂ¾ÃÃÂ¸ÃÃ."""
        self.logger.info("ÃÂ¡ÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÂ¼ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²...")
        executables = []
        
        paths_to_scan = [Path(directory)] if directory else self.scan_paths
        
        for scan_path in paths_to_scan:
            if not scan_path or not scan_path.exists():
                continue
            
            try:
                for item in scan_path.rglob("*"):
                    if item.suffix.lower() in self.executable_extensions:
                        exe_info = self._analyze_executable(item)
                        if exe_info:
                            executables.append(exe_info)
            except PermissionError:
                continue
            except Exception as e:
                self.logger.debug(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂºÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã {scan_path}: {e}")
        
        return {
            "status": "ok",
            "count": len(executables),
            "executables": executables[:100]  # ÃÃÂ³ÃÃÂ°ÃÂ½ÃÂ¸ÃÃÂµÃÂ½ÃÂ¸ÃÂµ
        }

    def _analyze_executable(self, path: Path) -> Optional[Dict]:
        """ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÂ¼ÃÂ¾ÃÂ³ÃÂ¾ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ°."""
        try:
            stat = path.stat()
            
            info = {
                "name": path.stem,
                "path": str(path),
                "extension": path.suffix,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
            
            # ÃÃÂµÃÃÃÂ¸Ã ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ° (Windows)
            try:
                import win32api
                version_info = win32api.GetFileVersionInfo(str(path), "\\")
                if version_info:
                    info["file_version"] = str(version_info.get("FileVersion", ""))
                    info["product_version"] = str(version_info.get("ProductVersion", ""))
                    info["company"] = str(version_info.get("CompanyName", ""))
                    info["description"] = str(version_info.get("FileDescription", ""))
            except Exception:
                pass
            
            return info
            
        except Exception as e:
            self.logger.debug(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ° {path}: {e}")
            return None

    # === ÃÃÃÃÃÃ ÃÃÂ ÃÃÃÃÃÃÃÃÂ¯ ===

    def analyze_app(self, app_name: str) -> Dict:
        """ÃÃÂ»ÃÃÂ±ÃÂ¾ÃÂºÃÂ¸ÃÂ¹ ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÂºÃÂ¾ÃÂ½ÃÂºÃÃÂµÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        self.logger.info(f"ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã: {app_name}")
        
        app_id = app_name.lower().replace(" ", "_")
        
        # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ² ÃÃ
        app_data = self.apps_db.get(app_id)
        if not app_data:
            # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ¿ÃÂ¾ ÃÃÂ°ÃÃÃÂ¸ÃÃÂ½ÃÂ¾ÃÂ¼Ã ÃÃÂ¾ÃÂ²ÃÂ¿ÃÂ°ÃÂ´ÃÂµÃÂ½ÃÂ¸Ã
            for key, value in self.apps_db.items():
                if app_name.lower() in key or app_name.lower() in value.get("name", "").lower():
                    app_data = value
                    app_id = key
                    break
        
        if not app_data:
            return {"status": "error", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{app_name}' ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ¾"}
        
        # ÃÃÂ»ÃÃÂ±ÃÂ¾ÃÂºÃÂ¸ÃÂ¹ ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·
        analysis = {
            "name": app_data.get("name", app_name),
            "version": app_data.get("version", "ÃÂ½ÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÃÃÂ½ÃÂ¾"),
            "publisher": app_data.get("publisher", "ÃÂ½ÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÃÃÂ½ÃÂ¾"),
            "install_path": app_data.get("install_path", ""),
            "size_kb": app_data.get("size_kb", 0),
            "install_date": app_data.get("install_date", "ÃÂ½ÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÃÃÂ½ÃÂ¾"),
        }
        
        # ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ² ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã
        if analysis["install_path"] and Path(analysis["install_path"]).exists():
            analysis["files"] = self._analyze_app_files(Path(analysis["install_path"]))
        
        # ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÂ¿ÃÃÂ¾ÃÃÂµÃÃÃÂ¾ÃÂ²
        analysis["running"] = self._is_app_running(app_name)
        if analysis["running"]:
            analysis["processes"] = self._get_app_processes(app_name)
        
        # ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÃÂµÃÃÃÃÃÂ¾ÃÂ²
        if analysis["running"] and analysis.get("processes"):
            analysis["resource_usage"] = self._get_app_resource_usage(analysis["processes"])
        
        # ÃÃÂ°ÃÃÂµÃÂ³ÃÂ¾ÃÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã
        analysis["category"] = self._categorize_app(app_name, app_data)
        
        # ÃÃÂ¿ÃÂ¸ÃÃÂ°ÃÂ½ÃÂ¸ÃÂµ
        analysis["description"] = self._generate_app_description(analysis)
        
        # ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃ
        self.apps_db[app_id] = {
            **app_data,
            "analyzed": True,
            "last_analyzed": datetime.now().isoformat(),
            "analysis": analysis
        }
        self._save_database()
        
        return {"status": "ok", "analysis": analysis}

    def _analyze_app_files(self, app_path: Path) -> Dict:
        """ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ· ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ² ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        files_info = {
            "total_files": 0,
            "total_size_mb": 0,
            "file_types": {},
            "config_files": [],
            "data_files": [],
            "executables": [],
        }
        
        try:
            for item in app_path.rglob("*"):
                if item.is_file():
                    files_info["total_files"] += 1
                    files_info["total_size_mb"] += item.stat().st_size / (1024 * 1024)
                    
                    ext = item.suffix.lower()
                    files_info["file_types"][ext] = files_info["file_types"].get(ext, 0) + 1
                    
                    if ext in {".ini", ".cfg", ".conf", ".json", ".xml", ".yaml", ".yml", ".toml"}:
                        files_info["config_files"].append(str(item.relative_to(app_path)))
                    
                    elif ext in {".db", ".sqlite", ".dat", ".sav"}:
                        files_info["data_files"].append(str(item.relative_to(app_path)))
                    
                    elif ext in self.executable_extensions:
                        files_info["executables"].append(str(item.relative_to(app_path)))
        
        except Exception as e:
            self.logger.debug(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ° ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ² {app_path}: {e}")
        
        files_info["total_size_mb"] = round(files_info["total_size_mb"], 2)
        return files_info

    def _is_app_running(self, app_name: str) -> bool:
        """ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ°, ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾ ÃÂ»ÃÂ¸ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        app_lower = app_name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                if app_lower in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def _get_app_processes(self, app_name: str) -> List[Dict]:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÂ½ÃÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ ÃÂ¿ÃÃÂ¾ÃÃÂµÃÃÃÂ°Ã ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        processes = []
        app_lower = app_name.lower()
        
        for proc in psutil.process_iter(["pid", "name", "exe", "status", "create_time"]):
            try:
                if app_lower in proc.info["name"].lower():
                    processes.append({
                        "pid": proc.info["pid"],
                        "name": proc.info["name"],
                        "exe": proc.info["exe"],
                        "status": proc.info["status"],
                        "started": datetime.fromtimestamp(proc.info["create_time"]).isoformat()
                            if proc.info["create_time"] else None
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return processes

    def _get_app_resource_usage(self, processes: List[Dict]) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã ÃÃÂµÃÃÃÃÃÂ¾ÃÂ² ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµÃÂ¼."""
        total_cpu = 0.0
        total_memory_mb = 0.0
        
        for proc_info in processes:
            try:
                proc = psutil.Process(proc_info["pid"])
                total_cpu += proc.cpu_percent(interval=0.1)
                total_memory_mb += proc.memory_info().rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return {
            "cpu_percent": round(total_cpu, 1),
            "memory_mb": round(total_memory_mb, 1),
            "process_count": len(processes)
        }

    def _categorize_app(self, app_name: str, app_data: Dict) -> str:
        """ÃÃÂ°ÃÃÂµÃÂ³ÃÂ¾ÃÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        name_lower = app_name.lower()
        
        categories = {
            "browser": ["chrome", "firefox", "edge", "opera", "brave", "safari", "ÃÃÂ½ÃÂ´ÃÂµÃÂºÃ"],
            "messenger": ["telegram", "discord", "slack", "whatsapp", "viber", "skype", "teams"],
            "editor": ["code", "vscode", "notepad", "sublime", "atom", "vim", "notepad++"],
            "media": ["vlc", "spotify", "youtube", "netflix", "plex", "kodi", "itunes"],
            "game": ["steam", "epic", "origin", "gog", "ubisoft", "battle.net"],
            "dev": ["python", "node", "java", "git", "docker", "visual studio", "intellij", "pycharm"],
            "office": ["word", "excel", "powerpoint", "outlook", "libreoffice", "office"],
            "security": ["antivirus", "defender", "kaspersky", "norton", "malwarebytes", "avast"],
            "system": ["explorer", "task manager", "control panel", "settings", "ccleaner"],
            "cloud": ["dropbox", "onedrive", "google drive", "yandex disk"],
        }
        
        for category, keywords in categories.items():
            if any(kw in name_lower for kw in keywords):
                return category
        
        return "other"

    def _generate_app_description(self, analysis: Dict) -> str:
        """ÃÃÂµÃÂ½ÃÂµÃÃÂ°ÃÃÂ¸Ã ÃÂ¾ÃÂ¿ÃÂ¸ÃÃÂ°ÃÂ½ÃÂ¸Ã ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        name = analysis.get("name", "ÃÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÃÃÂ½ÃÂ¾ÃÂµ")
        version = analysis.get("version", "ÃÂ½ÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÃÃÂ½ÃÂ¾")
        publisher = analysis.get("publisher", "ÃÂ½ÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÃÃÂ½ÃÂ¾")
        category = analysis.get("category", "other")
        
        category_names = {
            "browser": "ÃÂ²ÃÂµÃÂ±-ÃÂ±ÃÃÂ°ÃÃÂ·ÃÂµÃ",
            "messenger": "ÃÂ¼ÃÂµÃÃÃÂµÃÂ½ÃÂ´ÃÂ¶ÃÂµÃ",
            "editor": "ÃÃÂµÃÂºÃÃÃÂ¾ÃÂ²ÃÃÂ¹ ÃÃÂµÃÂ´ÃÂ°ÃÂºÃÃÂ¾Ã / IDE",
            "media": "ÃÂ¼ÃÂµÃÂ´ÃÂ¸ÃÂ°-ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ",
            "game": "ÃÂ¸ÃÂ³ÃÃÂ¾ÃÂ²ÃÂ°Ã ÃÂ¿ÃÂ»ÃÂ°ÃÃÃÂ¾ÃÃÂ¼ÃÂ°",
            "dev": "ÃÂ¸ÃÂ½ÃÃÃÃÃÂ¼ÃÂµÃÂ½Ã ÃÃÂ°ÃÂ·ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂºÃÂ¸",
            "office": "ÃÂ¾ÃÃÂ¸ÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ",
            "security": "ÃÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÂ±ÃÂµÃÂ·ÃÂ¾ÃÂ¿ÃÂ°ÃÃÂ½ÃÂ¾ÃÃÃÂ¸",
            "system": "ÃÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ½ÃÂ°Ã ÃÃÃÂ¸ÃÂ»ÃÂ¸ÃÃÂ°",
            "cloud": "ÃÂ¾ÃÂ±ÃÂ»ÃÂ°ÃÃÂ½ÃÂ¾ÃÂµ ÃÃÃÂ°ÃÂ½ÃÂ¸ÃÂ»ÃÂ¸ÃÃÂµ",
            "other": "ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ"
        }
        
        cat_name = category_names.get(category, "ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ")
        
        desc = f"{name} (ÃÂ²ÃÂµÃÃÃÂ¸Ã {version}) Ã¢ ÃÃÃÂ¾ {cat_name} ÃÂ¾Ã {publisher}."
        
        if analysis.get("running"):
            usage = analysis.get("resource_usage", {})
            desc += f" ÃÂ¡ÃÂµÃÂ¹ÃÃÂ°Ã ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾. CPU: {usage.get('cpu_percent', 0)}%, RAM: {usage.get('memory_mb', 0)} ÃÃ."
        
        files = analysis.get("files", {})
        if files.get("total_files"):
            desc += f" ÃÂ¡ÃÂ¾ÃÂ´ÃÂµÃÃÂ¶ÃÂ¸Ã {files['total_files']} ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ² ({files.get('total_size_mb', 0)} ÃÃ)."
        
        return desc

    # === ÃÂ£ÃÃÂ ÃÃÃÃÃÃÃ ÃÃÂ ÃÃÃÃÃÃÃÃÂ¯ÃÃ ===

    def launch_app(self, app_name: str) -> Dict:
        """ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        self.logger.info(f"ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã: {app_name}")
        
        # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ² ÃÃ
        app_id = app_name.lower().replace(" ", "_")
        app_data = self.apps_db.get(app_id)
        
        if not app_data:
            for key, value in self.apps_db.items():
                if app_name.lower() in key or app_name.lower() in value.get("name", "").lower():
                    app_data = value
                    break
        
        if not app_data:
            return {"status": "error", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{app_name}' ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ¾"}
        
        # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÂ¼ÃÂ¾ÃÂ³ÃÂ¾ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ°
        exe_path = None
        install_path = app_data.get("install_path", "")
        
        if install_path and Path(install_path).exists():
            # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ¾ÃÃÂ½ÃÂ¾ÃÂ²ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ exe
            for exe in Path(install_path).rglob("*.exe"):
                if app_name.lower().split()[0] in exe.stem.lower():
                    exe_path = str(exe)
                    break
            
            if not exe_path:
                # ÃÃÂµÃÃÃÂ¼ ÃÂ¿ÃÂµÃÃÂ²ÃÃÂ¹ exe
                for exe in Path(install_path).rglob("*.exe"):
                    exe_path = str(exe)
                    break
        
        if not exe_path:
            return {"status": "error", "message": "ÃÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÂ¼ÃÃÂ¹ ÃÃÂ°ÃÂ¹ÃÂ» ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½"}
        
        try:
            subprocess.Popen([exe_path], shell=True)
            return {
                "status": "ok",
                "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ {app_name} ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾",
                "path": exe_path
            }
        except Exception as e:
            return {"status": "error", "message": f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂºÃÂ°: {e}"}

    def close_app(self, app_name: str) -> Dict:
        """ÃÃÂ°ÃÂºÃÃÃÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        self.logger.info(f"ÃÃÂ°ÃÂºÃÃÃÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã: {app_name}")
        
        closed = []
        app_lower = app_name.lower()
        
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if app_lower in proc.info["name"].lower():
                    p = psutil.Process(proc.info["pid"])
                    p.terminate()
                    closed.append(proc.info["name"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if closed:
            return {
                "status": "ok",
                "message": f"ÃÃÂ°ÃÂºÃÃÃÃÂ¾ ÃÂ¿ÃÃÂ¾ÃÃÂµÃÃÃÂ¾ÃÂ²: {len(closed)}",
                "processes": closed
            }
        
        return {"status": "error", "message": f"ÃÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ '{app_name}' ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾"}

    # === ÃÃÂ¢ÃÂ§ÃÃÂ¢ÃÂ« ===

    def get_full_report(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÂ½ÃÃÂ¹ ÃÂ¾ÃÃÃÃ ÃÂ¾ ÃÂ²ÃÃÂµÃ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÃ."""
        if not self.apps_db:
            self.scan_installed_apps()
        
        categories = {}
        total_size = 0
        running_count = 0
        
        for app_id, app_data in self.apps_db.items():
            cat = self._categorize_app(app_data.get("name", ""), app_data)
            categories[cat] = categories.get(cat, 0) + 1
            
            size_kb = app_data.get("size_kb", 0)
            if isinstance(size_kb, (int, float)):
                total_size += size_kb
            
            if self._is_app_running(app_data.get("name", "")):
                running_count += 1
        
        return {
            "status": "ok",
            "total_apps": len(self.apps_db),
            "analyzed": sum(1 for a in self.apps_db.values() if a.get("analyzed")),
            "running": running_count,
            "total_size_mb": round(total_size / 1024, 1),
            "categories": categories,
            "top_by_size": self._get_top_apps_by_size()
        }

    def _get_top_apps_by_size(self, limit: int = 10) -> List[Dict]:
        """ÃÂ¢ÃÂ¾ÃÂ¿ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂ¹ ÃÂ¿ÃÂ¾ ÃÃÂ°ÃÂ·ÃÂ¼ÃÂµÃÃ."""
        apps_with_size = []
        
        for app_id, app_data in self.apps_db.items():
            size_kb = app_data.get("size_kb", 0)
            if isinstance(size_kb, (int, float)) and size_kb > 0:
                apps_with_size.append({
                    "name": app_data.get("name", app_id),
                    "size_mb": round(size_kb / 1024, 1),
                    "publisher": app_data.get("publisher", "")
                })
        
        apps_with_size.sort(key=lambda x: x["size_mb"], reverse=True)
        return apps_with_size[:limit]

    def format_report_message(self, report: Dict) -> str:
        """ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¾ÃÃÃÃÃÂ° ÃÂ² ÃÃÂ¾ÃÂ¾ÃÂ±ÃÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        if report["status"] != "ok":
            return "ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ¾ÃÃÃÃ"
        
        msg = f"Ã° ÃÃÃÃÃ ÃÂ¿ÃÂ¾ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÃÂ¼:\n\n"
        msg += f"ÃÃÃÂµÃÂ³ÃÂ¾: {report['total_apps']}\n"
        msg += f"ÃÃÃÂ¾ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¾: {report['analyzed']}\n"
        msg += f"ÃÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾ ÃÃÂµÃÂ¹ÃÃÂ°Ã: {report['running']}\n"
        msg += f"ÃÃÂ±ÃÃÂ¸ÃÂ¹ ÃÃÂ°ÃÂ·ÃÂ¼ÃÂµÃ: {report['total_size_mb']} ÃÃ\n\n"
        
        msg += "ÃÃÂ°ÃÃÂµÃÂ³ÃÂ¾ÃÃÂ¸ÃÂ¸:\n"
        for cat, count in sorted(report["categories"].items(), key=lambda x: x[1], reverse=True):
            msg += f"  Ã¢Â¢ {cat}: {count}\n"
        
        if report.get("top_by_size"):
            msg += "\nÃÂ¢ÃÂ¾ÃÂ¿ ÃÂ¿ÃÂ¾ ÃÃÂ°ÃÂ·ÃÂ¼ÃÂµÃÃ:\n"
            for app in report["top_by_size"][:5]:
                msg += f"  Ã¢Â¢ {app['name']} Ã¢ {app['size_mb']} ÃÃ\n"
        
        return msg

    def format_analysis_message(self, analysis: Dict) -> str:
        """ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ° ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        if analysis.get("status") != "ok":
            return analysis.get("message", "ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°")
        
        a = analysis["analysis"]
        msg = f"Ã° ÃÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·: {a['name']}\n\n"
        msg += f"{a['description']}\n\n"
        msg += f"ÃÃÂµÃÃÃÂ¸Ã: {a['version']}\n"
        msg += f"ÃÃÂ·ÃÂ´ÃÂ°ÃÃÂµÃÂ»Ã: {a['publisher']}\n"
        msg += f"ÃÃÂ°ÃÃÂµÃÂ³ÃÂ¾ÃÃÂ¸Ã: {a['category']}\n"
        
        if a.get("running"):
            usage = a.get("resource_usage", {})
            msg += f"\nÃ¢Â¡ ÃÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾:\n"
            msg += f"  CPU: {usage.get('cpu_percent', 0)}%\n"
            msg += f"  RAM: {usage.get('memory_mb', 0)} ÃÃ\n"
            msg += f"  ÃÃÃÂ¾ÃÃÂµÃÃÃ: {usage.get('process_count', 0)}\n"
        else:
            msg += "\nÃ¢Â¸ ÃÃÂµ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ¾\n"
        
        files = a.get("files", {})
        if files.get("total_files"):
            msg += f"\nÃ° ÃÂ¤ÃÂ°ÃÂ¹ÃÂ»Ã: {files['total_files']} ({files.get('total_size_mb', 0)} ÃÃ)\n"
        
        return msg
