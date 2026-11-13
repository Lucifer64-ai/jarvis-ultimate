"""
ÃÃÃÂ¾ÃÃÂ¸ÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»Ã JARVIS
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import Counter


class UserProfile:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¾ÃÃÂ¸ÃÂ»ÃÂµÃÂ¼ ÃÂ¸ ÃÂ¿ÃÃÂµÃÂ´ÃÂ¿ÃÂ¾ÃÃÃÂµÃÂ½ÃÂ¸ÃÃÂ¼ÃÂ¸ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»Ã."""

    def __init__(self, brain):
        self.brain = brain
        self.profile_file = Path("data/user_profile.json")
        self.profile_file.parent.mkdir(exist_ok=True)
        self.profile: Dict = self._load_profile()
        self.command_history: List[Dict] = []

    def _load_profile(self) -> Dict:
        """ÃÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÂ¿ÃÃÂ¾ÃÃÂ¸ÃÂ»Ã."""
        if self.profile_file.exists():
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "name": None,
            "preferred_name": "ÃÃÃ",
            "language": "ru",
            "created": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "preferences": {
                "voice_rate": 180,
                "voice_volume": 1.0,
                "hud_enabled": True,
                "notifications": True
            },
            "statistics": {
                "total_commands": 0,
                "favorite_commands": [],
                "active_hours": [],
                "most_used_modules": []
            }
        }

    def _save_profile(self):
        """ÃÂ¡ÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¾ÃÃÂ¸ÃÂ»Ã."""
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)

    def set_name(self, name: str) -> Dict:
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¸ÃÂ¼ÃÂµÃÂ½ÃÂ¸ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»Ã."""
        self.profile["name"] = name
        self._save_profile()
        return {"status": "ok", "message": f"ÃÃÂ¼Ã ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾: {name}"}

    def set_preferred_name(self, preferred: str) -> Dict:
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¿ÃÃÂµÃÂ´ÃÂ¿ÃÂ¾ÃÃÃÂ¸ÃÃÂµÃÂ»ÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¾ÃÂ±ÃÃÂ°ÃÃÂµÃÂ½ÃÂ¸Ã."""
        self.profile["preferred_name"] = preferred
        self._save_profile()
        return {"status": "ok", "message": f"ÃÃÃÂ´Ã ÃÂ¾ÃÂ±ÃÃÂ°ÃÃÂ°ÃÃÃÃ ÃÂº ÃÂ²ÃÂ°ÃÂ¼: {preferred}"}

    def get_greeting(self) -> str:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ²ÃÂµÃÃÃÃÂ²ÃÂ¸Ã."""
        preferred = self.profile.get("preferred_name", "ÃÃÃ")
        name = self.profile.get("name")
        
        if name:
            return f"ÃÃÂ´ÃÃÂ°ÃÂ²ÃÃÃÂ²ÃÃÂ¹ÃÃÂµ, {name}. ÃÂ ÃÂ°ÃÂ´ ÃÂ²ÃÂ°Ã ÃÂ²ÃÂ¸ÃÂ´ÃÂµÃÃ, {preferred}."
        return f"ÃÃÂ´ÃÃÂ°ÃÂ²ÃÃÃÂ²ÃÃÂ¹ÃÃÂµ, {preferred}."

    def update_activity(self):
        """ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÂ¾ÃÃÂ»ÃÂµÃÂ´ÃÂ½ÃÂµÃÂ¹ ÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂ½ÃÂ¾ÃÃÃÂ¸."""
        self.profile["last_active"] = datetime.now().isoformat()
        self._save_profile()

    def log_command(self, command: str, module: str = "unknown"):
        """ÃÃÂ¾ÃÂ³ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´Ã."""
        self.command_history.append({
            "command": command,
            "module": module,
            "timestamp": datetime.now().isoformat()
        })
        
        # ÃÃÂ³ÃÃÂ°ÃÂ½ÃÂ¸ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÃÃÂ¾ÃÃÂ¸ÃÂ¸
        if len(self.command_history) > 1000:
            self.command_history = self.command_history[-1000:]
        
        # ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÃÂ°ÃÃÂ¸ÃÃÃÂ¸ÃÂºÃÂ¸
        self.profile["statistics"]["total_commands"] += 1
        self._update_statistics()
        self._save_profile()

    def _update_statistics(self):
        """ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÃÂ°ÃÃÂ¸ÃÃÃÂ¸ÃÂºÃÂ¸."""
        if not self.command_history:
            return
        
        # ÃÂ¡ÃÂ°ÃÂ¼ÃÃÂµ ÃÃÂ°ÃÃÃÃÂµ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´Ã
        commands = [entry["command"] for entry in self.command_history[-100:]]
        command_counts = Counter(commands)
        self.profile["statistics"]["favorite_commands"] = [
            {"command": cmd, "count": count}
            for cmd, count in command_counts.most_common(5)
        ]
        
        # ÃÂ¡ÃÂ°ÃÂ¼ÃÃÂµ ÃÂ¸ÃÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÃÂµÃÂ¼ÃÃÂµ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂ¸
        modules = [entry["module"] for entry in self.command_history[-100:]]
        module_counts = Counter(modules)
        self.profile["statistics"]["most_used_modules"] = [
            {"module": mod, "count": count}
            for mod, count in module_counts.most_common(5)
        ]
        
        # ÃÃÂºÃÃÂ¸ÃÂ²ÃÂ½ÃÃÂµ ÃÃÂ°ÃÃ
        hours = []
        for entry in self.command_history[-100:]:
            try:
                dt = datetime.fromisoformat(entry["timestamp"])
                hours.append(dt.hour)
            except:
                pass
        
        if hours:
            hour_counts = Counter(hours)
            self.profile["statistics"]["active_hours"] = [
                {"hour": hour, "count": count}
                for hour, count in hour_counts.most_common(3)
            ]

    def set_preference(self, key: str, value: Any) -> Dict:
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¿ÃÃÂµÃÂ´ÃÂ¿ÃÂ¾ÃÃÃÂµÃÂ½ÃÂ¸Ã."""
        self.profile["preferences"][key] = value
        self._save_profile()
        return {"status": "ok", "message": f"ÃÃÃÂµÃÂ´ÃÂ¿ÃÂ¾ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ '{key}' ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾"}

    def get_preference(self, key: str, default: Any = None) -> Any:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÃÂµÃÂ´ÃÂ¿ÃÂ¾ÃÃÃÂµÃÂ½ÃÂ¸Ã."""
        return self.profile["preferences"].get(key, default)

    def get_profile(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¿ÃÃÂ¾ÃÃÂ¸ÃÂ»Ã."""
        return self.profile

    def get_statistics(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÃÂ°ÃÃÂ¸ÃÃÃÂ¸ÃÂºÃÂ¸."""
        return self.profile.get("statistics", {})

    def reset_statistics(self) -> Dict:
        """ÃÂ¡ÃÂ±ÃÃÂ¾Ã ÃÃÃÂ°ÃÃÂ¸ÃÃÃÂ¸ÃÂºÃÂ¸."""
        self.profile["statistics"] = {
            "total_commands": 0,
            "favorite_commands": [],
            "active_hours": [],
            "most_used_modules": []
        }
        self.command_history = []
        self._save_profile()
        return {"status": "ok", "message": "ÃÂ¡ÃÃÂ°ÃÃÂ¸ÃÃÃÂ¸ÃÂºÃÂ° ÃÃÂ±ÃÃÂ¾ÃÃÂµÃÂ½ÃÂ°"}
