"""
ÃÃÂ¡ÃÃÃÂµÃÃÂ½Ã ÃÃÂ¸ ÃÃÂ°ÃÃÂ²ÃÃÃÂ¾ÃÃÂ¼ÃÃÂ°ÃÃÃÂ¸ÃÃÂ·ÃÃÂ°ÃÃÃÂ¸ÃÃÂ¸ ÃÃÃÂ¼ÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ°
"""

from typing import Dict, List
import json
from pathlib import Path


class SceneManager:
    """ÃÃÂ£ÃÃÂ¿ÃÃÃÂ°ÃÃÂ²ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÃÃÂµÃÃÂ½ÃÃÂ°ÃÃÂ¼ÃÃÂ¸ ÃÃÃÂ¼ÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ´ÃÃÂ¾ÃÃÂ¼ÃÃÂ°."""

    def __init__(self, brain):
        self.brain = brain
        self.ha = brain.smart_home.get("home_assistant") if hasattr(brain, "smart_home") else None
        self.custom_scenes_file = Path("data/custom_scenes.json")
        self.custom_scenes_file.parent.mkdir(exist_ok=True)
        self.custom_scenes = self._load_scenes()

    def _load_scenes(self) -> Dict:
        """ÃÃÃÂ°ÃÃÂ³ÃÃÃÃÂ·ÃÃÂºÃÃÂ° ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÂ·ÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÃÂµÃÃÂ»ÃÃÃÃÂºÃÃÂ¸Ã ÃÃÃÃÂµÃÃÂ½."""
        if self.custom_scenes_file.exists():
            with open(self.custom_scenes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_scenes(self):
        """ÃÃÂ¡ÃÃÂ¾ÃÃÃÃÂ°ÃÃÂ½ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÃÃÂµÃÃÂ½."""
        with open(self.custom_scenes_file, "w", encoding="utf-8") as f:
            json.dump(self.custom_scenes, f, ensure_ascii=False, indent=2)

    def create_scene(self, name: str, actions: List[Dict]) -> Dict:
        """ÃÃÂ¡ÃÃÂ¾ÃÃÂ·ÃÃÂ´ÃÃÂ°ÃÃ ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÂ·ÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÃÂµÃÃÂ»ÃÃÃÃÂºÃÃ ÃÃÃÃÂµÃÃÂ½Ã."""
        self.custom_scenes[name] = {"actions": actions}
        self._save_scenes()
        return {"status": "ok", "name": name}

    async def activate_scene(self, name: str) -> Dict:
        """ÃÃÃÂºÃÃÃÂ¸ÃÃÂ²ÃÃÂ¸ÃÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃ ÃÃÃÃÂµÃÃÂ½Ã."""
        # ÃÃÃÃÂ¾ÃÃÂ²ÃÃÂµÃÃÃÂ¸ÃÃ ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÂ·ÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÃÂµÃÃÂ»ÃÃÃÃÂºÃÃÂ¸ÃÃÂµ ÃÃÃÃÂµÃÃÂ½Ã
        if name in self.custom_scenes:
            scene = self.custom_scenes[name]
            results = []
            for action in scene["actions"]:
                result = await self._execute_action(action)
                results.append(result)
            return {"status": "ok", "scene": name, "results": results}
        
        # ÃÃÃÂ¾ÃÃÂ¸ÃÃÃÂº ÃÃÂ² Home Assistant
        states = await self.ha.get_states()
        for state in states:
            if state["entity_id"].startswith("scene."):
                friendly = state["attributes"].get("friendly_name", "").lower()
                if name.lower() in friendly or name.lower() in state["entity_id"]:
                    return await self.ha.activate_scene(state["entity_id"])
        
        return {"status": "error", "message": f"ÃÃÂ¡ÃÃÃÂµÃÃÂ½ÃÃÂ° '{name}' ÃÃÂ½ÃÃÂµ ÃÃÂ½ÃÃÂ°ÃÃÂ¹ÃÃÂ´ÃÃÂµÃÃÂ½ÃÃÂ°"}

    async def _execute_action(self, action: Dict) -> Dict:
        """ÃÃÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÂ½ÃÃÂ¸ÃÃ ÃÃÂ´ÃÃÂµÃÃÂ¹ÃÃÃÃÂ²ÃÃÂ¸ÃÃÂµ ÃÃÃÃÂµÃÃÂ½Ã."""
        domain = action.get("domain")
        service = action.get("service")
        entity_id = action.get("entity_id")
        data = action.get("data", {})
        
        return await self.ha.call_service(domain, service, entity_id, **data)

    def list_scenes(self) -> List[str]:
        """ÃÃÂ¡ÃÃÂ¿ÃÃÂ¸ÃÃÃÂ¾ÃÃÂº ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÂ·ÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÃÂµÃÃÂ»ÃÃÃÃÂºÃÃÂ¸Ã ÃÃÃÃÂµÃÃÂ½."""
        return list(self.custom_scenes.keys())

    def delete_scene(self, name: str) -> Dict:
        """ÃÃÂ£ÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂ¸ÃÃ ÃÃÃÃÂµÃÃÂ½Ã."""
        if name in self.custom_scenes:
            del self.custom_scenes[name]
            self._save_scenes()
            return {"status": "ok"}
        return {"status": "error", "message": "ÃÃÂ¡ÃÃÃÂµÃÃÂ½ÃÃÂ° ÃÃÂ½ÃÃÂµ ÃÃÂ½ÃÃÂ°ÃÃÂ¹ÃÃÂ´ÃÃÂµÃÃÂ½ÃÃÂ°"}
