"""
Servo Controller - Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð°Ð¼Ð¸ Ð´Ð»Ñ Ð´Ð²Ð¸Ð¶ÐµÐ½Ð¸Ñ "Ð³Ð¾Ð»Ð¾Ð²Ñ"
"""

import time
from typing import Dict, Optional, Tuple
import logging


class ServoController:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð°Ð¼Ð¸ JARVIS."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        
        # ÐÐ¸Ð½Ñ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð¾Ð² (Ð´Ð»Ñ Raspberry Pi GPIO)
        self.pan_pin = brain.config.get("hardware.servo_pan_pin", 17)
        self.tilt_pin = brain.config.get("hardware.servo_tilt_pin", 27)
        
        # Ð¢ÐµÐºÑÑÐ¸Ðµ ÑÐ³Ð»Ñ
        self.pan_angle = 90  # ÐÐ¾ÑÐ¸Ð·Ð¾Ð½ÑÐ°Ð»ÑÐ½Ð¾Ðµ Ð¿Ð¾Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ (0-180)
        self.tilt_angle = 90  # ÐÐµÑÑÐ¸ÐºÐ°Ð»ÑÐ½Ð¾Ðµ Ð¿Ð¾Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ (0-180)
        
        # ÐÐ³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ñ
        self.pan_min = 0
        self.pan_max = 180
        self.tilt_min = 45
        self.tilt_max = 135
        
        self.initialized = False

    def initialize(self) -> Dict:
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð¾Ð²."""
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(self.pan_pin, GPIO.OUT)
            # GPIO.setup(self.tilt_pin, GPIO.OUT)
            # self.pwm_pan = GPIO.PWM(self.pan_pin, 50)
            # self.pwm_tilt = GPIO.PWM(self.tilt_pin, 50)
            # self.pwm_pan.start(7.5)  # Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½Ð¾Ðµ Ð¿Ð¾Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ
            # self.pwm_tilt.start(7.5)
            
            self.initialized = True
            self.logger.info("Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ")
            return {"status": "ok", "message": "Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ Ð³Ð¾ÑÐ¾Ð²Ñ Ðº ÑÐ°Ð±Ð¾ÑÐµ"}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð¾Ð²: {e}")
            return {"status": "error", "message": str(e)}

    def move_to(self, pan: int, tilt: int) -> Dict:
        """ÐÐµÑÐµÐ¼ÐµÑÐµÐ½Ð¸Ðµ Ð² ÑÐºÐ°Ð·Ð°Ð½Ð½ÑÑ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ñ."""
        if not self.initialized:
            return {"status": "error", "message": "Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ"}
        
        # ÐÐ³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ðµ ÑÐ³Ð»Ð¾Ð²
        pan = max(self.pan_min, min(self.pan_max, pan))
        tilt = max(self.tilt_min, min(self.tilt_max, tilt))
        
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # duty_pan = 2.5 + (pan / 18.0)
            # duty_tilt = 2.5 + (tilt / 18.0)
            # self.pwm_pan.ChangeDutyCycle(duty_pan)
            # self.pwm_tilt.ChangeDutyCycle(duty_tilt)
            
            self.pan_angle = pan
            self.tilt_angle = tilt
            
            self.logger.info(f"Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ: pan={pan}Â°, tilt={tilt}Â°")
            time.sleep(0.5)  # ÐÑÐµÐ¼Ñ Ð½Ð° Ð¿ÐµÑÐµÐ¼ÐµÑÐµÐ½Ð¸Ðµ
            
            return {"status": "ok", "message": f"ÐÐ¾Ð·Ð¸ÑÐ¸Ñ: {pan}Â°, {tilt}Â°"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def look_at(self, direction: str) -> Dict:
        """ÐÐ¾ÑÐ¼Ð¾ÑÑÐµÑÑ Ð² ÑÐºÐ°Ð·Ð°Ð½Ð½Ð¾Ð¼ Ð½Ð°Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ð¸."""
        directions = {
            "center": (90, 90),
            "left": (45, 90),
            "right": (135, 90),
            "up": (90, 135),
            "down": (90, 45),
            "up-left": (45, 135),
            "up-right": (135, 135),
            "down-left": (45, 45),
            "down-right": (135, 45)
        }
        
        if direction in directions:
            pan, tilt = directions[direction]
            return self.move_to(pan, tilt)
        
        return {"status": "error", "message": f"ÐÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾Ðµ Ð½Ð°Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ: {direction}"}

    def track_speaker(self, x: int, y: int) -> Dict:
        """Ð¡Ð»ÐµÐ´Ð¸ÑÑ Ð·Ð° Ð³Ð¾Ð²Ð¾ÑÑÑÐ¸Ð¼ (ÐºÐ¾Ð¾ÑÐ´Ð¸Ð½Ð°ÑÑ Ð»Ð¸ÑÐ°)."""
        # ÐÑÐµÐ¾Ð±ÑÐ°Ð·Ð¾Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾ÑÐ´Ð¸Ð½Ð°Ñ ÐºÐ°Ð¼ÐµÑÑ Ð² ÑÐ³Ð»Ñ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð¾Ð²
        # ÐÑÐµÐ´Ð¿Ð¾Ð»Ð°Ð³Ð°ÐµÑÑÑ, ÑÑÐ¾ ÐºÐ°Ð¼ÐµÑÐ° Ð¸Ð¼ÐµÐµÑ ÑÐ³Ð¾Ð» Ð¾Ð±Ð·Ð¾ÑÐ° 60Â°
        
        # Ð¦ÐµÐ½ÑÑ Ð¸Ð·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ - ÑÐµÐ½ÑÑ ÑÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ð¾Ð²
        center_x = 320  # ÐÐ»Ñ ÐºÐ°Ð¼ÐµÑÑ 640x480
        center_y = 240
        
        # Ð¡Ð¼ÐµÑÐµÐ½Ð¸Ðµ Ð¾Ñ ÑÐµÐ½ÑÑÐ°
        offset_x = x - center_x
        offset_y = y - center_y
        
        # ÐÑÐµÐ¾Ð±ÑÐ°Ð·Ð¾Ð²Ð°Ð½Ð¸Ðµ Ð² ÑÐ³Ð»Ñ (Ð¿ÑÐ¸Ð¼ÐµÑÐ½Ð°Ñ ÑÐ¾ÑÐ¼ÑÐ»Ð°)
        pan_offset = (offset_x / center_x) * 45  # Â±45Â°
        tilt_offset = (offset_y / center_y) * 45  # Â±45Â°
        
        new_pan = int(self.pan_angle + pan_offset)
        new_tilt = int(self.tilt_angle - tilt_offset)  # ÐÐ½Ð²ÐµÑÑÐ¸Ñ Ð´Ð»Ñ ÐµÑÑÐµÑÑÐ²ÐµÐ½Ð½Ð¾Ð³Ð¾ Ð´Ð²Ð¸Ð¶ÐµÐ½Ð¸Ñ
        
        return self.move_to(new_pan, new_tilt)

    def center(self) -> Dict:
        """ÐÐµÑÐ½ÑÑÑ Ð² ÑÐµÐ½ÑÑÐ°Ð»ÑÐ½Ð¾Ðµ Ð¿Ð¾Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ."""
        return self.look_at("center")

    def nod(self) -> Dict:
        """ÐÐ¸Ð²Ð¾Ðº (Ð´Ð°)."""
        self.move_to(90, 110)
        time.sleep(0.3)
        self.move_to(90, 70)
        time.sleep(0.3)
        self.move_to(90, 90)
        return {"status": "ok", "message": "ÐÐ¸Ð²Ð¾Ðº"}

    def shake(self) -> Dict:
        """ÐÐ¾ÐºÐ°ÑÐ¸Ð²Ð°Ð½Ð¸Ðµ (Ð½ÐµÑ)."""
        self.move_to(70, 90)
        time.sleep(0.3)
        self.move_to(110, 90)
        time.sleep(0.3)
        self.move_to(90, 90)
        return {"status": "ok", "message": "ÐÐ¾ÐºÐ°ÑÐ¸Ð²Ð°Ð½Ð¸Ðµ"}

    def get_position(self) -> Tuple[int, int]:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐµÐºÑÑÑÑ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ñ."""
        return (self.pan_angle, self.tilt_angle)

    def cleanup(self):
        """ÐÑÐ¸ÑÑÐºÐ° ÑÐµÑÑÑÑÐ¾Ð²."""
        if self.initialized:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # self.pwm_pan.stop()
            # self.pwm_tilt.stop()
            # GPIO.cleanup()
            self.initialized = False
            self.logger.info("Ð¡ÐµÑÐ²Ð¾Ð¿ÑÐ¸Ð²Ð¾Ð´Ñ Ð¾ÑÐ¸ÑÐµÐ½Ñ")
