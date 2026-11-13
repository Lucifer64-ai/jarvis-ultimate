"""
API ÑÐµÑÐ²ÐµÑ JARVIS Ð´Ð»Ñ Ð¼Ð¾Ð±Ð¸Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ
"""

import asyncio
import json
import hashlib
import secrets
from typing import Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path

try:
    from aiohttp import web
except ImportError:
    print("Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÐµ: pip install aiohttp")


class MobileServer:
    """HTTP/WebSocket ÑÐµÑÐ²ÐµÑ Ð´Ð»Ñ Ð¼Ð¾Ð±Ð¸Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""

    def __init__(self, brain):
        self.brain = brain
        
        # Ð§ÑÐµÐ½Ð¸Ðµ Ð¸Ð· Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ
        self.host = brain.config.mobile_api_host
        self.port = brain.config.mobile_api_port
        self.secret = brain.config.mobile_api_secret
        
        self.app = web.Application()
        self.tokens: Dict[str, Dict] = {}
        self.tokens_file = Path("data/api_tokens.json")
        self._load_tokens()
        self._setup_routes()

    def _load_tokens(self):
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° API ÑÐ¾ÐºÐµÐ½Ð¾Ð²."""
        if self.tokens_file.exists():
            with open(self.tokens_file, "r") as f:
                self.tokens = json.load(f)

    def _save_tokens(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ ÑÐ¾ÐºÐµÐ½Ð¾Ð²."""
        self.tokens_file.parent.mkdir(exist_ok=True)
        with open(self.tokens_file, "w") as f:
            json.dump(self.tokens, f, indent=2)

    def _setup_routes(self):
        """ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° Ð¼Ð°ÑÑÑÑÑÐ¾Ð²."""
        self.app.router.add_post("/api/auth/login", self.handle_login)
        self.app.router.add_post("/api/auth/register", self.handle_register)
        self.app.router.add_get("/api/status", self.handle_status)
        self.app.router.add_post("/api/command", self.handle_command)
        self.app.router.add_get("/api/system", self.handle_system_info)
        self.app.router.add_get("/api/devices", self.handle_devices)
        self.app.router.add_post("/api/device/control", self.handle_device_control)
        self.app.router.add_get("/api/sensors", self.handle_sensors)
        self.app.router.add_get("/ws", self.websocket_handler)

    def _verify_token(self, request) -> Optional[str]:
        """ÐÑÐ¾Ð²ÐµÑÐºÐ° ÑÐ¾ÐºÐµÐ½Ð° Ð°Ð²ÑÐ¾ÑÐ¸Ð·Ð°ÑÐ¸Ð¸."""
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
            if token in self.tokens:
                return self.tokens[token].get("username")
        return None

    async def handle_login(self, request):
        """ÐÐ²ÑÐ¾ÑÐ¸Ð·Ð°ÑÐ¸Ñ."""
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        token = secrets.token_hex(32)
        self.tokens[token] = {
            "username": username,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=30)).isoformat()
        }
        self._save_tokens()
        
        return web.json_response({"token": token, "username": username})

    async def handle_register(self, request):
        """Ð ÐµÐ³Ð¸ÑÑÑÐ°ÑÐ¸Ñ Ð½Ð¾Ð²Ð¾Ð³Ð¾ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð°."""
        data = await request.json()
        device_name = data.get("device_name")
        
        token = secrets.token_hex(32)
        self.tokens[token] = {
            "device": device_name,
            "created": datetime.now().isoformat(),
            "type": "device"
        }
        self._save_tokens()
        
        return web.json_response({"token": token, "device": device_name})

    async def handle_status(self, request):
        """Ð¡ÑÐ°ÑÑÑ JARVIS."""
        user = self._verify_token(request)
        if not user:
            return web.json_response({"error": "Unauthorized"}, status=401)
        
        status = self.brain.get_status()
        return web.json_response(status)

    async def handle_command(self, request):
        """ÐÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²Ð¾Ð¹ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        user = self._verify_token(request)
        if not user:
            return web.json_response({"error": "Unauthorized"}, status=401)
        
        data = await request.json()
        command = data.get("command", "")
        
        result = self.brain.execute_command(command)
        return web.json_response(result)

    async def handle_system_info(self, request):
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ ÑÐ¸ÑÑÐµÐ¼Ðµ."""
        user = self._verify_token(request)
        if not user:
            return web.json_response({"error": "Unauthorized"}, status=401)
        
        info = self.brain.modules["hardware"].get_full_report()
        return web.json_response(info)

    async def handle_devices(self, request):
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº ÑÑÑÑÐ¾Ð¹ÑÑÐ² ÑÐ¼Ð½Ð¾Ð³Ð¾ Ð´Ð¾Ð¼Ð°."""
        user = self._verify_token(request)
        if not user:
            return web.json_response({"error": "Unauthorized"}, status=401)
        
        if hasattr(self.brain, "smart_home") and "home_assistant" in self.brain.smart_home:
            ha = self.brain.smart_home["home_assistant"]
            devices = await ha.get_states()
            return web.json_response({"devices": devices})
        
        return web.json_response({"devices": [], "message": "Home Assistant Ð½Ðµ Ð¿Ð¾Ð´ÐºÐ»ÑÑÐµÐ½"})

    async def handle_device_control(self, request):
        """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÑÑÑÐ¾Ð¹ÑÑÐ²Ð¾Ð¼."""
        user = self._verify_token(request)
        if not user:
            return web.json_response({"error": "Unauthorized"}, status=401)
        
        data = await request.json()
        entity_id = data.get("entity_id")
        action = data.get("action")
        
        if hasattr(self.brain, "smart_home") and "home_assistant" in self.brain.smart_home:
            ha = self.brain.smart_home["home_assistant"]
            domain = entity_id.split(".")[0]
            
            if action == "on":
                result = await ha.call_service(domain, "turn_on", entity_id)
            elif action == "off":
                result = await ha.call_service(domain, "turn_off", entity_id)
            elif action == "toggle":
                result = await ha.call_service(domain, "toggle", entity_id)
            else:
                return web.json_response({"error": "Unknown action"}, status=400)
            
            return web.json_response(result)
        
        return web.json_response({"error": "Home Assistant not connected"}, status=503)

    async def handle_sensors(self, request):
        """ÐÐ°Ð½Ð½ÑÐµ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð²."""
        user = self._verify_token(request)
        if not user:
            return web.json_response({"error": "Unauthorized"}, status=401)
        
        if hasattr(self.brain, "smart_home") and "home_assistant" in self.brain.smart_home:
            ha = self.brain.smart_home["home_assistant"]
            states = await ha.get_states()
            sensors = [s for s in states if s["entity_id"].startswith("sensor.")]
            return web.json_response({"sensors": sensors})
        
        return web.json_response({"sensors": []})

    async def websocket_handler(self, request):
        """WebSocket Ð´Ð»Ñ real-time Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ð¹."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                
                if data.get("type") == "command":
                    result = self.brain.execute_command(data.get("command", ""))
                    await ws.send_json({"type": "result", "data": result})
                
                elif data.get("type") == "status":
                    status = self.brain.get_status()
                    await ws.send_json({"type": "status", "data": status})
            
            elif msg.type == web.WSMsgType.ERROR:
                self.brain.logger.error(f"WebSocket error: {ws.exception()}")
        
        return ws

    def start(self):
        """ÐÐ°Ð¿ÑÑÐº ÑÐµÑÐ²ÐµÑÐ°."""
        self.brain.logger.info(f"Mobile API ÑÐµÑÐ²ÐµÑ Ð·Ð°Ð¿ÑÑÐµÐ½ Ð½Ð° {self.host}:{self.port}")
        web.run_app(self.app, host=self.host, port=self.port)

    def start_async(self):
        """ÐÐ°Ð¿ÑÑÐº Ð² Ð¾ÑÐ´ÐµÐ»ÑÐ½Ð¾Ð¼ Ð¿Ð¾ÑÐ¾ÐºÐµ."""
        import threading
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()
