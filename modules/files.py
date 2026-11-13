"""
Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ°Ð¹Ð»Ð°Ð¼Ð¸ JARVIS
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
from send2trash import send2trash


class FileModule:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ°Ð¹Ð»Ð¾Ð²Ð¾Ð¹ ÑÐ¸ÑÑÐµÐ¼Ð¾Ð¹."""

    def __init__(self, brain):
        self.brain = brain

    def list_directory(self, path: str = ".") -> List[Dict]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº ÑÐ°Ð¹Ð»Ð¾Ð² Ð² Ð´Ð¸ÑÐµÐºÑÐ¾ÑÐ¸Ð¸."""
        try:
            items = []
            for item in Path(path).iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })
            return items
        except Exception as e:
            return [{"error": str(e)}]

    def create_file(self, path: str, content: str = "") -> Dict:
        """Ð¡Ð¾Ð·Ð´Ð°ÑÑ ÑÐ°Ð¹Ð»."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"status": "ok", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_file(self, path: str) -> Dict:
        """Ð£Ð´Ð°Ð»Ð¸ÑÑ ÑÐ°Ð¹Ð» Ð² ÐºÐ¾ÑÐ·Ð¸Ð½Ñ."""
        try:
            send2trash(path)
            return {"status": "ok", "message": f"Ð¤Ð°Ð¹Ð» '{path}' Ð¿ÐµÑÐµÐ¼ÐµÑÑÐ½ Ð² ÐºÐ¾ÑÐ·Ð¸Ð½Ñ"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def copy_file(self, src: str, dst: str) -> Dict:
        """ÐÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°ÑÑ ÑÐ°Ð¹Ð»."""
        try:
            shutil.copy2(src, dst)
            return {"status": "ok", "src": src, "dst": dst}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def move_file(self, src: str, dst: str) -> Dict:
        """ÐÐµÑÐµÐ¼ÐµÑÑÐ¸ÑÑ ÑÐ°Ð¹Ð»."""
        try:
            shutil.move(src, dst)
            return {"status": "ok", "src": src, "dst": dst}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_directory(self, path: str) -> Dict:
        """Ð¡Ð¾Ð·Ð´Ð°ÑÑ Ð´Ð¸ÑÐµÐºÑÐ¾ÑÐ¸Ñ."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return {"status": "ok", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
