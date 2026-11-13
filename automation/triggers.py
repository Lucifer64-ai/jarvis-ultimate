"""
ÃÂ¡ÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ¾ÃÂ² JARVIS
"""

from typing import Dict, List, Callable
import threading
import time


class TriggerManager:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ°ÃÂ¼ÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain
        self.triggers: Dict[str, Dict] = {}
        self.running = False

    def add_trigger(self, name: str, condition: Callable, action: Callable):
        """ÃÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ¸ÃÃ ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃ."""
        self.triggers[name] = {
            "condition": condition,
            "action": action,
            "active": True
        }
        self.brain.logger.info(f"ÃÂ¢ÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃ '{name}' ÃÂ´ÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½")
        return {"status": "ok", "name": name}

    def remove_trigger(self, name: str):
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃ."""
        if name in self.triggers:
            del self.triggers[name]
            return {"status": "ok"}
        return {"status": "error", "message": "ÃÂ¢ÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃ ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½"}

    def list_triggers(self) -> List[str]:
        """ÃÂ¡ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ¾ÃÂ²."""
        return list(self.triggers.keys())

    def start(self):
        """ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ¸ ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ¾ÃÂ²."""
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÃÃÃÂ½ÃÂ¾ÃÂ²ÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂ¸ÃÂºÃÂ» ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ¸ ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ¾ÃÂ²."""
        while self.running:
            for name, trigger in self.triggers.items():
                if not trigger["active"]:
                    continue
                
                try:
                    if trigger["condition"]():
                        self.brain.logger.info(f"ÃÂ¢ÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃ '{name}' ÃÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂ°ÃÂ»")
                        trigger["action"]()
                except Exception as e:
                    self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ° '{name}': {e}")
            
            time.sleep(5)

    def stop(self):
        """ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ¸ ÃÃÃÂ¸ÃÂ³ÃÂ³ÃÂµÃÃÂ¾ÃÂ²."""
        self.running = False
