"""
ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð² ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°
"""

from typing import Dict, List, Optional
import asyncio


class SensorMonitor:
    """ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð² ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°."""

    def __init__(self, brain):
        self.brain = brain
        self.ha = brain.smart_home.get("home_assistant") if hasattr(brain, "smart_home") else None
        self.alerts = {}

    async def get_all_sensors(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð²ÑÐµ Ð´Ð°ÑÑÐ¸ÐºÐ¸."""
        states = await self.ha.get_states()
        if "error" in states:
            return []
        
        sensors = []
        for state in states:
            if state["entity_id"].startswith("sensor."):
                sensors.append({
                    "entity_id": state["entity_id"],
                    "name": state["attributes"].get("friendly_name", ""),
                    "value": state["state"],
                    "unit": state["attributes"].get("unit_of_measurement", ""),
                    "device_class": state["attributes"].get("device_class", ""),
                })
        
        return sensors

    async def get_temperature(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÑ."""
        sensors = await self.get_all_sensors()
        temps = [s for s in sensors if s.get("device_class") == "temperature"]
        if temps:
            return {
                "sensors": temps,
                "average": sum(float(t["value"]) for t in temps if t["value"] not in ["unknown", "unavailable"]) / len(temps) if temps else 0
            }
        return {"sensors": [], "average": 0}

    async def get_humidity(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð²Ð»Ð°Ð¶Ð½Ð¾ÑÑÑ."""
        sensors = await self.get_all_sensors()
        hums = [s for s in sensors if s.get("device_class") == "humidity"]
        return {"sensors": hums}

    async def get_motion_sensors(self) -> List[Dict]:
        """ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð´Ð²Ð¸Ð¶ÐµÐ½Ð¸Ñ."""
        sensors = await self.get_all_sensors()
        return [s for s in sensors if s.get("device_class") == "motion"]

    async def get_door_sensors(self) -> List[Dict]:
        """ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð´Ð²ÐµÑÐµÐ¹/Ð¾ÐºÐ¾Ð½."""
        sensors = await self.get_all_sensors()
        return [s for s in sensors if s.get("device_class") in ["door", "window", "opening"]]

    def set_alert(self, name: str, entity_id: str, condition: str, threshold: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ Ð¾Ð¿Ð¾Ð²ÐµÑÐµÐ½Ð¸Ðµ."""
        self.alerts[name] = {
            "entity_id": entity_id,
            "condition": condition,  # "above", "below"
            "threshold": threshold,
            "active": True
        }

    async def check_alerts(self) -> List[Dict]:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¾Ð¿Ð¾Ð²ÐµÑÐµÐ½Ð¸Ñ."""
        triggered = []
        for name, alert in self.alerts.items():
            if not alert["active"]:
                continue
            
            entity = await self.ha.get_entity(alert["entity_id"])
            if "error" in entity:
                continue
            
            try:
                value = float(entity["state"])
            except (ValueError, TypeError):
                continue
            
            if alert["condition"] == "above" and value > alert["threshold"]:
                triggered.append({
                    "name": name,
                    "entity_id": alert["entity_id"],
                    "value": value,
                    "threshold": alert["threshold"],
                    "message": f"{name}: Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ {value} Ð²ÑÑÐµ Ð¿Ð¾ÑÐ¾Ð³Ð° {alert['threshold']}"
                })
            elif alert["condition"] == "below" and value < alert["threshold"]:
                triggered.append({
                    "name": name,
                    "entity_id": alert["entity_id"],
                    "value": value,
                    "threshold": alert["threshold"],
                    "message": f"{name}: Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ {value} Ð½Ð¸Ð¶Ðµ Ð¿Ð¾ÑÐ¾Ð³Ð° {alert['threshold']}"
                })
        
        return triggered
