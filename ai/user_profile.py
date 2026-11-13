"""
ÐÑÐ¾ÑÐ¸Ð»Ñ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ JARVIS
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import Counter


class UserProfile:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿ÑÐ¾ÑÐ¸Ð»ÐµÐ¼ Ð¸ Ð¿ÑÐµÐ´Ð¿Ð¾ÑÑÐµÐ½Ð¸ÑÐ¼Ð¸ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ."""

    def __init__(self, brain):
        self.brain = brain
        self.profile_file = Path("data/user_profile.json")
        self.profile_file.parent.mkdir(exist_ok=True)
        self.profile: Dict = self._load_profile()
        self.command_history: List[Dict] = []

    def _load_profile(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¿ÑÐ¾ÑÐ¸Ð»Ñ."""
        if self.profile_file.exists():
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "name": None,
            "preferred_name": "ÑÑÑ",
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
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð¿ÑÐ¾ÑÐ¸Ð»Ñ."""
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)

    def set_name(self, name: str) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¸Ð¼ÐµÐ½Ð¸ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ."""
        self.profile["name"] = name
        self._save_profile()
        return {"status": "ok", "message": f"ÐÐ¼Ñ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð¾: {name}"}

    def set_preferred_name(self, preferred: str) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¿ÑÐµÐ´Ð¿Ð¾ÑÑÐ¸ÑÐµÐ»ÑÐ½Ð¾Ð³Ð¾ Ð¾Ð±ÑÐ°ÑÐµÐ½Ð¸Ñ."""
        self.profile["preferred_name"] = preferred
        self._save_profile()
        return {"status": "ok", "message": f"ÐÑÐ´Ñ Ð¾Ð±ÑÐ°ÑÐ°ÑÑÑÑ Ðº Ð²Ð°Ð¼: {preferred}"}

    def get_greeting(self) -> str:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¿ÑÐ¸Ð²ÐµÑÑÑÐ²Ð¸Ñ."""
        preferred = self.profile.get("preferred_name", "ÑÑÑ")
        name = self.profile.get("name")
        
        if name:
            return f"ÐÐ´ÑÐ°Ð²ÑÑÐ²ÑÐ¹ÑÐµ, {name}. Ð Ð°Ð´ Ð²Ð°Ñ Ð²Ð¸Ð´ÐµÑÑ, {preferred}."
        return f"ÐÐ´ÑÐ°Ð²ÑÑÐ²ÑÐ¹ÑÐµ, {preferred}."

    def update_activity(self):
        """ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿Ð¾ÑÐ»ÐµÐ´Ð½ÐµÐ¹ Ð°ÐºÑÐ¸Ð²Ð½Ð¾ÑÑÐ¸."""
        self.profile["last_active"] = datetime.now().isoformat()
        self._save_profile()

    def log_command(self, command: str, module: str = "unknown"):
        """ÐÐ¾Ð³Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        self.command_history.append({
            "command": command,
            "module": module,
            "timestamp": datetime.now().isoformat()
        })
        
        # ÐÐ³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ðµ Ð¸ÑÑÐ¾ÑÐ¸Ð¸
        if len(self.command_history) > 1000:
            self.command_history = self.command_history[-1000:]
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÐ°ÑÐ¸ÑÑÐ¸ÐºÐ¸
        self.profile["statistics"]["total_commands"] += 1
        self._update_statistics()
        self._save_profile()

    def _update_statistics(self):
        """ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÐ°ÑÐ¸ÑÑÐ¸ÐºÐ¸."""
        if not self.command_history:
            return
        
        # Ð¡Ð°Ð¼ÑÐµ ÑÐ°ÑÑÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
        commands = [entry["command"] for entry in self.command_history[-100:]]
        command_counts = Counter(commands)
        self.profile["statistics"]["favorite_commands"] = [
            {"command": cmd, "count": count}
            for cmd, count in command_counts.most_common(5)
        ]
        
        # Ð¡Ð°Ð¼ÑÐµ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÐµÐ¼ÑÐµ Ð¼Ð¾Ð´ÑÐ»Ð¸
        modules = [entry["module"] for entry in self.command_history[-100:]]
        module_counts = Counter(modules)
        self.profile["statistics"]["most_used_modules"] = [
            {"module": mod, "count": count}
            for mod, count in module_counts.most_common(5)
        ]
        
        # ÐÐºÑÐ¸Ð²Ð½ÑÐµ ÑÐ°ÑÑ
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
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¿ÑÐµÐ´Ð¿Ð¾ÑÑÐµÐ½Ð¸Ñ."""
        self.profile["preferences"][key] = value
        self._save_profile()
        return {"status": "ok", "message": f"ÐÑÐµÐ´Ð¿Ð¾ÑÑÐµÐ½Ð¸Ðµ '{key}' ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð¾"}

    def get_preference(self, key: str, default: Any = None) -> Any:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¿ÑÐµÐ´Ð¿Ð¾ÑÑÐµÐ½Ð¸Ñ."""
        return self.profile["preferences"].get(key, default)

    def get_profile(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¿Ð¾Ð»Ð½Ð¾Ð³Ð¾ Ð¿ÑÐ¾ÑÐ¸Ð»Ñ."""
        return self.profile

    def get_statistics(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ ÑÑÐ°ÑÐ¸ÑÑÐ¸ÐºÐ¸."""
        return self.profile.get("statistics", {})

    def reset_statistics(self) -> Dict:
        """Ð¡Ð±ÑÐ¾Ñ ÑÑÐ°ÑÐ¸ÑÑÐ¸ÐºÐ¸."""
        self.profile["statistics"] = {
            "total_commands": 0,
            "favorite_commands": [],
            "active_hours": [],
            "most_used_modules": []
        }
        self.command_history = []
        self._save_profile()
        return {"status": "ok", "message": "Ð¡ÑÐ°ÑÐ¸ÑÑÐ¸ÐºÐ° ÑÐ±ÑÐ¾ÑÐµÐ½Ð°"}
