"""
Ð¡ÑÐµÐ½Ñ Ð¸ Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸Ð·Ð°ÑÐ¸Ð¸ ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°
"""

from typing import Dict, List
import json
from pathlib import Path


class SceneManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÐµÐ½Ð°Ð¼Ð¸ ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°."""

    def __init__(self, brain):
        self.brain = brain
        self.ha = brain.smart_home.get("home_assistant") if hasattr(brain, "smart_home") else None
        self.custom_scenes_file = Path("data/custom_scenes.json")
        self.custom_scenes_file.parent.mkdir(exist_ok=True)
        self.custom_scenes = self._load_scenes()

    def _load_scenes(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÑÐºÐ¸Ñ ÑÑÐµÐ½."""
        if self.custom_scenes_file.exists():
            with open(self.custom_scenes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_scenes(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ ÑÑÐµÐ½."""
        with open(self.custom_scenes_file, "w", encoding="utf-8") as f:
            json.dump(self.custom_scenes, f, ensure_ascii=False, indent=2)

    def create_scene(self, name: str, actions: List[Dict]) -> Dict:
        """Ð¡Ð¾Ð·Ð´Ð°ÑÑ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÑÐºÑÑ ÑÑÐµÐ½Ñ."""
        self.custom_scenes[name] = {"actions": actions}
        self._save_scenes()
        return {"status": "ok", "name": name}

    async def activate_scene(self, name: str) -> Dict:
        """ÐÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°ÑÑ ÑÑÐµÐ½Ñ."""
        # ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÑÐºÐ¸Ðµ ÑÑÐµÐ½Ñ
        if name in self.custom_scenes:
            scene = self.custom_scenes[name]
            results = []
            for action in scene["actions"]:
                result = await self._execute_action(action)
                results.append(result)
            return {"status": "ok", "scene": name, "results": results}
        
        # ÐÐ¾Ð¸ÑÐº Ð² Home Assistant
        states = await self.ha.get_states()
        for state in states:
            if state["entity_id"].startswith("scene."):
                friendly = state["attributes"].get("friendly_name", "").lower()
                if name.lower() in friendly or name.lower() in state["entity_id"]:
                    return await self.ha.activate_scene(state["entity_id"])
        
        return {"status": "error", "message": f"Ð¡ÑÐµÐ½Ð° '{name}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}

    async def _execute_action(self, action: Dict) -> Dict:
        """ÐÑÐ¿Ð¾Ð»Ð½Ð¸ÑÑ Ð´ÐµÐ¹ÑÑÐ²Ð¸Ðµ ÑÑÐµÐ½Ñ."""
        domain = action.get("domain")
        service = action.get("service")
        entity_id = action.get("entity_id")
        data = action.get("data", {})
        
        return await self.ha.call_service(domain, service, entity_id, **data)

    def list_scenes(self) -> List[str]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÑÐºÐ¸Ñ ÑÑÐµÐ½."""
        return list(self.custom_scenes.keys())

    def delete_scene(self, name: str) -> Dict:
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ ÑÑÐµÐ½Ñ."""
        if name in self.custom_scenes:
            del self.custom_scenes[name]
            self._save_scenes()
            return {"status": "ok"}
        return {"status": "error", "message": "Ð¡ÑÐµÐ½Ð° Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}
