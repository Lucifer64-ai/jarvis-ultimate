"""
ÐÑÑÐµÐ½ÑÐ¸ÑÐ¸ÐºÐ°ÑÐ¸Ñ Ð´Ð»Ñ Ð¼Ð¾Ð±Ð¸Ð»ÑÐ½Ð¾Ð³Ð¾ API
"""

import hashlib
import secrets
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta


class AuthManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð°ÑÑÐµÐ½ÑÐ¸ÑÐ¸ÐºÐ°ÑÐ¸ÐµÐ¹."""

    def __init__(self, brain):
        self.brain = brain
        self.users_file = Path("data/users.json")
        self.tokens_file = Path("data/api_tokens.json")
        self.users_file.parent.mkdir(exist_ok=True)
        
        self.users: Dict = self._load_users()
        self.tokens: Dict = self._load_tokens()

    def _load_users(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹."""
        if self.users_file.exists():
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def _save_users(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹."""
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=2)

    def _load_tokens(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° ÑÐ¾ÐºÐµÐ½Ð¾Ð²."""
        if self.tokens_file.exists():
            with open(self.tokens_file, "r") as f:
                return json.load(f)
        return {}

    def _save_tokens(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ ÑÐ¾ÐºÐµÐ½Ð¾Ð²."""
        with open(self.tokens_file, "w") as f:
            json.dump(self.tokens, f, indent=2)

    def _hash_password(self, password: str) -> str:
        """Ð¥ÐµÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¿Ð°ÑÐ¾Ð»Ñ."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str) -> Dict:
        """Ð ÐµÐ³Ð¸ÑÑÑÐ°ÑÐ¸Ñ Ð½Ð¾Ð²Ð¾Ð³Ð¾ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ."""
        if username in self.users:
            return {"status": "error", "message": "ÐÐ¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ ÑÐ¶Ðµ ÑÑÑÐµÑÑÐ²ÑÐµÑ"}
        
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "created": datetime.now().isoformat()
        }
        self._save_users()
        
        return {"status": "ok", "username": username}

    def authenticate(self, username: str, password: str) -> Dict:
        """ÐÑÑÐµÐ½ÑÐ¸ÑÐ¸ÐºÐ°ÑÐ¸Ñ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ."""
        if username not in self.users:
            return {"status": "error", "message": "ÐÐ¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
        
        user = self.users[username]
        if user["password_hash"] != self._hash_password(password):
            return {"status": "error", "message": "ÐÐµÐ²ÐµÑÐ½ÑÐ¹ Ð¿Ð°ÑÐ¾Ð»Ñ"}
        
        # ÐÐµÐ½ÐµÑÐ°ÑÐ¸Ñ ÑÐ¾ÐºÐµÐ½Ð°
        token = secrets.token_hex(32)
        self.tokens[token] = {
            "username": username,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=30)).isoformat()
        }
        self._save_tokens()
        
        return {"status": "ok", "token": token, "username": username}

    def verify_token(self, token: str) -> Optional[str]:
        """ÐÑÐ¾Ð²ÐµÑÐºÐ° ÑÐ¾ÐºÐµÐ½Ð°."""
        if token not in self.tokens:
            return None
        
        token_data = self.tokens[token]
        expires = datetime.fromisoformat(token_data["expires"])
        
        if datetime.now() > expires:
            del self.tokens[token]
            self._save_tokens()
            return None
        
        return token_data.get("username")

    def revoke_token(self, token: str) -> Dict:
        """ÐÑÐ·ÑÐ² ÑÐ¾ÐºÐµÐ½Ð°."""
        if token in self.tokens:
            del self.tokens[token]
            self._save_tokens()
            return {"status": "ok"}
        return {"status": "error", "message": "Ð¢Ð¾ÐºÐµÐ½ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}

    def list_users(self) -> list:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹."""
        return list(self.users.keys())

    def delete_user(self, username: str) -> Dict:
        """Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ."""
        if username in self.users:
            del self.users[username]
            self._save_users()
            return {"status": "ok"}
        return {"status": "error", "message": "ÐÐ¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½"}
