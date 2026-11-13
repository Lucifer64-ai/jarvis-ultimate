"""
ÐÐµÐ½ÐµÐ´Ð¶ÐµÑ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ° JARVIS
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path


class ContextManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ¾Ð¼ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ° Ð¸ ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ñ."""

    def __init__(self, brain):
        self.brain = brain
        self.context_file = Path("data/context.json")
        self.context_file.parent.mkdir(exist_ok=True)
        
        self.context: Dict = self._load_context()
        self.conversation_history: List[Dict] = []
        self.max_history = 50

    def _load_context(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° ÐºÐ¾Ð½ÑÐµÐºÑÑÐ° Ð¸Ð· ÑÐ°Ð¹Ð»Ð°."""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°: {e}")
        
        return {
            "user_preferences": {},
            "session_start": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }

    def _save_context(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°."""
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self.context, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ñ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°: {e}")

    def update(self, key: str, value):
        """ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°."""
        self.context[key] = value
        self.context["last_activity"] = datetime.now().isoformat()
        self._save_context()

    def get(self, key: str, default=None):
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ñ Ð¸Ð· ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°."""
        return self.context.get(key, default)

    def add_to_history(self, role: str, content: str):
        """ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð² Ð¸ÑÑÐ¾ÑÐ¸Ñ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ°."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # ÐÐ³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ðµ Ð¸ÑÑÐ¾ÑÐ¸Ð¸
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    def get_history(self, limit: int = 10) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¸ÑÑÐ¾ÑÐ¸Ð¸ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ°."""
        return self.conversation_history[-limit:]

    def clear_history(self):
        """ÐÑÐ¸ÑÑÐºÐ° Ð¸ÑÑÐ¾ÑÐ¸Ð¸."""
        self.conversation_history = []

    def get_system_context(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ ÑÐ¸ÑÑÐµÐ¼Ð½Ð¾Ð³Ð¾ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°."""
        import psutil
        
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d")
        }

    def set_user_preference(self, key: str, value):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÑÐºÐ¸Ñ Ð¿ÑÐµÐ´Ð¿Ð¾ÑÑÐµÐ½Ð¸Ð¹."""
        if "user_preferences" not in self.context:
            self.context["user_preferences"] = {}
        
        self.context["user_preferences"][key] = value
        self._save_context()

    def get_user_preference(self, key: str, default=None):
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÑÐºÐ¸Ñ Ð¿ÑÐµÐ´Ð¿Ð¾ÑÑÐµÐ½Ð¸Ð¹."""
        return self.context.get("user_preferences", {}).get(key, default)
