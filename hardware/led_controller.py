"""
LED Controller - ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ LED ÃÂ¸ÃÂ½ÃÂ´ÃÂ¸ÃÂºÃÂ°ÃÃÂ¾ÃÃÂ°ÃÂ¼ÃÂ¸
"""

import time
import threading
from typing import Dict, Optional, Tuple
import logging


class LEDController:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ LED ÃÂ¸ÃÂ½ÃÂ´ÃÂ¸ÃÂºÃÂ°ÃÃÂ¾ÃÃÂ°ÃÂ¼ÃÂ¸ JARVIS."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        
        # ÃÃÂ¸ÃÂ½Ã LED (ÃÂ´ÃÂ»Ã Raspberry Pi GPIO)
        self.led_pins = brain.config.get("hardware.led_pins", [18, 23, 24])  # RGB
        
        # ÃÂ¡ÃÂ¾ÃÃÃÂ¾ÃÃÂ½ÃÂ¸Ã
        self.current_color = (0, 0, 0)
        self.brightness = 100
        self.animation_thread: Optional[threading.Thread] = None
        self.stop_animation = False
        
        self.initialized = False

    def initialize(self) -> Dict:
        """ÃÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã LED."""
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # for pin in self.led_pins:
            #     GPIO.setup(pin, GPIO.OUT)
            #     self.pwm.append(GPIO.PWM(pin, 1000))
            #     self.pwm[-1].start(0)
            
            self.initialized = True
            self.logger.info("LED ÃÂ¸ÃÂ½ÃÂ´ÃÂ¸ÃÂºÃÂ°ÃÃÂ¾ÃÃ ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½Ã")
            return {"status": "ok", "message": "LED ÃÂ³ÃÂ¾ÃÃÂ¾ÃÂ²Ã ÃÂº ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂµ"}
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ LED: {e}")
            return {"status": "error", "message": str(e)}

    def set_color(self, r: int, g: int, b: int) -> Dict:
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÃÂ²ÃÂµÃÃÂ° (0-255)."""
        if not self.initialized:
            return {"status": "error", "message": "LED ÃÂ½ÃÂµ ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½Ã"}
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        self.current_color = (r, g, b)
        
        # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
        # duty_r = (r / 255.0) * (self.brightness / 100.0) * 100
        # duty_g = (g / 255.0) * (self.brightness / 100.0) * 100
        # duty_b = (b / 255.0) * (self.brightness / 100.0) * 100
        # self.pwm[0].ChangeDutyCycle(duty_r)
        # self.pwm[1].ChangeDutyCycle(duty_g)
        # self.pwm[2].ChangeDutyCycle(duty_b)
        
        self.logger.info(f"LED ÃÃÂ²ÃÂµÃ: RGB({r}, {g}, {b})")
        return {"status": "ok", "message": f"ÃÂ¦ÃÂ²ÃÂµÃ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½: RGB({r}, {g}, {b})"}

    def set_brightness(self, level: int) -> Dict:
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÃÃÂºÃÂ¾ÃÃÃÂ¸ (0-100)."""
        self.brightness = max(0, min(100, level))
        r, g, b = self.current_color
        return self.set_color(r, g, b)

    def off(self) -> Dict:
        """ÃÃÃÂºÃÂ»ÃÃÃÂ¸ÃÃ LED."""
        self.stop_animation = True
        return self.set_color(0, 0, 0)

    # ÃÃÃÂµÃÂ´ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ½ÃÃÂµ ÃÃÂ²ÃÂµÃÃÂ°
    def idle(self) -> Dict:
        """ÃÂ ÃÂµÃÂ¶ÃÂ¸ÃÂ¼ ÃÂ¾ÃÂ¶ÃÂ¸ÃÂ´ÃÂ°ÃÂ½ÃÂ¸Ã - ÃÃÂ¸ÃÂ½ÃÂ¸ÃÂ¹."""
        return self.set_color(0, 100, 255)

    def listening(self) -> Dict:
        """ÃÂ¡ÃÂ»ÃÃÃÂ°ÃÂµÃ - ÃÂ·ÃÂµÃÂ»ÃÂµÃÂ½ÃÃÂ¹."""
        return self.set_color(0, 255, 100)

    def speaking(self) -> Dict:
        """ÃÃÂ¾ÃÂ²ÃÂ¾ÃÃÂ¸Ã - ÃÂ³ÃÂ¾ÃÂ»ÃÃÂ±ÃÂ¾ÃÂ¹."""
        return self.set_color(0, 200, 255)

    def thinking(self) -> Dict:
        """ÃÃÃÂ¼ÃÂ°ÃÂµÃ - ÃÂ¶ÃÂµÃÂ»ÃÃÃÂ¹."""
        return self.set_color(255, 200, 0)

    def error(self) -> Dict:
        """ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° - ÃÂºÃÃÂ°ÃÃÂ½ÃÃÂ¹."""
        return self.set_color(255, 0, 0)

    def success(self) -> Dict:
        """ÃÂ£ÃÃÂ¿ÃÂµÃ - ÃÂ·ÃÂµÃÂ»ÃÂµÃÂ½ÃÃÂ¹."""
        return self.set_color(0, 255, 0)

    # ÃÃÂ½ÃÂ¸ÃÂ¼ÃÂ°ÃÃÂ¸ÃÂ¸
    def pulse(self, color: Tuple[int, int, int], duration: float = 2.0) -> Dict:
        """ÃÃÃÂ»ÃÃÃÂ°ÃÃÂ¸Ã."""
        self.stop_animation = True
        time.sleep(0.1)
        self.stop_animation = False
        
        def animate():
            r, g, b = color
            steps = 50
            for i in range(steps):
                if self.stop_animation:
                    break
                factor = (i / steps) * (self.brightness / 100.0)
                self.set_color(int(r * factor), int(g * factor), int(b * factor))
                time.sleep(duration / steps / 2)
            
            for i in range(steps, -1, -1):
                if self.stop_animation:
                    break
                factor = (i / steps) * (self.brightness / 100.0)
                self.set_color(int(r * factor), int(g * factor), int(b * factor))
                time.sleep(duration / steps / 2)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
        
        return {"status": "ok", "message": "ÃÃÃÂ»ÃÃÃÂ°ÃÃÂ¸Ã ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ°"}

    def breathe(self, duration: float = 3.0) -> Dict:
        """ÃÃÃÃÂ°ÃÂ½ÃÂ¸ÃÂµ - ÃÂ¿ÃÂ»ÃÂ°ÃÂ²ÃÂ½ÃÂ°Ã ÃÂ¿ÃÃÂ»ÃÃÃÂ°ÃÃÂ¸Ã ÃÃÂ¸ÃÂ½ÃÂ¸ÃÂ¼."""
        return self.pulse((0, 100, 255), duration)

    def rainbow(self, duration: float = 5.0) -> Dict:
        """ÃÂ ÃÂ°ÃÂ´ÃÃÂ³ÃÂ°."""
        self.stop_animation = True
        time.sleep(0.1)
        self.stop_animation = False
        
        def animate():
            colors = [
                (255, 0, 0),    # ÃÃÃÂ°ÃÃÂ½ÃÃÂ¹
                (255, 127, 0),  # ÃÃÃÂ°ÃÂ½ÃÂ¶ÃÂµÃÂ²ÃÃÂ¹
                (255, 255, 0),  # ÃÃÂµÃÂ»ÃÃÃÂ¹
                (0, 255, 0),    # ÃÃÂµÃÂ»ÃÂµÃÂ½ÃÃÂ¹
                (0, 0, 255),    # ÃÂ¡ÃÂ¸ÃÂ½ÃÂ¸ÃÂ¹
                (75, 0, 130),   # ÃÃÂ½ÃÂ´ÃÂ¸ÃÂ³ÃÂ¾
                (148, 0, 211)   # ÃÂ¤ÃÂ¸ÃÂ¾ÃÂ»ÃÂµÃÃÂ¾ÃÂ²ÃÃÂ¹
            ]
            
            step_time = duration / len(colors)
            for color in colors:
                if self.stop_animation:
                    break
                r, g, b = color
                factor = self.brightness / 100.0
                self.set_color(int(r * factor), int(g * factor), int(b * factor))
                time.sleep(step_time)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
        
        return {"status": "ok", "message": "ÃÂ ÃÂ°ÃÂ´ÃÃÂ³ÃÂ° ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ°"}

    def get_status(self) -> Dict:
        """ÃÂ¡ÃÃÂ°ÃÃÃ LED."""
        return {
            "initialized": self.initialized,
            "color": self.current_color,
            "brightness": self.brightness
        }

    def cleanup(self):
        """ÃÃÃÂ¸ÃÃÃÂºÃÂ° ÃÃÂµÃÃÃÃÃÂ¾ÃÂ²."""
        self.stop_animation = True
        if self.initialized:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # for pwm in self.pwm:
            #     pwm.stop()
            # GPIO.cleanup()
            self.initialized = False
            self.logger.info("LED ÃÂ¾ÃÃÂ¸ÃÃÂµÃÂ½Ã")
