"""
ÐÐ½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ JARVIS Ñ Home Assistant
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional
import json
import logging


class HomeAssistantIntegration:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ¼Ð½ÑÐ¼ Ð´Ð¾Ð¼Ð¾Ð¼ ÑÐµÑÐµÐ· Home Assistant."""

    def __init__(self, brain):
        self.brain = brain
        
        # Ð§ÑÐµÐ½Ð¸Ðµ Ð¸Ð· Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ
        self.url = brain.config.home_assistant_url
        self.token = brain.config.home_assistant_token
        
        if self.url and self.token:
            self.brain.logger.info(f"Home Assistant Ð¿Ð¾Ð´ÐºÐ»ÑÑÐµÐ½: {self.url}")
        else:
            self.brain.logger.warning("Home Assistant Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½. ÐÐ¾Ð±Ð°Ð²ÑÑÐµ HOME_ASSISTANT_URL Ð¸ HOME_ASSISTANT_TOKEN Ð² .env")
        
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        """Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ HTTP ÑÐµÑÑÐ¸Ð¸."""
        if not self.url or not self.token:
            raise Exception("Home Assistant Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½")
        
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
            )

    async def close(self):
        """ÐÐ°ÐºÑÑÑÐ¸Ðµ ÑÐµÑÑÐ¸Ð¸."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_states(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð²ÑÐµ ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ñ ÑÑÑÑÐ¾Ð¹ÑÑÐ²."""
        await self._ensure_session()
        try:
            async with self.session.get(f"{self.url}/api/states") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"error": f"Status {resp.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def get_entity(self, entity_id: str) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ ÐºÐ¾Ð½ÐºÑÐµÑÐ½Ð¾Ð³Ð¾ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð°."""
        await self._ensure_session()
        try:
            async with self.session.get(f"{self.url}/api/states/{entity_id}") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"error": f"Status {resp.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def call_service(self, domain: str, service: str, entity_id: str = None, **kwargs) -> Dict:
        """ÐÑÐ·Ð¾Ð² ÑÐµÑÐ²Ð¸ÑÐ° Home Assistant."""
        await self._ensure_session()
        
        data = kwargs.copy()
        if entity_id:
            data["entity_id"] = entity_id
        
        try:
            async with self.session.post(
                f"{self.url}/api/services/{domain}/{service}",
                json=data
            ) as resp:
                if resp.status == 200:
                    return {"status": "ok"}
                return {"error": f"Status {resp.status}"}
        except Exception as e:
            return {"error": str(e)}

    # === Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¾ÑÐ²ÐµÑÐµÐ½Ð¸ÐµÐ¼ ===

    async def turn_on_light(self, entity_id: str, brightness: int = None, color: tuple = None):
        """ÐÐºÐ»ÑÑÐ¸ÑÑ ÑÐ²ÐµÑ."""
        kwargs = {}
        if brightness:
            kwargs["brightness"] = int(brightness * 2.55)
        if color:
            kwargs["rgb_color"] = color
        
        return await self.call_service("light", "turn_on", entity_id, **kwargs)

    async def turn_off_light(self, entity_id: str):
        """ÐÑÐºÐ»ÑÑÐ¸ÑÑ ÑÐ²ÐµÑ."""
        return await self.call_service("light", "turn_off", entity_id)

    async def set_brightness(self, entity_id: str, brightness: int):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÑÐºÐ¾ÑÑÑ."""
        return await self.turn_on_light(entity_id, brightness=brightness)

    async def set_color(self, entity_id: str, r: int, g: int, b: int):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÐ²ÐµÑ."""
        return await self.turn_on_light(entity_id, color=(r, g, b))

    # === Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÐºÐ»Ð¸Ð¼Ð°ÑÐ¾Ð¼ ===

    async def set_temperature(self, entity_id: str, temperature: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÑ."""
        return await self.call_service(
            "climate", "set_temperature",
            entity_id, temperature=temperature
        )

    async def set_hvac_mode(self, entity_id: str, mode: str):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÐµÐ¶Ð¸Ð¼ HVAC."""
        return await self.call_service(
            "climate", "set_hvac_mode",
            entity_id, hvac_mode=mode
        )

    # === Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¼ÐµÐ´Ð¸Ð° ===

    async def media_play(self, entity_id: str):
        """ÐÐ¾ÑÐ¿ÑÐ¾Ð¸Ð·Ð²ÐµÑÑÐ¸ Ð¼ÐµÐ´Ð¸Ð°."""
        return await self.call_service("media_player", "media_play", entity_id)

    async def media_pause(self, entity_id: str):
        """ÐÐ°ÑÐ·Ð° Ð¼ÐµÐ´Ð¸Ð°."""
        return await self.call_service("media_player", "media_pause", entity_id)

    async def media_stop(self, entity_id: str):
        """ÐÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ Ð¼ÐµÐ´Ð¸Ð°."""
        return await self.call_service("media_player", "media_stop", entity_id)

    async def set_volume(self, entity_id: str, volume: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑ."""
        return await self.call_service(
            "media_player", "volume_set",
            entity_id, volume_level=volume
        )

    # === Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð·Ð°Ð¼ÐºÐ°Ð¼Ð¸ ===

    async def lock(self, entity_id: str):
        """ÐÐ°Ð±Ð»Ð¾ÐºÐ¸ÑÐ¾Ð²Ð°ÑÑ Ð·Ð°Ð¼Ð¾Ðº."""
        return await self.call_service("lock", "lock", entity_id)

    async def unlock(self, entity_id: str):
        """Ð Ð°Ð·Ð±Ð»Ð¾ÐºÐ¸ÑÐ¾Ð²Ð°ÑÑ Ð·Ð°Ð¼Ð¾Ðº."""
        return await self.call_service("lock", "unlock", entity_id)

    # === Ð¡ÑÐµÐ½Ñ Ð¸ ÑÐºÑÐ¸Ð¿ÑÑ ===

    async def activate_scene(self, entity_id: str):
        """ÐÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°ÑÑ ÑÑÐµÐ½Ñ."""
        return await self.call_service("scene", "turn_on", entity_id)

    async def run_script(self, entity_id: str):
        """ÐÐ°Ð¿ÑÑÑÐ¸ÑÑ ÑÐºÑÐ¸Ð¿Ñ."""
        return await self.call_service("script", "turn_on", entity_id)

    # === ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¸ ===

    async def get_lights(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐ¿Ð¸ÑÐ¾Ðº Ð²ÑÐµÑ ÑÐ²ÐµÑÐ¸Ð»ÑÐ½Ð¸ÐºÐ¾Ð²."""
        states = await self.get_states()
        if "error" in states:
            return []
        return [s for s in states if s["entity_id"].startswith("light.")]

    async def get_switches(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐ¿Ð¸ÑÐ¾Ðº Ð²ÑÐµÑ Ð²ÑÐºÐ»ÑÑÐ°ÑÐµÐ»ÐµÐ¹."""
        states = await self.get_states()
        if "error" in states:
            return []
        return [s for s in states if s["entity_id"].startswith("switch.")]

    async def get_sensors(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐ¿Ð¸ÑÐ¾Ðº Ð²ÑÐµÑ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð²."""
        states = await self.get_states()
        if "error" in states:
            return []
        return [s for s in states if s["entity_id"].startswith("sensor.")]

    async def get_cameras(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐ¿Ð¸ÑÐ¾Ðº ÐºÐ°Ð¼ÐµÑ."""
        states = await self.get_states()
        if "error" in states:
            return []
        return [s for s in states if s["entity_id"].startswith("camera.")]

    # === ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´ ===

    async def handle_command(self, command: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²Ð¾Ð¹ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð´Ð»Ñ ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°."""
        cmd = command.lower()
        
        # Ð¡Ð²ÐµÑ
        if "Ð²ÐºÐ»ÑÑÐ¸ ÑÐ²ÐµÑ" in cmd or "Ð·Ð°Ð¶Ð³Ð¸ ÑÐ²ÐµÑ" in cmd:
            lights = await self.get_lights()
            for light in lights:
                await self.turn_on_light(light["entity_id"])
            return {"response": f"ÐÐºÐ»ÑÑÐ°Ñ {len(lights)} ÑÐ²ÐµÑÐ¸Ð»ÑÐ½Ð¸ÐºÐ¾Ð²."}
        
        elif "Ð²ÑÐºÐ»ÑÑÐ¸ ÑÐ²ÐµÑ" in cmd or "Ð¿Ð¾ÑÑÑÐ¸ ÑÐ²ÐµÑ" in cmd:
            lights = await self.get_lights()
            for light in lights:
                await self.turn_off_light(light["entity_id"])
            return {"response": "ÐÑÐºÐ»ÑÑÐ°Ñ Ð²ÐµÑÑ ÑÐ²ÐµÑ."}
        
        # Ð¢ÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÐ°
        elif "ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑ" in cmd and any(c in cmd for c in ["20", "21", "22", "23", "24", "25"]):
            import re
            match = re.search(r'(\d+)', cmd)
            if match:
                temp = float(match.group(1))
                states = await self.get_states()
                climates = [s for s in states if s["entity_id"].startswith("climate.")]
                for climate in climates:
                    await self.set_temperature(climate["entity_id"], temp)
                return {"response": f"Ð£ÑÑÐ°Ð½Ð°Ð²Ð»Ð¸Ð²Ð°Ñ ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÑ {temp} Ð³ÑÐ°Ð´ÑÑÐ¾Ð²."}
        
        # Ð¡ÑÐµÐ½Ñ
        elif "ÑÑÐµÐ½" in cmd:
            states = await self.get_states()
            scenes = [s for s in states if s["entity_id"].startswith("scene.")]
            if scenes:
                await self.activate_scene(scenes[0]["entity_id"])
                return {"response": f"ÐÐºÑÐ¸Ð²Ð¸ÑÑÑ ÑÑÐµÐ½Ñ {scenes[0]['attributes'].get('friendly_name', '')}."}
        
        return {"response": "ÐÐµ Ð¿Ð¾Ð½Ð¸Ð¼Ð°Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð´Ð»Ñ ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°."}
