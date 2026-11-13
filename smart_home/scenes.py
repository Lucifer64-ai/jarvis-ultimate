"""
ÃÂ¡ÃÃÂµÃÂ½Ã ÃÂ¸ ÃÂ°ÃÂ²ÃÃÂ¾ÃÂ¼ÃÂ°ÃÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÃÂ¼ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ´ÃÂ¾ÃÂ¼ÃÂ°
"""

from typing import Dict, List
import json
from pathlib import Path


class SceneManager:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÃÂµÃÂ½ÃÂ°ÃÂ¼ÃÂ¸ ÃÃÂ¼ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ´ÃÂ¾ÃÂ¼ÃÂ°."""

    def __init__(self, brain):
        self.brain = brain
        self.ha = brain.smart_home.get("home_assistant") if hasattr(brain, "smart_home") else None
        self.custom_scenes_file = Path("data/custom_scenes.json")
        self.custom_scenes_file.parent.mkdir(exist_ok=True)
        self.custom_scenes = self._load_scenes()

    def _load_scenes(self) -> Dict:
        """ÃÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»ÃÃÃÂºÃÂ¸Ã ÃÃÃÂµÃÂ½."""
        if self.custom_scenes_file.exists():
            with open(self.custom_scenes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_scenes(self):
        """ÃÂ¡ÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÃÂµÃÂ½."""
        with open(self.custom_scenes_file, "w", encoding="utf-8") as f:
            json.dump(self.custom_scenes, f, ensure_ascii=False, indent=2)

    def create_scene(self, name: str, actions: List[Dict]) -> Dict:
        """ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»ÃÃÃÂºÃÃ ÃÃÃÂµÃÂ½Ã."""
        self.custom_scenes[name] = {"actions": actions}
        self._save_scenes()
        return {"status": "ok", "name": name}

    async def activate_scene(self, name: str) -> Dict:
        """ÃÃÂºÃÃÂ¸ÃÂ²ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÃ ÃÃÃÂµÃÂ½Ã."""
        # ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂ¸ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»ÃÃÃÂºÃÂ¸ÃÂµ ÃÃÃÂµÃÂ½Ã
        if name in self.custom_scenes:
            scene = self.custom_scenes[name]
            results = []
            for action in scene["actions"]:
                result = await self._execute_action(action)
                results.append(result)
            return {"status": "ok", "scene": name, "results": results}
        
        # ÃÃÂ¾ÃÂ¸ÃÃÂº ÃÂ² Home Assistant
        states = await self.ha.get_states()
        for state in states:
            if state["entity_id"].startswith("scene."):
                friendly = state["attributes"].get("friendly_name", "").lower()
                if name.lower() in friendly or name.lower() in state["entity_id"]:
                    return await self.ha.activate_scene(state["entity_id"])
        
        return {"status": "error", "message": f"ÃÂ¡ÃÃÂµÃÂ½ÃÂ° '{name}' ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ°"}

    async def _execute_action(self, action: Dict) -> Dict:
        """ÃÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂ¸ÃÃ ÃÂ´ÃÂµÃÂ¹ÃÃÃÂ²ÃÂ¸ÃÂµ ÃÃÃÂµÃÂ½Ã."""
        domain = action.get("domain")
        service = action.get("service")
        entity_id = action.get("entity_id")
        data = action.get("data", {})
        
        return await self.ha.call_service(domain, service, entity_id, **data)

    def list_scenes(self) -> List[str]:
        """ÃÂ¡ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»ÃÃÃÂºÃÂ¸Ã ÃÃÃÂµÃÂ½."""
        return list(self.custom_scenes.keys())

    def delete_scene(self, name: str) -> Dict:
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÃÃÂµÃÂ½Ã."""
        if name in self.custom_scenes:
            del self.custom_scenes[name]
            self._save_scenes()
            return {"status": "ok"}
        return {"status": "error", "message": "ÃÂ¡ÃÃÂµÃÂ½ÃÂ° ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ°"}
