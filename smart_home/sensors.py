"""
ÃÃÂ¾ÃÂ½ÃÂ¸ÃÃÂ¾ÃÃÂ¸ÃÂ½ÃÂ³ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¾ÃÂ² ÃÃÂ¼ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ´ÃÂ¾ÃÂ¼ÃÂ°
"""

from typing import Dict, List, Optional
import asyncio


class SensorMonitor:
    """ÃÃÂ¾ÃÂ½ÃÂ¸ÃÃÂ¾ÃÃÂ¸ÃÂ½ÃÂ³ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¾ÃÂ² ÃÃÂ¼ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ´ÃÂ¾ÃÂ¼ÃÂ°."""

    def __init__(self, brain):
        self.brain = brain
        self.ha = brain.smart_home.get("home_assistant") if hasattr(brain, "smart_home") else None
        self.alerts = {}

    async def get_all_sensors(self) -> List[Dict]:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ²ÃÃÂµ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸."""
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
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÃÂµÃÂ¼ÃÂ¿ÃÂµÃÃÂ°ÃÃÃÃ."""
        sensors = await self.get_all_sensors()
        temps = [s for s in sensors if s.get("device_class") == "temperature"]
        if temps:
            return {
                "sensors": temps,
                "average": sum(float(t["value"]) for t in temps if t["value"] not in ["unknown", "unavailable"]) / len(temps) if temps else 0
            }
        return {"sensors": [], "average": 0}

    async def get_humidity(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ²ÃÂ»ÃÂ°ÃÂ¶ÃÂ½ÃÂ¾ÃÃÃ."""
        sensors = await self.get_all_sensors()
        hums = [s for s in sensors if s.get("device_class") == "humidity"]
        return {"sensors": hums}

    async def get_motion_sensors(self) -> List[Dict]:
        """ÃÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸ ÃÂ´ÃÂ²ÃÂ¸ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        sensors = await self.get_all_sensors()
        return [s for s in sensors if s.get("device_class") == "motion"]

    async def get_door_sensors(self) -> List[Dict]:
        """ÃÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸ ÃÂ´ÃÂ²ÃÂµÃÃÂµÃÂ¹/ÃÂ¾ÃÂºÃÂ¾ÃÂ½."""
        sensors = await self.get_all_sensors()
        return [s for s in sensors if s.get("device_class") in ["door", "window", "opening"]]

    def set_alert(self, name: str, entity_id: str, condition: str, threshold: float):
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ¸ÃÃ ÃÂ¾ÃÂ¿ÃÂ¾ÃÂ²ÃÂµÃÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        self.alerts[name] = {
            "entity_id": entity_id,
            "condition": condition,  # "above", "below"
            "threshold": threshold,
            "active": True
        }

    async def check_alerts(self) -> List[Dict]:
        """ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂ¸ÃÃ ÃÂ¾ÃÂ¿ÃÂ¾ÃÂ²ÃÂµÃÃÂµÃÂ½ÃÂ¸Ã."""
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
                    "message": f"{name}: ÃÂ·ÃÂ½ÃÂ°ÃÃÂµÃÂ½ÃÂ¸ÃÂµ {value} ÃÂ²ÃÃÃÂµ ÃÂ¿ÃÂ¾ÃÃÂ¾ÃÂ³ÃÂ° {alert['threshold']}"
                })
            elif alert["condition"] == "below" and value < alert["threshold"]:
                triggered.append({
                    "name": name,
                    "entity_id": alert["entity_id"],
                    "value": value,
                    "threshold": alert["threshold"],
                    "message": f"{name}: ÃÂ·ÃÂ½ÃÂ°ÃÃÂµÃÂ½ÃÂ¸ÃÂµ {value} ÃÂ½ÃÂ¸ÃÂ¶ÃÂµ ÃÂ¿ÃÂ¾ÃÃÂ¾ÃÂ³ÃÂ° {alert['threshold']}"
                })
        
        return triggered
