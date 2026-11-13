"""
ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ°ÃÂ¼ÃÂ¸ JARVIS
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
from send2trash import send2trash


class FileModule:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²ÃÂ¾ÃÂ¹ ÃÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ¾ÃÂ¹."""

    def __init__(self, brain):
        self.brain = brain

    def list_directory(self, path: str = ".") -> List[Dict]:
        """ÃÂ¡ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂº ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ² ÃÂ² ÃÂ´ÃÂ¸ÃÃÂµÃÂºÃÃÂ¾ÃÃÂ¸ÃÂ¸."""
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
        """ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"status": "ok", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_file(self, path: str) -> Dict:
        """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂ¸ÃÃ ÃÃÂ°ÃÂ¹ÃÂ» ÃÂ² ÃÂºÃÂ¾ÃÃÂ·ÃÂ¸ÃÂ½Ã."""
        try:
            send2trash(path)
            return {"status": "ok", "message": f"ÃÂ¤ÃÂ°ÃÂ¹ÃÂ» '{path}' ÃÂ¿ÃÂµÃÃÂµÃÂ¼ÃÂµÃÃÃÂ½ ÃÂ² ÃÂºÃÂ¾ÃÃÂ·ÃÂ¸ÃÂ½Ã"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def copy_file(self, src: str, dst: str) -> Dict:
        """ÃÃÂ¾ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»."""
        try:
            shutil.copy2(src, dst)
            return {"status": "ok", "src": src, "dst": dst}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def move_file(self, src: str, dst: str) -> Dict:
        """ÃÃÂµÃÃÂµÃÂ¼ÃÂµÃÃÃÂ¸ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»."""
        try:
            shutil.move(src, dst)
            return {"status": "ok", "src": src, "dst": dst}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_directory(self, path: str) -> Dict:
        """ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÃ ÃÂ´ÃÂ¸ÃÃÂµÃÂºÃÃÂ¾ÃÃÂ¸Ã."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return {"status": "ok", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
