"""
Ð¡Ð¸ÑÑÐµÐ¼Ð° Ð¼Ð°ÐºÑÐ¾ÑÐ¾Ð² JARVIS
"""

import json
from pathlib import Path
from typing import Dict, List


class MacroManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¼Ð°ÐºÑÐ¾ÑÐ°Ð¼Ð¸."""

    def __init__(self, brain):
        self.brain = brain
        self.macros_dir = Path("macros")
        self.macros_dir.mkdir(exist_ok=True)
        self.macros: Dict[str, Dict] = {}
        self._load_macros()

    def _load_macros(self):
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¼Ð°ÐºÑÐ¾ÑÐ¾Ð² Ð¸Ð· ÑÐ°Ð¹Ð»Ð¾Ð²."""
        for file in self.macros_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.macros[file.stem] = data
            except Exception as e:
                self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð°ÐºÑÐ¾ÑÐ° {file}: {e}")

    def create_macro(self, name: str, commands: List[str]) -> Dict:
        """Ð¡Ð¾Ð·Ð´Ð°ÑÑ Ð¼Ð°ÐºÑÐ¾Ñ."""
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
        """ÐÑÐ¿Ð¾Ð»Ð½Ð¸ÑÑ Ð¼Ð°ÐºÑÐ¾Ñ."""
        if name not in self.macros:
            return {"status": "error", "message": "ÐÐ°ÐºÑÐ¾Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
        
        macro = self.macros[name]
        results = []
        
        for command in macro["commands"]:
            result = self.brain.execute_command(command)
            results.append(result)
        
        return {"status": "ok", "results": results}

    def list_macros(self) -> List[str]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð¼Ð°ÐºÑÐ¾ÑÐ¾Ð²."""
        return list(self.macros.keys())

    def delete_macro(self, name: str) -> Dict:
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ Ð¼Ð°ÐºÑÐ¾Ñ."""
        if name in self.macros:
            file_path = self.macros_dir / f"{name}.json"
            if file_path.exists():
                file_path.unlink()
            del self.macros[name]
            return {"status": "ok"}
        return {"status": "error", "message": "ÐÐ°ÐºÑÐ¾Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
