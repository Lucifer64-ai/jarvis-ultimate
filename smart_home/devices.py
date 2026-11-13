"""
Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð°Ð¼Ð¸ ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°
"""

from typing import Dict, List, Optional
import asyncio


class DeviceManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð°Ð¼Ð¸ ÑÐµÑÐµÐ· Home Assistant."""

    def __init__(self, brain):
        self.brain = brain
        self.ha = brain.smart_home.get("home_assistant") if hasattr(brain, "smart_home") else None
        self.device_aliases = {}

    def set_alias(self, name: str, entity_id: str):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ Ð¿ÑÐµÐ²Ð´Ð¾Ð½Ð¸Ð¼ Ð´Ð»Ñ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð°."""
        self.device_aliases[name.lower()] = entity_id

    def get_entity_id(self, name: str) -> Optional[str]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ entity_id Ð¿Ð¾ Ð¸Ð¼ÐµÐ½Ð¸."""
        return self.device_aliases.get(name.lower())

    async def turn_on(self, name: str) -> Dict:
        """ÐÐºÐ»ÑÑÐ¸ÑÑ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð¾."""
        entity_id = self.get_entity_id(name)
        if not entity_id:
            return {"status": "error", "message": f"Ð£ÑÑÑÐ¾Ð¹ÑÑÐ²Ð¾ '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}
        
        domain = entity_id.split(".")[0]
        return await self.ha.call_service(domain, "turn_on", entity_id)

    async def turn_off(self, name: str) -> Dict:
        """ÐÑÐºÐ»ÑÑÐ¸ÑÑ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð¾."""
        entity_id = self.get_entity_id(name)
        if not entity_id:
            return {"status": "error", "message": f"Ð£ÑÑÑÐ¾Ð¹ÑÑÐ²Ð¾ '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}
        
        domain = entity_id.split(".")[0]
        return await self.ha.call_service(domain, "turn_off", entity_id)

    async def get_status(self, name: str) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÑÐ°ÑÑÑ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð°."""
        entity_id = self.get_entity_id(name)
        if not entity_id:
            return {"status": "error", "message": f"Ð£ÑÑÑÐ¾Ð¹ÑÑÐ²Ð¾ '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}
        
        return await self.ha.get_entity(entity_id)

    async def list_devices(self) -> List[Dict]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð²ÑÐµÑ ÑÑÑÑÐ¾Ð¹ÑÑÐ²."""
        states = await self.ha.get_states()
        if "error" in states:
            return []
        
        devices = []
        for state in states:
            domain = state["entity_id"].split(".")[0]
            if domain in ["light", "switch", "climate", "media_player", "lock", "sensor", "camera"]:
                devices.append({
                    "entity_id": state["entity_id"],
                    "name": state["attributes"].get("friendly_name", state["entity_id"]),
                    "state": state["state"],
                    "domain": domain,
                })
        
        return devices
