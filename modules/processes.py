"""
Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿ÑÐ¾ÑÐµÑÑÐ°Ð¼Ð¸ JARVIS
"""

import psutil
from typing import Dict, List


class ProcessModule:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿ÑÐ¾ÑÐµÑÑÐ°Ð¼Ð¸ ÑÐ¸ÑÑÐµÐ¼Ñ."""

    def __init__(self, brain):
        self.brain = brain

    def list_processes(self, limit: int = 20) -> List[Dict]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð·Ð°Ð¿ÑÑÐµÐ½Ð½ÑÑ Ð¿ÑÐ¾ÑÐµÑÑÐ¾Ð²."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu": round(proc.info['cpu_percent'], 1),
                    "memory": round(proc.info['memory_percent'], 1)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        processes.sort(key=lambda x: x['cpu'], reverse=True)
        return processes[:limit]

    def kill_process(self, name: str) -> Dict:
        """ÐÐ°Ð²ÐµÑÑÐ¸ÑÑ Ð¿ÑÐ¾ÑÐµÑÑ Ð¿Ð¾ Ð¸Ð¼ÐµÐ½Ð¸."""
        killed = []
        for proc in psutil.process_iter(['name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed:
            return {"status": "ok", "killed": killed}
        return {"status": "error", "message": f"ÐÑÐ¾ÑÐµÑÑ '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}

    def get_process_info(self, name: str) -> Dict:
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ Ð¿ÑÐ¾ÑÐµÑÑÐµ."""
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                if name.lower() in proc.info['name'].lower():
                    return {
                        "status": "ok",
                        "process": {
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cpu": round(proc.info['cpu_percent'], 1),
                            "memory": round(proc.info['memory_percent'], 1),
                            "status": proc.info['status']
                        }
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return {"status": "error", "message": f"ÐÑÐ¾ÑÐµÑÑ '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
