"""
ÐÐ»Ð°Ð½Ð¸ÑÐ¾Ð²ÑÐ¸Ðº Ð·Ð°Ð´Ð°Ñ JARVIS
"""

import schedule
import time
import threading
from typing import Dict, List, Callable
from datetime import datetime


class TaskScheduler:
    """ÐÐ»Ð°Ð½Ð¸ÑÐ¾Ð²ÑÐ¸Ðº Ð·Ð°Ð´Ð°Ñ."""

    def __init__(self, brain):
        self.brain = brain
        self.tasks: Dict[str, Dict] = {}
        self.running = False

    def add_task(self, name: str, time_str: str, callback: Callable, days: List[str] = None):
        """ÐÐ¾Ð±Ð°Ð²Ð¸ÑÑ Ð·Ð°Ð´Ð°ÑÑ."""
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
        
        self.brain.logger.info(f"ÐÐ°Ð´Ð°ÑÐ° '{name}' Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð° Ð½Ð° {time_str}")
        return {"status": "ok", "name": name}

    def remove_task(self, name: str):
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ Ð·Ð°Ð´Ð°ÑÑ."""
        if name in self.tasks:
            schedule.clear(name)
            del self.tasks[name]
            self.brain.logger.info(f"ÐÐ°Ð´Ð°ÑÐ° '{name}' ÑÐ´Ð°Ð»ÐµÐ½Ð°")
            return {"status": "ok"}
        return {"status": "error", "message": "ÐÐ°Ð´Ð°ÑÐ° Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}

    def list_tasks(self) -> List[Dict]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð·Ð°Ð´Ð°Ñ."""
        return [
            {"name": name, **data}
            for name, data in self.tasks.items()
        ]

    def start(self):
        """ÐÐ°Ð¿ÑÑÐº Ð¿Ð»Ð°Ð½Ð¸ÑÐ¾Ð²ÑÐ¸ÐºÐ°."""
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÐÑÐ½Ð¾Ð²Ð½Ð¾Ð¹ ÑÐ¸ÐºÐ» Ð¿Ð»Ð°Ð½Ð¸ÑÐ¾Ð²ÑÐ¸ÐºÐ°."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¿Ð»Ð°Ð½Ð¸ÑÐ¾Ð²ÑÐ¸ÐºÐ°."""
        self.running = False
        schedule.clear()
