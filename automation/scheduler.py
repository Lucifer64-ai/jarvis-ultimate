"""
ÃÃÂ»ÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÃÂ¸ÃÂº ÃÂ·ÃÂ°ÃÂ´ÃÂ°Ã JARVIS
"""

import schedule
import time
import threading
from typing import Dict, List, Callable
from datetime import datetime


class TaskScheduler:
    """ÃÃÂ»ÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÃÂ¸ÃÂº ÃÂ·ÃÂ°ÃÂ´ÃÂ°Ã."""

    def __init__(self, brain):
        self.brain = brain
        self.tasks: Dict[str, Dict] = {}
        self.running = False

    def add_task(self, name: str, time_str: str, callback: Callable, days: List[str] = None):
        """ÃÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ¸ÃÃ ÃÂ·ÃÂ°ÃÂ´ÃÂ°ÃÃ."""
        job = schedule.every()
        
        if days:
            for day in days:
                getattr(job, day.lower()).at(time_str).do(callback)
        else:
            job.every().day.at(time_str).do(callback)
        
        self.tasks[name] = {
            "time": time_str,
            "days": days or ["every day"],
            "callback": callback.__name__,
            "created": datetime.now().isoformat()
        }
        
        self.brain.logger.info(f"ÃÃÂ°ÃÂ´ÃÂ°ÃÃÂ° '{name}' ÃÂ´ÃÂ¾ÃÂ±ÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ° ÃÂ½ÃÂ° {time_str}")
        return {"status": "ok", "name": name}

    def remove_task(self, name: str):
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÂ·ÃÂ°ÃÂ´ÃÂ°ÃÃ."""
        if name in self.tasks:
            schedule.clear(name)
            del self.tasks[name]
            self.brain.logger.info(f"ÃÃÂ°ÃÂ´ÃÂ°ÃÃÂ° '{name}' ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ°")
            return {"status": "ok"}
        return {"status": "error", "message": "ÃÃÂ°ÃÂ´ÃÂ°ÃÃÂ° ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ°"}

    def list_tasks(self) -> List[Dict]:
        """ÃÂ¡ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÂ·ÃÂ°ÃÂ´ÃÂ°Ã."""
        return [
            {"name": name, **data}
            for name, data in self.tasks.items()
        ]

    def start(self):
        """ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¿ÃÂ»ÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÃÂ¸ÃÂºÃÂ°."""
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÃÃÃÂ½ÃÂ¾ÃÂ²ÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂ¸ÃÂºÃÂ» ÃÂ¿ÃÂ»ÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÃÂ¸ÃÂºÃÂ°."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¿ÃÂ»ÃÂ°ÃÂ½ÃÂ¸ÃÃÂ¾ÃÂ²ÃÃÂ¸ÃÂºÃÂ°."""
        self.running = False
        schedule.clear()
