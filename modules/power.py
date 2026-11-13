"""
Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿Ð¸ÑÐ°Ð½Ð¸ÐµÐ¼ JARVIS
"""

import psutil
from typing import Dict


class PowerModule:
    """ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ."""

    def __init__(self, brain):
        self.brain = brain

    def get_battery_info(self) -> Dict:
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ Ð±Ð°ÑÐ°ÑÐµÐµ."""
        battery = psutil.sensors_battery()
        if battery is None:
            return {"status": "ok", "available": False}

        return {
            "status": "ok",
            "available": True,
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "charging": battery.power_plugged and battery.percent < 100
        }

    def get_power_status(self) -> Dict:
        """Ð¡ÑÐ°ÑÑÑ Ð¿Ð¸ÑÐ°Ð½Ð¸Ñ."""
        battery = self.get_battery_info()
        if not battery.get("available"):
            return {"status": "ok", "source": "AC", "message": "ÐÐ¸ÑÐ°Ð½Ð¸Ðµ Ð¾Ñ ÑÐµÑÐ¸"}

        if battery.get("plugged"):
            return {"status": "ok", "source": "AC", "percent": battery["percent"]}
        else:
            return {"status": "ok", "source": "battery", "percent": battery["percent"]}
