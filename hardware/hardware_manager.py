"""
Hardware Manager - ÐÐ»Ð°Ð²Ð½ÑÐ¹ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑ Ð°Ð¿Ð¿Ð°ÑÐ°ÑÐ½Ð¾Ð³Ð¾ Ð¾Ð±ÐµÑÐ¿ÐµÑÐµÐ½Ð¸Ñ JARVIS
"""

from typing import Dict, Optional
import logging


class HardwareManager:
    """Ð¦ÐµÐ½ÑÑÐ°Ð»Ð¸Ð·Ð¾Ð²Ð°Ð½Ð½Ð¾Ðµ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð²ÑÐµÐ¼ Ð¶ÐµÐ»ÐµÐ·Ð¾Ð¼ JARVIS."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        
        # ÐÐ¾Ð¼Ð¿Ð¾Ð½ÐµÐ½ÑÑ
        self.display = None
        self.servos = None
        self.leds = None
        self.sensors = None
        
        self.initialized = False

    def initialize(self) -> Dict:
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð²ÑÐµÑ Ð°Ð¿Ð¿Ð°ÑÐ°ÑÐ½ÑÑ ÐºÐ¾Ð¼Ð¿Ð¾Ð½ÐµÐ½ÑÐ¾Ð²."""
        try:
            # ÐÐ¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¸Ð¹ Ð´Ð¸ÑÐ¿Ð»ÐµÐ¹
            from hardware.holographic_display import HolographicDisplay
            self.display = HolographicDisplay(self.brain)
            self.logger.info("â ÐÐ¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¸Ð¹ Ð´Ð¸ÑÐ¿Ð»ÐµÐ¹ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½")
            
            # Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ
            from hardware.servo_controller import ServoController
            self.servos = ServoController(self.brain)
            self.servos.initialize()
            self.logger.info("â Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
            
            # LED Ð¸Ð½Ð´Ð¸ÐºÐ°ÑÐ¾ÑÑ
            from hardware.led_controller import LEDController
            self.leds = LEDController(self.brain)
            self.leds.initialize()
            self.logger.info("â LED Ð¸Ð½Ð´Ð¸ÐºÐ°ÑÐ¾ÑÑ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
            
            # ÐÐ°ÑÑÐ¸ÐºÐ¸
            from hardware.sensor_manager import SensorManager
            self.sensors = SensorManager(self.brain)
            self.sensors.initialize()
            self.logger.info("â ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
            
            self.initialized = True
            
            # ÐÐ°ÑÐ°Ð»ÑÐ½Ð¾Ðµ ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ
            self.leds.idle()
            self.servos.center()
            
            return {"status": "ok", "message": "ÐÐ¿Ð¿Ð°ÑÐ°ÑÐ½Ð¾Ðµ Ð¾Ð±ÐµÑÐ¿ÐµÑÐµÐ½Ð¸Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ð¾"}
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ hardware: {e}")
            return {"status": "error", "message": str(e)}

    def activate(self) -> Dict:
        """ÐÐºÑÐ¸Ð²Ð°ÑÐ¸Ñ JARVIS (Ð²ÐºÐ»ÑÑÐµÐ½Ð¸Ðµ Ð´Ð¸ÑÐ¿Ð»ÐµÑ, Ð¿ÑÐ¸Ð²ÐµÑÑÑÐ²Ð¸Ðµ)."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        try:
            # ÐÐºÐ»ÑÑÐµÐ½Ð¸Ðµ Ð´Ð¸ÑÐ¿Ð»ÐµÑ
            self.display.activate()
            
            # ÐÑÐ¸Ð²ÐµÑÑÑÐ²ÐµÐ½Ð½Ð°Ñ Ð°Ð½Ð¸Ð¼Ð°ÑÐ¸Ñ
            self.leds.pulse((0, 200, 255), duration=2.0)
            self.servos.look_at("center")
            
            # ÐÐ¾ÐºÐ°Ð· Ð³Ð¾Ð»Ð¾Ð³ÑÐ°Ð¼Ð¼Ñ
            self.display.show_hologram("default")
            
            return {"status": "ok", "message": "JARVIS Ð°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def deactivate(self) -> Dict:
        """ÐÐµÐ°ÐºÑÐ¸Ð²Ð°ÑÐ¸Ñ JARVIS."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        try:
            self.display.deactivate()
            self.leds.off()
            self.servos.center()
            
            return {"status": "ok", "message": "JARVIS Ð´ÐµÐ°ÐºÑÐ¸Ð²Ð¸ÑÐ¾Ð²Ð°Ð½"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def on_listening(self) -> Dict:
        """JARVIS ÑÐ»ÑÑÐ°ÐµÑ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        self.leds.listening()
        self.servos.look_at("center")
        
        return {"status": "ok", "message": "Ð¡Ð»ÑÑÐ°Ñ..."}

    def on_thinking(self) -> Dict:
        """JARVIS Ð´ÑÐ¼Ð°ÐµÑ."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        self.leds.thinking()
        
        return {"status": "ok", "message": "ÐÑÐ¼Ð°Ñ..."}

    def on_speaking(self) -> Dict:
        """JARVIS Ð³Ð¾Ð²Ð¾ÑÐ¸Ñ."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        self.leds.speaking()
        
        return {"status": "ok", "message": "ÐÐ¾Ð²Ð¾ÑÑ..."}

    def on_error(self) -> Dict:
        """ÐÑÐ¸Ð±ÐºÐ°."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        self.leds.error()
        self.servos.shake()
        
        return {"status": "ok", "message": "ÐÑÐ¸Ð±ÐºÐ°"}

    def on_success(self) -> Dict:
        """Ð£ÑÐ¿ÐµÑ."""
        if not self.initialized:
            return {"status": "error", "message": "Hardware Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}
        
        self.leds.success()
        self.servos.nod()
        
        return {"status": "ok", "message": "Ð£ÑÐ¿ÐµÑÐ½Ð¾"}

    def track_speaker(self, x: int, y: int) -> Dict:
        """Ð¡Ð»ÐµÐ´Ð¸ÑÑ Ð·Ð° Ð³Ð¾Ð²Ð¾ÑÑÑÐ¸Ð¼."""
        if not self.initialized or not self.servos:
            return {"status": "error", "message": "Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ Ð½Ðµ Ð³Ð¾ÑÐ¾Ð²Ñ"}
        
        return self.servos.track_speaker(x, y)

    def get_environment(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð´Ð°Ð½Ð½ÑÐµ Ð¾Ð± Ð¾ÐºÑÑÐ¶Ð°ÑÑÐµÐ¹ ÑÑÐµÐ´Ðµ."""
        if not self.initialized or not self.sensors:
            return {"status": "error", "message": "ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð½Ðµ Ð³Ð¾ÑÐ¾Ð²Ñ"}
        
        return self.sensors.get_all_readings()

    def is_someone_present(self) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¿ÑÐ¸ÑÑÑÑÑÐ²Ð¸Ðµ ÑÐµÐ»Ð¾Ð²ÐµÐºÐ°."""
        if not self.initialized or not self.sensors:
            return False
        
        return self.sensors.is_someone_present()

    def get_status(self) -> Dict:
        """ÐÐ¾Ð»Ð½ÑÐ¹ ÑÑÐ°ÑÑÑ hardware."""
        status = {
            "initialized": self.initialized,
            "components": {}
        }
        
        if self.display:
            status["components"]["display"] = self.display.get_status()
        
        if self.servos:
            pan, tilt = self.servos.get_position()
            status["components"]["servos"] = {
                "initialized": self.servos.initialized,
                "position": {"pan": pan, "tilt": tilt}
            }
        
        if self.leds:
            status["components"]["leds"] = self.leds.get_status()
        
        if self.sensors:
            status["components"]["sensors"] = {
                "initialized": self.sensors.initialized,
                "readings": self.sensors.get_all_readings()
            }
        
        return status

    def cleanup(self):
        """ÐÑÐ¸ÑÑÐºÐ° ÑÐµÑÑÑÑÐ¾Ð²."""
        if self.initialized:
            if self.servos:
                self.servos.cleanup()
            if self.leds:
                self.leds.cleanup()
            if self.sensors:
                self.sensors.cleanup()
            
            self.initialized = False
            self.logger.info("Hardware Ð¾ÑÐ¸ÑÐµÐ½")
