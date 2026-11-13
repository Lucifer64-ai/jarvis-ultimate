"""
App Analyzer Module - ÐÐ½Ð°Ð»Ð¸Ð· ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ Ð½Ð° ÐÐ
JARVIS ÑÐºÐ°Ð½Ð¸ÑÑÐµÑ, Ð¸Ð·ÑÑÐ°ÐµÑ Ð¸ ÑÐ°Ð·Ð±Ð¸ÑÐ°ÐµÑÑÑ Ð² Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸ÑÑ
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
    """ÐÐ¾Ð´ÑÐ»Ñ Ð°Ð½Ð°Ð»Ð¸Ð·Ð° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ Ð½Ð° ÐÐ."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.config = brain.config
        
        # ÐÐ°Ð·Ð° Ð´Ð°Ð½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹
        self.apps_db = {}
        self.db_path = Path("data/apps_database.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # ÐÐ°Ð³ÑÑÐ·ÐºÐ° ÑÑÑÐµÑÑÐ²ÑÑÑÐµÐ¹ ÐÐ
        self._load_database()
        
        # ÐÑÑÐ¸ Ð´Ð»Ñ ÑÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ñ
        self.scan_paths = [
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")),
            Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")),
            Path(os.environ.get("LOCALAPPDATA", "")),
            Path(os.environ.get("APPDATA", "")),
            Path(os.path.expanduser("~\\Desktop")),
            Path(os.environ.get("USERPROFILE", "")),
        ]
        
        # Ð Ð°ÑÑÐ¸ÑÐµÐ½Ð¸Ñ Ð¸ÑÐ¿Ð¾Ð»Ð½ÑÐµÐ¼ÑÑ ÑÐ°Ð¹Ð»Ð¾Ð²
        self.executable_extensions = {".exe", ".msi", ".bat", ".cmd", ".ps1", ".com"}
        
        # Ð Ð°ÑÑÐ¸ÑÐµÐ½Ð¸Ñ Ð´Ð¾ÐºÑÐ¼ÐµÐ½ÑÐ¾Ð² Ð´Ð»Ñ Ð°Ð½Ð°Ð»Ð¸Ð·Ð°
        self.document_extensions = {
            ".txt", ".md", ".json", ".xml", ".yaml", ".yml",
            ".ini", ".cfg", ".conf", ".log",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h"
        }
        
        self.logger.info("â ÐÐ¾Ð´ÑÐ»Ñ Ð°Ð½Ð°Ð»Ð¸Ð·Ð° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½")

    def _load_database(self):
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð±Ð°Ð·Ñ Ð´Ð°Ð½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        try:
            if self.db_path.exists():
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.apps_db = json.load(f)
                self.logger.info(f"ÐÐ°Ð³ÑÑÐ¶ÐµÐ½Ð° ÐÐ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹: {len(self.apps_db)} Ð·Ð°Ð¿Ð¸ÑÐµÐ¹")
            else:
                self.apps_db = {}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ ÐÐ: {e}")
            self.apps_db = {}

    def _save_database(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð±Ð°Ð·Ñ Ð´Ð°Ð½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.apps_db, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ñ ÐÐ: {e}")

    # === Ð¡ÐÐÐÐÐ ÐÐÐÐÐÐ ===

    def scan_installed_apps(self) -> Dict:
        """Ð¡ÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ ÑÐµÑÐµÐ· ÑÐµÐµÑÑÑ Windows."""
        self.logger.info("Ð¡ÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹...")
        apps = []
        
        # ÐÐ»ÑÑÐ¸ ÑÐµÐµÑÑÑÐ° Ð´Ð»Ñ Ð¿Ð¾Ð¸ÑÐºÐ°
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
                self.logger.debug(f"ÐÑÐ¸Ð±ÐºÐ° ÑÑÐµÐ½Ð¸Ñ ÑÐµÐµÑÑÑÐ° {path}: {e}")
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÐÐ
        for app in apps:
            app_id = app.get("name", "").lower().replace(" ", "_")
            self.apps_db[app_id] = {
                **app,
                "last_seen": datetime.now().isoformat(),
                "analyzed": self.apps_db.get(app_id, {}).get("analyzed", False)
            }
        
        self._save_database()
        
        self.logger.info(f"ÐÐ°Ð¹Ð´ÐµÐ½Ð¾ {len(apps)} ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð½ÑÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹")
        return {
            "status": "ok",
            "count": len(apps),
            "apps": apps
        }

    def _read_registry_app(self, key) -> Optional[Dict]:
        """Ð§ÑÐµÐ½Ð¸Ðµ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¸ Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¸ Ð¸Ð· ÑÐµÐµÑÑÑÐ°."""
        try:
            name = winreg.QueryValueEx(key, "DisplayName")[0]
        except (OSError, FileNotFoundError):
            return None
        
        app_info = {"name": name}
        
        # ÐÐ¾Ð¿Ð¾Ð»Ð½Ð¸ÑÐµÐ»ÑÐ½ÑÐµ Ð¿Ð¾Ð»Ñ
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
        """Ð¡ÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¸ÑÐ¿Ð¾Ð»Ð½ÑÐµÐ¼ÑÑ ÑÐ°Ð¹Ð»Ð¾Ð² Ð² Ð´Ð¸ÑÐµÐºÑÐ¾ÑÐ¸ÑÑ."""
        self.logger.info("Ð¡ÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¸ÑÐ¿Ð¾Ð»Ð½ÑÐµÐ¼ÑÑ ÑÐ°Ð¹Ð»Ð¾Ð²...")
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
                self.logger.debug(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ñ {scan_path}: {e}")
        
        return {
            "status": "ok",
            "count": len(executables),
            "executables": executables[:100]  # ÐÐ³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ðµ
        }

    def _analyze_executable(self, path: Path) -> Optional[Dict]:
        """ÐÐ½Ð°Ð»Ð¸Ð· Ð¸ÑÐ¿Ð¾Ð»Ð½ÑÐµÐ¼Ð¾Ð³Ð¾ ÑÐ°Ð¹Ð»Ð°."""
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
            
            # ÐÐµÑÑÐ¸Ñ ÑÐ°Ð¹Ð»Ð° (Windows)
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
            self.logger.debug(f"ÐÑÐ¸Ð±ÐºÐ° Ð°Ð½Ð°Ð»Ð¸Ð·Ð° {path}: {e}")
            return None

    # === ÐÐÐÐÐÐ ÐÐ ÐÐÐÐÐÐÐÐ¯ ===

    def analyze_app(self, app_name: str) -> Dict:
        """ÐÐ»ÑÐ±Ð¾ÐºÐ¸Ð¹ Ð°Ð½Ð°Ð»Ð¸Ð· ÐºÐ¾Ð½ÐºÑÐµÑÐ½Ð¾Ð³Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        self.logger.info(f"ÐÐ½Ð°Ð»Ð¸Ð· Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ: {app_name}")
        
        app_id = app_name.lower().replace(" ", "_")
        
        # ÐÐ¾Ð¸ÑÐº Ð² ÐÐ
        app_data = self.apps_db.get(app_id)
        if not app_data:
            # ÐÐ¾Ð¸ÑÐº Ð¿Ð¾ ÑÐ°ÑÑÐ¸ÑÐ½Ð¾Ð¼Ñ ÑÐ¾Ð²Ð¿Ð°Ð´ÐµÐ½Ð¸Ñ
            for key, value in self.apps_db.items():
                if app_name.lower() in key or app_name.lower() in value.get("name", "").lower():
                    app_data = value
                    app_id = key
                    break
        
        if not app_data:
            return {"status": "error", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{app_name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}
        
        # ÐÐ»ÑÐ±Ð¾ÐºÐ¸Ð¹ Ð°Ð½Ð°Ð»Ð¸Ð·
        analysis = {
            "name": app_data.get("name", app_name),
            "version": app_data.get("version", "Ð½ÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾"),
            "publisher": app_data.get("publisher", "Ð½ÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾"),
            "install_path": app_data.get("install_path", ""),
            "size_kb": app_data.get("size_kb", 0),
            "install_date": app_data.get("install_date", "Ð½ÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾"),
        }
        
        # ÐÐ½Ð°Ð»Ð¸Ð· ÑÐ°Ð¹Ð»Ð¾Ð² Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ
        if analysis["install_path"] and Path(analysis["install_path"]).exists():
            analysis["files"] = self._analyze_app_files(Path(analysis["install_path"]))
        
        # ÐÐ½Ð°Ð»Ð¸Ð· Ð¿ÑÐ¾ÑÐµÑÑÐ¾Ð²
        analysis["running"] = self._is_app_running(app_name)
        if analysis["running"]:
            analysis["processes"] = self._get_app_processes(app_name)
        
        # ÐÐ½Ð°Ð»Ð¸Ð· ÑÐµÑÑÑÑÐ¾Ð²
        if analysis["running"] and analysis.get("processes"):
            analysis["resource_usage"] = self._get_app_resource_usage(analysis["processes"])
        
        # ÐÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð·Ð°ÑÐ¸Ñ
        analysis["category"] = self._categorize_app(app_name, app_data)
        
        # ÐÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ
        analysis["description"] = self._generate_app_description(analysis)
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÐÐ
        self.apps_db[app_id] = {
            **app_data,
            "analyzed": True,
            "last_analyzed": datetime.now().isoformat(),
            "analysis": analysis
        }
        self._save_database()
        
        return {"status": "ok", "analysis": analysis}

    def _analyze_app_files(self, app_path: Path) -> Dict:
        """ÐÐ½Ð°Ð»Ð¸Ð· ÑÐ°Ð¹Ð»Ð¾Ð² Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
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
            self.logger.debug(f"ÐÑÐ¸Ð±ÐºÐ° Ð°Ð½Ð°Ð»Ð¸Ð·Ð° ÑÐ°Ð¹Ð»Ð¾Ð² {app_path}: {e}")
        
        files_info["total_size_mb"] = round(files_info["total_size_mb"], 2)
        return files_info

    def _is_app_running(self, app_name: str) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐºÐ°, Ð·Ð°Ð¿ÑÑÐµÐ½Ð¾ Ð»Ð¸ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ."""
        app_lower = app_name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                if app_lower in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def _get_app_processes(self, app_name: str) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¸ Ð¾ Ð¿ÑÐ¾ÑÐµÑÑÐ°Ñ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
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
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°Ð½Ð¸Ñ ÑÐµÑÑÑÑÐ¾Ð² Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸ÐµÐ¼."""
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
        """ÐÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð·Ð°ÑÐ¸Ñ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        name_lower = app_name.lower()
        
        categories = {
            "browser": ["chrome", "firefox", "edge", "opera", "brave", "safari", "ÑÐ½Ð´ÐµÐºÑ"],
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
        """ÐÐµÐ½ÐµÑÐ°ÑÐ¸Ñ Ð¾Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        name = analysis.get("name", "ÐÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾Ðµ")
        version = analysis.get("version", "Ð½ÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾")
        publisher = analysis.get("publisher", "Ð½ÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾")
        category = analysis.get("category", "other")
        
        category_names = {
            "browser": "Ð²ÐµÐ±-Ð±ÑÐ°ÑÐ·ÐµÑ",
            "messenger": "Ð¼ÐµÑÑÐµÐ½Ð´Ð¶ÐµÑ",
            "editor": "ÑÐµÐºÑÑÐ¾Ð²ÑÐ¹ ÑÐµÐ´Ð°ÐºÑÐ¾Ñ / IDE",
            "media": "Ð¼ÐµÐ´Ð¸Ð°-Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ",
            "game": "Ð¸Ð³ÑÐ¾Ð²Ð°Ñ Ð¿Ð»Ð°ÑÑÐ¾ÑÐ¼Ð°",
            "dev": "Ð¸Ð½ÑÑÑÑÐ¼ÐµÐ½Ñ ÑÐ°Ð·ÑÐ°Ð±Ð¾ÑÐºÐ¸",
            "office": "Ð¾ÑÐ¸ÑÐ½Ð¾Ðµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ",
            "security": "ÑÐ¸ÑÑÐµÐ¼Ð° Ð±ÐµÐ·Ð¾Ð¿Ð°ÑÐ½Ð¾ÑÑÐ¸",
            "system": "ÑÐ¸ÑÑÐµÐ¼Ð½Ð°Ñ ÑÑÐ¸Ð»Ð¸ÑÐ°",
            "cloud": "Ð¾Ð±Ð»Ð°ÑÐ½Ð¾Ðµ ÑÑÐ°Ð½Ð¸Ð»Ð¸ÑÐµ",
            "other": "Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ"
        }
        
        cat_name = category_names.get(category, "Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ")
        
        desc = f"{name} (Ð²ÐµÑÑÐ¸Ñ {version}) â ÑÑÐ¾ {cat_name} Ð¾Ñ {publisher}."
        
        if analysis.get("running"):
            usage = analysis.get("resource_usage", {})
            desc += f" Ð¡ÐµÐ¹ÑÐ°Ñ Ð·Ð°Ð¿ÑÑÐµÐ½Ð¾. CPU: {usage.get('cpu_percent', 0)}%, RAM: {usage.get('memory_mb', 0)} ÐÐ."
        
        files = analysis.get("files", {})
        if files.get("total_files"):
            desc += f" Ð¡Ð¾Ð´ÐµÑÐ¶Ð¸Ñ {files['total_files']} ÑÐ°Ð¹Ð»Ð¾Ð² ({files.get('total_size_mb', 0)} ÐÐ)."
        
        return desc

    # === Ð£ÐÐ ÐÐÐÐÐÐÐ ÐÐ ÐÐÐÐÐÐÐÐ¯ÐÐ ===

    def launch_app(self, app_name: str) -> Dict:
        """ÐÐ°Ð¿ÑÑÐº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        self.logger.info(f"ÐÐ°Ð¿ÑÑÐº Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ: {app_name}")
        
        # ÐÐ¾Ð¸ÑÐº Ð² ÐÐ
        app_id = app_name.lower().replace(" ", "_")
        app_data = self.apps_db.get(app_id)
        
        if not app_data:
            for key, value in self.apps_db.items():
                if app_name.lower() in key or app_name.lower() in value.get("name", "").lower():
                    app_data = value
                    break
        
        if not app_data:
            return {"status": "error", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{app_name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}
        
        # ÐÐ¾Ð¸ÑÐº Ð¸ÑÐ¿Ð¾Ð»Ð½ÑÐµÐ¼Ð¾Ð³Ð¾ ÑÐ°Ð¹Ð»Ð°
        exe_path = None
        install_path = app_data.get("install_path", "")
        
        if install_path and Path(install_path).exists():
            # ÐÐ¾Ð¸ÑÐº Ð¾ÑÐ½Ð¾Ð²Ð½Ð¾Ð³Ð¾ exe
            for exe in Path(install_path).rglob("*.exe"):
                if app_name.lower().split()[0] in exe.stem.lower():
                    exe_path = str(exe)
                    break
            
            if not exe_path:
                # ÐÐµÑÑÐ¼ Ð¿ÐµÑÐ²ÑÐ¹ exe
                for exe in Path(install_path).rglob("*.exe"):
                    exe_path = str(exe)
                    break
        
        if not exe_path:
            return {"status": "error", "message": "ÐÑÐ¿Ð¾Ð»Ð½ÑÐµÐ¼ÑÐ¹ ÑÐ°Ð¹Ð» Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
        
        try:
            subprocess.Popen([exe_path], shell=True)
            return {
                "status": "ok",
                "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ {app_name} Ð·Ð°Ð¿ÑÑÐµÐ½Ð¾",
                "path": exe_path
            }
        except Exception as e:
            return {"status": "error", "message": f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð¿ÑÑÐºÐ°: {e}"}

    def close_app(self, app_name: str) -> Dict:
        """ÐÐ°ÐºÑÑÑÐ¸Ðµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        self.logger.info(f"ÐÐ°ÐºÑÑÑÐ¸Ðµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ: {app_name}")
        
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
                "message": f"ÐÐ°ÐºÑÑÑÐ¾ Ð¿ÑÐ¾ÑÐµÑÑÐ¾Ð²: {len(closed)}",
                "processes": closed
            }
        
        return {"status": "error", "message": f"ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ '{app_name}' Ð½Ðµ Ð·Ð°Ð¿ÑÑÐµÐ½Ð¾"}

    # === ÐÐ¢Ð§ÐÐ¢Ð« ===

    def get_full_report(self) -> Dict:
        """ÐÐ¾Ð»Ð½ÑÐ¹ Ð¾ÑÑÑÑ Ð¾ Ð²ÑÐµÑ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸ÑÑ."""
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
        """Ð¢Ð¾Ð¿ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹ Ð¿Ð¾ ÑÐ°Ð·Ð¼ÐµÑÑ."""
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
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¾ÑÑÑÑÐ° Ð² ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ."""
        if report["status"] != "ok":
            return "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ Ð¾ÑÑÑÑ"
        
        msg = f"ð ÐÑÑÑÑ Ð¿Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸ÑÐ¼:\n\n"
        msg += f"ÐÑÐµÐ³Ð¾: {report['total_apps']}\n"
        msg += f"ÐÑÐ¾Ð°Ð½Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ð¾: {report['analyzed']}\n"
        msg += f"ÐÐ°Ð¿ÑÑÐµÐ½Ð¾ ÑÐµÐ¹ÑÐ°Ñ: {report['running']}\n"
        msg += f"ÐÐ±ÑÐ¸Ð¹ ÑÐ°Ð·Ð¼ÐµÑ: {report['total_size_mb']} ÐÐ\n\n"
        
        msg += "ÐÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¸:\n"
        for cat, count in sorted(report["categories"].items(), key=lambda x: x[1], reverse=True):
            msg += f"  â¢ {cat}: {count}\n"
        
        if report.get("top_by_size"):
            msg += "\nÐ¢Ð¾Ð¿ Ð¿Ð¾ ÑÐ°Ð·Ð¼ÐµÑÑ:\n"
            for app in report["top_by_size"][:5]:
                msg += f"  â¢ {app['name']} â {app['size_mb']} ÐÐ\n"
        
        return msg

    def format_analysis_message(self, analysis: Dict) -> str:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð°Ð½Ð°Ð»Ð¸Ð·Ð° Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        if analysis.get("status") != "ok":
            return analysis.get("message", "ÐÑÐ¸Ð±ÐºÐ° Ð°Ð½Ð°Ð»Ð¸Ð·Ð°")
        
        a = analysis["analysis"]
        msg = f"ð ÐÐ½Ð°Ð»Ð¸Ð·: {a['name']}\n\n"
        msg += f"{a['description']}\n\n"
        msg += f"ÐÐµÑÑÐ¸Ñ: {a['version']}\n"
        msg += f"ÐÐ·Ð´Ð°ÑÐµÐ»Ñ: {a['publisher']}\n"
        msg += f"ÐÐ°ÑÐµÐ³Ð¾ÑÐ¸Ñ: {a['category']}\n"
        
        if a.get("running"):
            usage = a.get("resource_usage", {})
            msg += f"\nâ¡ ÐÐ°Ð¿ÑÑÐµÐ½Ð¾:\n"
            msg += f"  CPU: {usage.get('cpu_percent', 0)}%\n"
            msg += f"  RAM: {usage.get('memory_mb', 0)} ÐÐ\n"
            msg += f"  ÐÑÐ¾ÑÐµÑÑÑ: {usage.get('process_count', 0)}\n"
        else:
            msg += "\nâ¸ ÐÐµ Ð·Ð°Ð¿ÑÑÐµÐ½Ð¾\n"
        
        files = a.get("files", {})
        if files.get("total_files"):
            msg += f"\nð Ð¤Ð°Ð¹Ð»Ñ: {files['total_files']} ({files.get('total_size_mb', 0)} ÐÐ)\n"
        
        return msg
