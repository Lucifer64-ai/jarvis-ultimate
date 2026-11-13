"""
Sensor Manager - ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ°ÃÂ¼ÃÂ¸ JARVIS
"""

import time
from typing import Dict, Optional, List
import logging


class SensorManager:
    """ÃÂ£ÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ°ÃÂ¼ÃÂ¸ JARVIS."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        
        # ÃÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸
        self.motion_detected = False
        self.distance_cm = 100.0
        self.temperature_c = 20.0
        self.humidity_percent = 50.0
        self.light_level = 500
        
        self.initialized = False

    def initialize(self) -> Dict:
        """ÃÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¾ÃÂ²."""
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # 
            # # PIR Motion Sensor
            # self.motion_pin = 22
            # GPIO.setup(self.motion_pin, GPIO.IN)
            # 
            # # Ultrasonic Distance Sensor
            # self.trig_pin = 23
            # self.echo_pin = 24
            # GPIO.setup(self.trig_pin, GPIO.OUT)
            # GPIO.setup(self.echo_pin, GPIO.IN)
            # 
            # # DHT22 Temperature/Humidity Sensor
            # import adafruit_dht
            # self.dht_pin = 17
            # self.dht_sensor = adafruit_dht.DHT22(self.dht_pin)
            
            self.initialized = True
            self.logger.info("ÃÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸ ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½Ã")
            return {"status": "ok", "message": "ÃÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸ ÃÂ³ÃÂ¾ÃÃÂ¾ÃÂ²Ã ÃÂº ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂµ"}
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¾ÃÂ²: {e}")
            return {"status": "error", "message": str(e)}

    def read_motion(self) -> bool:
        """ÃÂ§ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ° ÃÂ´ÃÂ²ÃÂ¸ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        if not self.initialized:
            return False
        
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # self.motion_detected = GPIO.input(self.motion_pin)
            # return self.motion_detected
            
            # ÃÃÂ»Ã ÃÂ´ÃÂµÃÂ¼ÃÂ¾ÃÂ½ÃÃÃÃÂ°ÃÃÂ¸ÃÂ¸ - ÃÃÂ»ÃÃÃÂ°ÃÂ¹ÃÂ½ÃÂ¾ÃÂµ ÃÂ·ÃÂ½ÃÂ°ÃÃÂµÃÂ½ÃÂ¸ÃÂµ
            import random
            self.motion_detected = random.choice([True, False])
            return self.motion_detected
        except:
            return False

    def read_distance(self) -> float:
        """ÃÂ§ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂ»ÃÃÃÃÂ°ÃÂ·ÃÂ²ÃÃÂºÃÂ¾ÃÂ²ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ° ÃÃÂ°ÃÃÃÃÂ¾ÃÃÂ½ÃÂ¸Ã."""
        if not self.initialized:
            return 100.0
        
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # GPIO.output(self.trig_pin, True)
            # time.sleep(0.00001)
            # GPIO.output(self.trig_pin, False)
            # 
            # pulse_start = time.time()
            # while GPIO.input(self.echo_pin) == 0:
            #     pulse_start = time.time()
            # 
            # while GPIO.input(self.echo_pin) == 1:
            #     pulse_end = time.time()
            # 
            # pulse_duration = pulse_end - pulse_start
            # distance = pulse_duration * 17150  # ÃÂ¡ÃÂºÃÂ¾ÃÃÂ¾ÃÃÃ ÃÂ·ÃÂ²ÃÃÂºÃÂ°
            # self.distance_cm = round(distance, 2)
            
            # ÃÃÂ»Ã ÃÂ´ÃÂµÃÂ¼ÃÂ¾ÃÂ½ÃÃÃÃÂ°ÃÃÂ¸ÃÂ¸
            import random
            self.distance_cm = random.uniform(10, 200)
            return self.distance_cm
        except:
            return 100.0

    def read_temperature(self) -> float:
        """ÃÂ§ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÃÂµÃÂ¼ÃÂ¿ÃÂµÃÃÂ°ÃÃÃÃ."""
        if not self.initialized:
            return 20.0
        
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # self.temperature_c = self.dht_sensor.temperature
            
            # ÃÃÂ»Ã ÃÂ´ÃÂµÃÂ¼ÃÂ¾ÃÂ½ÃÃÃÃÂ°ÃÃÂ¸ÃÂ¸
            import random
            self.temperature_c = random.uniform(18, 28)
            return round(self.temperature_c, 1)
        except:
            return 20.0

    def read_humidity(self) -> float:
        """ÃÂ§ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ²ÃÂ»ÃÂ°ÃÂ¶ÃÂ½ÃÂ¾ÃÃÃÂ¸."""
        if not self.initialized:
            return 50.0
        
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # self.humidity_percent = self.dht_sensor.humidity
            
            # ÃÃÂ»Ã ÃÂ´ÃÂµÃÂ¼ÃÂ¾ÃÂ½ÃÃÃÃÂ°ÃÃÂ¸ÃÂ¸
            import random
            self.humidity_percent = random.uniform(30, 70)
            return round(self.humidity_percent, 1)
        except:
            return 50.0

    def read_light(self) -> int:
        """ÃÂ§ÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ° ÃÂ¾ÃÃÂ²ÃÂµÃÃÂµÃÂ½ÃÂ½ÃÂ¾ÃÃÃÂ¸."""
        if not self.initialized:
            return 500
        
        try:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # import adafruit_mcp3xxx.mcp3008 as MCP
            # from adafruit_mcp3xxx.analog_in import AnalogIn
            # light_value = light.value
            
            # ÃÃÂ»Ã ÃÂ´ÃÂµÃÂ¼ÃÂ¾ÃÂ½ÃÃÃÃÂ°ÃÃÂ¸ÃÂ¸
            import random
            self.light_level = random.randint(0, 1000)
            return self.light_level
        except:
            return 500

    def get_all_readings(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ²ÃÃÂµ ÃÂ¿ÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÂ½ÃÂ¸Ã ÃÂ´ÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¾ÃÂ²."""
        return {
            "motion": self.read_motion(),
            "distance_cm": self.read_distance(),
            "temperature_c": self.read_temperature(),
            "humidity_percent": self.read_humidity(),
            "light_level": self.read_light()
        }

    def is_someone_present(self) -> bool:
        """ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂ¸ÃÃ ÃÂ¿ÃÃÂ¸ÃÃÃÃÃÃÂ²ÃÂ¸ÃÂµ ÃÃÂµÃÂ»ÃÂ¾ÃÂ²ÃÂµÃÂºÃÂ°."""
        motion = self.read_motion()
        distance = self.read_distance()
        
        # ÃÃÃÂ»ÃÂ¸ ÃÂµÃÃÃ ÃÂ´ÃÂ²ÃÂ¸ÃÂ¶ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÂ»ÃÂ¸ ÃÂºÃÃÂ¾-ÃÃÂ¾ ÃÂ±ÃÂ»ÃÂ¸ÃÂ·ÃÂºÃÂ¾
        return motion or distance < 100

    def get_environment_status(self) -> Dict:
        """ÃÂ¡ÃÃÂ°ÃÃÃ ÃÂ¾ÃÂºÃÃÃÂ¶ÃÂ°ÃÃÃÂµÃÂ¹ ÃÃÃÂµÃÂ´Ã."""
        temp = self.read_temperature()
        humidity = self.read_humidity()
        light = self.read_light()
        
        status = {
            "temperature": f"{temp}ÃÂ°C",
            "humidity": f"{humidity}%",
            "light": light,
            "comfort": "comfortable"
        }
        
        # ÃÃÃÂµÃÂ½ÃÂºÃÂ° ÃÂºÃÂ¾ÃÂ¼ÃÃÂ¾ÃÃÃÂ°
        if temp < 18 or temp > 26:
            status["comfort"] = "uncomfortable_temperature"
        elif humidity < 30 or humidity > 60:
            status["comfort"] = "uncomfortable_humidity"
        
        return status

    def cleanup(self):
        """ÃÃÃÂ¸ÃÃÃÂºÃÂ° ÃÃÂµÃÃÃÃÃÂ¾ÃÂ²."""
        if self.initialized:
            # Ã ÃÃÂµÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂµÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸:
            # GPIO.cleanup()
            self.initialized = False
            self.logger.info("ÃÃÂ°ÃÃÃÂ¸ÃÂºÃÂ¸ ÃÂ¾ÃÃÂ¸ÃÃÂµÃÂ½Ã")
