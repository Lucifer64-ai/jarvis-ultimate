"""
Ð¡Ð¸ÑÑÐµÐ¼Ð° ÑÑÐ¸Ð³Ð³ÐµÑÐ¾Ð² JARVIS
"""

from typing import Dict, List, Callable
import threading
import time


class TriggerManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÐ¸Ð³Ð³ÐµÑÐ°Ð¼Ð¸."""

    def __init__(self, brain):
        self.brain = brain
        self.triggers: Dict[str, Dict] = {}
        self.running = False

    def add_trigger(self, name: str, condition: Callable, action: Callable):
        """ÐÐ¾Ð±Ð°Ð²Ð¸ÑÑ ÑÑÐ¸Ð³Ð³ÐµÑ."""
        self.triggers[name] = {
            "condition": condition,
            "action": action,
            "active": True
        }
        self.brain.logger.info(f"Ð¢ÑÐ¸Ð³Ð³ÐµÑ '{name}' Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½")
        return {"status": "ok", "name": name}

    def remove_trigger(self, name: str):
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ ÑÑÐ¸Ð³Ð³ÐµÑ."""
        if name in self.triggers:
            del self.triggers[name]
            return {"status": "ok"}
        return {"status": "error", "message": "Ð¢ÑÐ¸Ð³Ð³ÐµÑ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}

    def list_triggers(self) -> List[str]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº ÑÑÐ¸Ð³Ð³ÐµÑÐ¾Ð²."""
        return list(self.triggers.keys())

    def start(self):
        """ÐÐ°Ð¿ÑÑÐº Ð¿ÑÐ¾Ð²ÐµÑÐºÐ¸ ÑÑÐ¸Ð³Ð³ÐµÑÐ¾Ð²."""
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÐÑÐ½Ð¾Ð²Ð½Ð¾Ð¹ ÑÐ¸ÐºÐ» Ð¿ÑÐ¾Ð²ÐµÑÐºÐ¸ ÑÑÐ¸Ð³Ð³ÐµÑÐ¾Ð²."""
        while self.running:
            for name, trigger in self.triggers.items():
                if not trigger["active"]:
                    continue
                
                try:
                    if trigger["condition"]():
                        self.brain.logger.info(f"Ð¢ÑÐ¸Ð³Ð³ÐµÑ '{name}' ÑÑÐ°Ð±Ð¾ÑÐ°Ð»")
                        trigger["action"]()
                except Exception as e:
                    self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÑÐ¸Ð³Ð³ÐµÑÐ° '{name}': {e}")
            
            time.sleep(5)

    def stop(self):
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¿ÑÐ¾Ð²ÐµÑÐºÐ¸ ÑÑÐ¸Ð³Ð³ÐµÑÐ¾Ð²."""
        self.running = False
