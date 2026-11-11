"""
ÐÐµÐ½ÐµÐ´Ð¶ÐµÑ Ð¿Ð»Ð°Ð³Ð¸Ð½Ð¾Ð² JARVIS
"""

import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional


class PluginManager:
    """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¸ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¿Ð»Ð°Ð³Ð¸Ð½Ð°Ð¼Ð¸."""

    def __init__(self, brain):
        self.brain = brain
        self.plugins_dir = Path("plugins")
        self.plugins_dir.mkdir(exist_ok=True)
        self.loaded: Dict[str, object] = {}

    def discover_plugins(self) -> List[str]:
        plugins = []
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "plugin.py").exists():
                plugins.append(item.name)
            elif item.suffix == ".py" and item.name != "__init__.py":
                plugins.append(item.stem)
        return plugins

    def load_plugin(self, name: str) -> Dict:
        try:
            plugin_path = self.plugins_dir / name
            if plugin_path.is_dir():
                spec = importlib.util.spec_from_file_location(
                    name, str(plugin_path / "plugin.py")
                )
            else:
                spec = importlib.util.spec_from_file_location(
                    name, str(self.plugins_dir / f"{name}.py")
                )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "setup"):
                plugin = module.setup(self.brain)
                self.loaded[name] = plugin
                self.brain.logger.info(f"ÐÐ»Ð°Ð³Ð¸Ð½ '{name}' Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
                return {"status": "ok", "name": name}
            else:
                return {"status": "error", "message": "ÐÐ»Ð°Ð³Ð¸Ð½ Ð½Ðµ Ð¸Ð¼ÐµÐµÑ ÑÑÐ½ÐºÑÐ¸Ð¸ setup()"}
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¿Ð»Ð°Ð³Ð¸Ð½Ð° {name}: {e}")
            return {"status": "error", "message": str(e)}


    def load_plugins(self) -> List[Dict]:
        """Загрузить все обнаруженные плагины."""
        results = []
        plugins = self.discover_plugins()
        for name in plugins:
            result = self.load_plugin(name)
            results.append(result)
        return results

    def unload_plugin(self, name: str) -> Dict:
        if name in self.loaded:
            plugin = self.loaded[name]
            if hasattr(plugin, "shutdown"):
                plugin.shutdown()
            del self.loaded[name]
            return {"status": "ok"}
        return {"status": "error", "message": "ÐÐ»Ð°Ð³Ð¸Ð½ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}

    def list_plugins(self) -> List[Dict]:
        available = self.discover_plugins()
        return [
            {"name": name, "loaded": name in self.loaded}
            for name in available
        ]

    def get_plugin(self, name: str) -> Optional[object]:
        return self.loaded.get(name)
