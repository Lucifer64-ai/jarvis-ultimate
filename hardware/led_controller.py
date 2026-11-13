"""
LED Controller - Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ LED Ð¸Ð½Ð´Ð¸ÐºÐ°ÑÐ¾ÑÐ°Ð¼Ð¸
"""

import time
import threading
from typing import Dict, Optional, Tuple
import logging


class LEDController:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ LED Ð¸Ð½Ð´Ð¸ÐºÐ°ÑÐ¾ÑÐ°Ð¼Ð¸ JARVIS."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        
        # ÐÐ¸Ð½Ñ LED (Ð´Ð»Ñ Raspberry Pi GPIO)
        self.led_pins = brain.config.get("hardware.led_pins", [18, 23, 24])  # RGB
        
        # Ð¡Ð¾ÑÑÐ¾ÑÐ½Ð¸Ñ
        self.current_color = (0, 0, 0)
        self.brightness = 100
        self.animation_thread: Optional[threading.Thread] = None
        self.stop_animation = False
        
        self.initialized = False

    def initialize(self) -> Dict:
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ LED."""
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # for pin in self.led_pins:
            #     GPIO.setup(pin, GPIO.OUT)
            #     self.pwm.append(GPIO.PWM(pin, 1000))
            #     self.pwm[-1].start(0)
            
            self.initialized = True
            self.logger.info("LED Ð¸Ð½Ð´Ð¸ÐºÐ°ÑÐ¾ÑÑ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ")
            return {"status": "ok", "message": "LED Ð³Ð¾ÑÐ¾Ð²Ñ Ðº ÑÐ°Ð±Ð¾ÑÐµ"}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ LED: {e}")
            return {"status": "error", "message": str(e)}

    def set_color(self, r: int, g: int, b: int) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÑÐ²ÐµÑÐ° (0-255)."""
        if not self.initialized:
            return {"status": "error", "message": "LED Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ"}
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        self.current_color = (r, g, b)
        
        # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
        # duty_r = (r / 255.0) * (self.brightness / 100.0) * 100
        # duty_g = (g / 255.0) * (self.brightness / 100.0) * 100
        # duty_b = (b / 255.0) * (self.brightness / 100.0) * 100
        # self.pwm[0].ChangeDutyCycle(duty_r)
        # self.pwm[1].ChangeDutyCycle(duty_g)
        # self.pwm[2].ChangeDutyCycle(duty_b)
        
        self.logger.info(f"LED ÑÐ²ÐµÑ: RGB({r}, {g}, {b})")
        return {"status": "ok", "message": f"Ð¦Ð²ÐµÑ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½: RGB({r}, {g}, {b})"}

    def set_brightness(self, level: int) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÑÑÐºÐ¾ÑÑÐ¸ (0-100)."""
        self.brightness = max(0, min(100, level))
        r, g, b = self.current_color
        return self.set_color(r, g, b)

    def off(self) -> Dict:
        """ÐÑÐºÐ»ÑÑÐ¸ÑÑ LED."""
        self.stop_animation = True
        return self.set_color(0, 0, 0)

    # ÐÑÐµÐ´ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð½ÑÐµ ÑÐ²ÐµÑÐ°
    def idle(self) -> Dict:
        """Ð ÐµÐ¶Ð¸Ð¼ Ð¾Ð¶Ð¸Ð´Ð°Ð½Ð¸Ñ - ÑÐ¸Ð½Ð¸Ð¹."""
        return self.set_color(0, 100, 255)

    def listening(self) -> Dict:
        """Ð¡Ð»ÑÑÐ°ÐµÑ - Ð·ÐµÐ»ÐµÐ½ÑÐ¹."""
        return self.set_color(0, 255, 100)

    def speaking(self) -> Dict:
        """ÐÐ¾Ð²Ð¾ÑÐ¸Ñ - Ð³Ð¾Ð»ÑÐ±Ð¾Ð¹."""
        return self.set_color(0, 200, 255)

    def thinking(self) -> Dict:
        """ÐÑÐ¼Ð°ÐµÑ - Ð¶ÐµÐ»ÑÑÐ¹."""
        return self.set_color(255, 200, 0)

    def error(self) -> Dict:
        """ÐÑÐ¸Ð±ÐºÐ° - ÐºÑÐ°ÑÐ½ÑÐ¹."""
        return self.set_color(255, 0, 0)

    def success(self) -> Dict:
        """Ð£ÑÐ¿ÐµÑ - Ð·ÐµÐ»ÐµÐ½ÑÐ¹."""
        return self.set_color(0, 255, 0)

    # ÐÐ½Ð¸Ð¼Ð°ÑÐ¸Ð¸
    def pulse(self, color: Tuple[int, int, int], duration: float = 2.0) -> Dict:
        """ÐÑÐ»ÑÑÐ°ÑÐ¸Ñ."""
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
        
        return {"status": "ok", "message": "ÐÑÐ»ÑÑÐ°ÑÐ¸Ñ Ð·Ð°Ð¿ÑÑÐµÐ½Ð°"}

    def breathe(self, duration: float = 3.0) -> Dict:
        """ÐÑÑÐ°Ð½Ð¸Ðµ - Ð¿Ð»Ð°Ð²Ð½Ð°Ñ Ð¿ÑÐ»ÑÑÐ°ÑÐ¸Ñ ÑÐ¸Ð½Ð¸Ð¼."""
        return self.pulse((0, 100, 255), duration)

    def rainbow(self, duration: float = 5.0) -> Dict:
        """Ð Ð°Ð´ÑÐ³Ð°."""
        self.stop_animation = True
        time.sleep(0.1)
        self.stop_animation = False
        
        def animate():
            colors = [
                (255, 0, 0),    # ÐÑÐ°ÑÐ½ÑÐ¹
                (255, 127, 0),  # ÐÑÐ°Ð½Ð¶ÐµÐ²ÑÐ¹
                (255, 255, 0),  # ÐÐµÐ»ÑÑÐ¹
                (0, 255, 0),    # ÐÐµÐ»ÐµÐ½ÑÐ¹
                (0, 0, 255),    # Ð¡Ð¸Ð½Ð¸Ð¹
                (75, 0, 130),   # ÐÐ½Ð´Ð¸Ð³Ð¾
                (148, 0, 211)   # Ð¤Ð¸Ð¾Ð»ÐµÑÐ¾Ð²ÑÐ¹
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
        
        return {"status": "ok", "message": "Ð Ð°Ð´ÑÐ³Ð° Ð·Ð°Ð¿ÑÑÐµÐ½Ð°"}

    def get_status(self) -> Dict:
        """Ð¡ÑÐ°ÑÑÑ LED."""
        return {
            "initialized": self.initialized,
            "color": self.current_color,
            "brightness": self.brightness
        }

    def cleanup(self):
        """ÐÑÐ¸ÑÑÐºÐ° ÑÐµÑÑÑÑÐ¾Ð²."""
        self.stop_animation = True
        if self.initialized:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # for pwm in self.pwm:
            #     pwm.stop()
            # GPIO.cleanup()
            self.initialized = False
            self.logger.info("LED Ð¾ÑÐ¸ÑÐµÐ½Ñ")
