"""
ÐÐ±ÑÐ°Ð±Ð¾ÑÑÐ¸Ðº Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´ JARVIS
"""

from typing import Dict, Optional
import re


class CommandHandler:
    """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´."""

    def __init__(self, brain):
        self.brain = brain
        self.commands = self._register_commands()

    def _register_commands(self) -> Dict:
        """Ð ÐµÐ³Ð¸ÑÑÑÐ°ÑÐ¸Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´."""
        return {
            # Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
            r"Ð²ÑÐºÐ»ÑÑÐ¸ (ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ|Ð¿Ðº)": ("system", "shutdown"),
            r"Ð¿ÐµÑÐµÐ·Ð°Ð³ÑÑÐ·Ð¸ (ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ|Ð¿Ðº)": ("system", "restart"),
            r"Ð¾ÑÐ¼ÐµÐ½Ð¸ Ð²ÑÐºÐ»ÑÑÐµÐ½Ð¸Ðµ": ("system", "cancel_shutdown"),
            r"Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹ (ÑÐºÑÐ°Ð½|ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ)": ("system", "lock_screen"),
            r"ÑÐ¿ÑÑÐ¸Ð¹ ÑÐµÐ¶Ð¸Ð¼": ("system", "sleep"),

            # ÐÐ¾Ð»Ð½ÑÐ¹ ÐºÐ¾Ð½ÑÑÐ¾Ð»Ñ ÑÐ°Ð±Ð¾ÑÐµÐ³Ð¾ ÑÑÐ¾Ð»Ð°/ÐÐ
            r"(Ð¿Ð¾ÐºÐ°Ð¶Ð¸|Ð¾ÑÐºÑÐ¾Ð¹) ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»|ÑÐ²ÐµÑÐ½Ð¸ Ð²ÑÐµ Ð¾ÐºÐ½Ð°|ÑÐ²ÐµÑÐ½Ð¸ Ð¾ÐºÐ½Ð°": ("desktop", "show_desktop"),
            r"ÑÐ´ÐµÐ»Ð°Ð¹ Ð³ÑÐ¾Ð¼ÑÐµ|ÑÐ²ÐµÐ»Ð¸ÑÑ Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑ|Ð³ÑÐ¾Ð¼ÑÐµ": ("desktop", "volume_up"),
            r"ÑÐ´ÐµÐ»Ð°Ð¹ ÑÐ¸ÑÐµ|ÑÐ¼ÐµÐ½ÑÑÐ¸ Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑ|ÑÐ¸ÑÐµ": ("desktop", "volume_down"),
            r"Ð±ÐµÐ· Ð·Ð²ÑÐºÐ°|mute|Ð²ÑÐºÐ»ÑÑÐ¸ Ð·Ð²ÑÐº": ("desktop", "mute"),
            r"Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹ ÑÐºÑÐ°Ð½|Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹ ÑÐºÑÐ°Ð½|lock screen": ("desktop", "lock_screen"),
            r"ÐºÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°ÑÑ|copy": ("desktop", "shortcut"),
            r"Ð²ÑÑÐ°Ð²Ð¸ÑÑ|paste": ("desktop", "shortcut"),
            r"Ð¾ÑÐ¼ÐµÐ½Ð¸ÑÑ|undo": ("desktop", "shortcut"),
            r"Ð²ÑÐ´ÐµÐ»Ð¸ÑÑ Ð²ÑÑ|select all": ("desktop", "shortcut"),

            # ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ
            r"ÐºÐ¾ÑÐ¾ÑÑÐ¹ ÑÐ°Ñ|Ð²ÑÐµÐ¼Ñ|ÑÐºÐ¾Ð»ÑÐºÐ¾ Ð²ÑÐµÐ¼ÐµÐ½Ð¸": ("info", "time"),
            r"ÐºÐ°ÐºÐ°Ñ (Ð´Ð°ÑÐ°|ÑÐµÐ³Ð¾Ð´Ð½Ñ)": ("info", "date"),
            r"ÐºÐ°ÐºÐ°Ñ Ð¿Ð¾Ð³Ð¾Ð´Ð°": ("info", "weather"),
            r"ÑÑÐ°ÑÑÑ ÑÐ¸ÑÑÐµÐ¼Ñ": ("info", "system_status"),
            r"Ð·Ð°Ð³ÑÑÐ·ÐºÐ° Ð¿ÑÐ¾ÑÐµÑÑÐ¾ÑÐ°": ("info", "cpu_usage"),
            r"ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ Ð±Ð°ÑÐ°ÑÐµÐ¸": ("info", "battery"),

            # ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ
            r"Ð¾ÑÐºÑÐ¾Ð¹ (Ð±Ð»Ð¾ÐºÐ½Ð¾Ñ|notepad)": ("app", "open_notepad"),
            r"Ð¾ÑÐºÑÐ¾Ð¹ ÐºÐ°Ð»ÑÐºÑÐ»ÑÑÐ¾Ñ": ("app", "open_calculator"),
            r"Ð¾ÑÐºÑÐ¾Ð¹ youtube": ("app", "open_youtube"),
            r"Ð¾ÑÐºÑÐ¾Ð¹ github": ("app", "open_github"),

            # Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ
            r"Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑ (\d+)": ("control", "set_volume"),
            r"ÑÑÐºÐ¾ÑÑÑ (\d+)": ("control", "set_brightness"),
            r"ÑÐ²ÐµÑÐ½Ð¸ Ð²ÑÐµ Ð¾ÐºÐ½Ð°": ("control", "minimize_all"),
            r"Ð¿Ð¾ÐºÐ°Ð¶Ð¸ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»": ("control", "show_desktop"),

            # Ð¡ÐµÑÑ
            r"ÑÐµÑÑ ÑÐºÐ¾ÑÐ¾ÑÑÐ¸|ÑÐºÐ¾ÑÐ¾ÑÑÑ Ð¸Ð½ÑÐµÑÐ½ÐµÑÐ°": ("network", "speed_test"),
            r"ÐºÐ°ÐºÐ¾Ð¹ (ip|Ð°Ð¹Ð¿Ð¸) Ð°Ð´ÑÐµÑ": ("network", "get_ip"),
        }

    def parse_command(self, text: str) -> Optional[Dict]:
        """Ð Ð°Ð·Ð±Ð¾Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        text_lower = text.lower().strip()

        for pattern, (category, action) in self.commands.items():
            match = re.match(pattern, text_lower)
            if match:
                result = {
                    "category": category,
                    "action": action,
                    "original": text,
                }

                if match.groups():
                    result["params"] = match.groups()

                if category in {"desktop", "control"} and action == "shortcut":
                    # Ð´Ð»Ñ copy/paste/undo/select all, Ð¿ÐµÑÐµÐ´Ð°ÑÐ¼ Ð¸Ð¼Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ ÐºÐ°Ðº Ð¿Ð°ÑÐ°Ð¼ÐµÑÑ
                    result["shortcut_name"] = text_lower

                return result

        return None

    def execute(self, text: str) -> Dict:
        """ÐÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        command = self.parse_command(text)

        if not command:
            return {"status": "error", "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð½Ðµ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð½Ð°"}

        category = command["category"]
        action = command["action"]

        try:
            if category == "system":
                module = self.brain.modules.get("system")
                if module and hasattr(module, action):
                    return getattr(module, action)()

            elif category == "desktop":
                module = self.brain.modules.get("desktop_control")
                if module and hasattr(module, action):
                    if action == "shortcut":
                        shortcut_name = self._extract_shortcut_name(text)
                        if not shortcut_name:
                            return {"status": "error", "message": "ÐÐ¾Ð¼Ð±Ð¸Ð½Ð°ÑÐ¸Ñ Ð½Ðµ Ð¿Ð¾Ð´Ð´ÐµÑÐ¶Ð¸Ð²Ð°ÐµÑÑÑ"}
                        return module.shortcut(shortcut_name)
                    return getattr(module, action)()
                # fallback to legacy desktop/system actions
                legacy = self.brain.modules.get("system")
                if legacy and hasattr(legacy, action):
                    return getattr(legacy, action)()

            elif category == "info":
                return self._handle_info(action)

            elif category == "app":
                return self._handle_app(action)

            elif category == "control":
                return self._handle_control(action, command.get("params"))

            elif category == "network":
                module = self.brain.modules.get("network")
                if module and hasattr(module, action):
                    return getattr(module, action)()

            return {"status": "error", "message": "ÐÐµÐ¹ÑÑÐ²Ð¸Ðµ Ð½Ðµ ÑÐµÐ°Ð»Ð¸Ð·Ð¾Ð²Ð°Ð½Ð¾"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _extract_shortcut_name(self, text: str) -> str:
        text_lower = text.lower().strip()
        mapping = {
            "ÐºÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°ÑÑ": "copy",
            "copy": "copy",
            "Ð²ÑÑÐ°Ð²Ð¸ÑÑ": "paste",
            "paste": "paste",
            "Ð¾ÑÐ¼ÐµÐ½Ð¸ÑÑ": "undo",
            "undo": "undo",
            "Ð²ÑÐ´ÐµÐ»Ð¸ÑÑ Ð²ÑÑ": "select_all",
            "select all": "select_all",
        }
        for key, value in mapping.items():
            if key in text_lower:
                return value
        return ""

    def _handle_info(self, action: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¾Ð½Ð½ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´."""
        from datetime import datetime

        if action == "time":
            now = datetime.now()
            return {"status": "ok", "message": f"Ð¡ÐµÐ¹ÑÐ°Ñ {now.strftime('%H:%M')}"}

        elif action == "date":
            now = datetime.now()
            return {"status": "ok", "message": f"Ð¡ÐµÐ³Ð¾Ð´Ð½Ñ {now.strftime('%d %B %Y')}"}

        elif action == "system_status":
            hardware = self.brain.modules.get("hardware")
            if hardware:
                report = hardware.get_full_report()
                return {"status": "ok", "data": report}

        elif action == "cpu_usage":
            hardware = self.brain.modules.get("hardware")
            if hardware:
                cpu_info = hardware.get_cpu_info()
                return {"status": "ok", "message": f"ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¿ÑÐ¾ÑÐµÑÑÐ¾ÑÐ° {cpu_info['usage']}%"}

        elif action == "battery":
            power = self.brain.modules.get("power")
            if power:
                battery = power.get_battery_info()
                if battery.get("available"):
                    return {"status": "ok", "message": f"ÐÐ°ÑÑÐ´ Ð±Ð°ÑÐ°ÑÐµÐ¸ {battery['percent']}%"}
                else:
                    return {"status": "ok", "message": "ÐÐ°ÑÐ°ÑÐµÑ Ð½Ðµ Ð¾Ð±Ð½Ð°ÑÑÐ¶ÐµÐ½Ð°"}

        return {"status": "error", "message": "ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð½ÐµÐ´Ð¾ÑÑÑÐ¿Ð½Ð°"}

    def _handle_app(self, action: str) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð¾ÑÐºÑÑÑÐ¸Ñ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        import subprocess

        apps = {
            "open_notepad": "notepad",
            "open_calculator": "calc",
            "open_youtube": "https://youtube.com",
            "open_github": "https://github.com",
        }

        if action in apps:
            target = apps[action]
            try:
                if target.startswith("http"):
                    subprocess.Popen(["cmd", "/c", "start", "", target], shell=True)
                else:
                    subprocess.Popen([target])
                return {"status": "ok", "message": f"ÐÑÐºÑÑÐ²Ð°Ñ {action.replace('open_', '')}"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "error", "message": "ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}

    def _handle_control(self, action: str, params: tuple = None) -> Dict:
        """ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ñ."""
        try:
            import pyautogui
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
        except Exception:
            pyautogui = None
            AudioUtilities = None
            IAudioEndpointVolume = None
            CLSCTX_ALL = None

        if action == "set_volume" and params:
            if pyautogui is None or AudioUtilities is None:
                return {"status": "error", "message": "Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑÑ Ð½ÐµÐ´Ð¾ÑÑÑÐ¿Ð½Ð¾"}
            try:
                volume_level = int(params[0]) / 100
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                volume.SetMasterVolumeLevelScalar(volume_level, None)
                return {"status": "ok", "message": f"ÐÑÐ¾Ð¼ÐºÐ¾ÑÑÑ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð° Ð½Ð° {params[0]}%"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        elif action == "minimize_all":
            desktop = self.brain.modules.get("desktop_control")
            if desktop:
                return desktop.minimize_all()

        elif action == "show_desktop":
            desktop = self.brain.modules.get("desktop_control")
            if desktop:
                return desktop.show_desktop()

        return {"status": "error", "message": "ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð½Ðµ ÑÐµÐ°Ð»Ð¸Ð·Ð¾Ð²Ð°Ð½Ð°"}

