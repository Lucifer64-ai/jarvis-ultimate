"""
ÃÂ¡ÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾ÃÃÂ¾ÃÂ² JARVIS
"""

import json
from pathlib import Path
from typing import Dict, List


class MacroManager:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾ÃÃÂ°ÃÂ¼ÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain
        self.macros_dir = Path("macros")
        self.macros_dir.mkdir(exist_ok=True)
        self.macros: Dict[str, Dict] = {}
        self._load_macros()

    def _load_macros(self):
        """ÃÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾ÃÃÂ¾ÃÂ² ÃÂ¸ÃÂ· ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²."""
        for file in self.macros_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.macros[file.stem] = data
            except Exception as e:
                self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾ÃÃÂ° {file}: {e}")

    def create_macro(self, name: str, commands: List[str]) -> Dict:
        """ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÃ ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾Ã."""
        macro = {
            "name": name,
            "commands": commands,
            "created": str(datetime.now())
        }
        
        file_path = self.macros_dir / f"{name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(macro, f, ensure_ascii=False, indent=2)
        
        self.macros[name] = macro
        return {"status": "ok", "name": name}

    def execute_macro(self, name: str) -> Dict:
        """ÃÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂ¸ÃÃ ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾Ã."""
        if name not in self.macros:
            return {"status": "error", "message": "ÃÃÂ°ÃÂºÃÃÂ¾Ã ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½"}
        
        macro = self.macros[name]
        results = []
        
        for command in macro["commands"]:
            result = self.brain.execute_command(command)
            results.append(result)
        
        return {"status": "ok", "results": results}

    def list_macros(self) -> List[str]:
        """ÃÂ¡ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾ÃÃÂ¾ÃÂ²."""
        return list(self.macros.keys())

    def delete_macro(self, name: str) -> Dict:
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÂ¼ÃÂ°ÃÂºÃÃÂ¾Ã."""
        if name in self.macros:
            file_path = self.macros_dir / f"{name}.json"
            if file_path.exists():
                file_path.unlink()
            del self.macros[name]
            return {"status": "ok"}
        return {"status": "error", "message": "ÃÃÂ°ÃÂºÃÃÂ¾Ã ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½"}
