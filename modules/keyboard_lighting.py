"""Optional keyboard RGB control through a local OpenRGB SDK server.

RGB keyboard control is vendor/model dependent. This adapter only connects to
OpenRGB on localhost; it does not search the network or run shell commands.
Requires `openrgb-python` and the OpenRGB SDK server to be enabled locally.
"""

from typing import Dict


class KeyboardLightingModule:
    def __init__(self, brain):
        self.brain = brain

    def set_color(self, red: int, green: int, blue: int, device_index: int | None = None) -> Dict:
        try:
            rgb = tuple(max(0, min(255, int(value))) for value in (red, green, blue))
        except (TypeError, ValueError):
            return {"status": "error", "message": "Ð¦Ð²ÐµÑ Ð´Ð¾Ð»Ð¶ÐµÐ½ Ð±ÑÑÑ Ð·Ð°Ð´Ð°Ð½ ÑÑÐµÐ¼Ñ ÑÐ¸ÑÐ»Ð°Ð¼Ð¸ Ð¾Ñ 0 Ð´Ð¾ 255"}

        try:
            from openrgb import OpenRGBClient
            from openrgb.utils import RGBColor
        except ImportError:
            return {
                "status": "unavailable",
                "message": "ÐÐ»Ñ RGB-ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ ÑÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÐµ openrgb-python Ð¸ Ð²ÐºÐ»ÑÑÐ¸ÑÐµ Ð»Ð¾ÐºÐ°Ð»ÑÐ½ÑÐ¹ SDK Server Ð² OpenRGB.",
            }

        try:
            client = OpenRGBClient("127.0.0.1", 6742, name="JARVIS")
            devices = list(client.devices)
            keyboards = [device for device in devices if "keyboard" in str(getattr(device, "type", "")).lower()]
            if not keyboards:
                keyboards = [device for device in devices if "keyboard" in str(getattr(device, "name", "")).lower()]
            if not keyboards:
                return {"status": "unavailable", "message": "OpenRGB Ð½Ðµ Ð¾Ð±Ð½Ð°ÑÑÐ¶Ð¸Ð» ÑÐ¾Ð²Ð¼ÐµÑÑÐ¸Ð¼ÑÑ ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ"}

            selected_index = 0 if device_index is None else int(device_index)
            if selected_index < 0 or selected_index >= len(keyboards):
                return {"status": "error", "message": "ÐÐ½Ð´ÐµÐºÑ ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ Ð²Ð½Ðµ Ð´Ð¸Ð°Ð¿Ð°Ð·Ð¾Ð½Ð°", "count": len(keyboards)}

            keyboard = keyboards[selected_index]
            keyboard.set_color(RGBColor(*rgb))
            return {
                "status": "ok",
                "message": f"Ð¦Ð²ÐµÑ ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½: RGB{rgb}",
                "device": str(getattr(keyboard, "name", "keyboard")),
            }
        except Exception as error:
            self.brain.logger.warning("ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¸Ð·Ð¼ÐµÐ½Ð¸ÑÑ Ð¿Ð¾Ð´ÑÐ²ÐµÑÐºÑ ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ: %s", error)
            return {
                "status": "error",
                "message": "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿Ð¾Ð´ÐºÐ»ÑÑÐ¸ÑÑÑÑ Ðº OpenRGB. ÐÑÐ¾Ð²ÐµÑÑÑÐµ SDK Server Ð¸ ÑÐ¾Ð²Ð¼ÐµÑÑÐ¸Ð¼Ð¾ÑÑÑ ÐºÐ»Ð°Ð²Ð¸Ð°ÑÑÑÑ.",
            }

    def off(self, device_index: int | None = None) -> Dict:
        return self.set_color(0, 0, 0, device_index)
