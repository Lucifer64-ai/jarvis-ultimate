"""
Sensor Manager - Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð´Ð°ÑÑÐ¸ÐºÐ°Ð¼Ð¸ JARVIS
"""

import time
from typing import Dict, Optional, List
import logging


class SensorManager:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð´Ð°ÑÑÐ¸ÐºÐ°Ð¼Ð¸ JARVIS."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        
        # ÐÐ°ÑÑÐ¸ÐºÐ¸
        self.motion_detected = False
        self.distance_cm = 100.0
        self.temperature_c = 20.0
        self.humidity_percent = 50.0
        self.light_level = 500
        
        self.initialized = False

    def initialize(self) -> Dict:
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð²."""
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
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
            self.logger.info("ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½Ñ")
            return {"status": "ok", "message": "ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð³Ð¾ÑÐ¾Ð²Ñ Ðº ÑÐ°Ð±Ð¾ÑÐµ"}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð²: {e}")
            return {"status": "error", "message": str(e)}

    def read_motion(self) -> bool:
        """Ð§ÑÐµÐ½Ð¸Ðµ Ð´Ð°ÑÑÐ¸ÐºÐ° Ð´Ð²Ð¸Ð¶ÐµÐ½Ð¸Ñ."""
        if not self.initialized:
            return False
        
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # self.motion_detected = GPIO.input(self.motion_pin)
            # return self.motion_detected
            
            # ÐÐ»Ñ Ð´ÐµÐ¼Ð¾Ð½ÑÑÑÐ°ÑÐ¸Ð¸ - ÑÐ»ÑÑÐ°Ð¹Ð½Ð¾Ðµ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ
            import random
            self.motion_detected = random.choice([True, False])
            return self.motion_detected
        except:
            return False

    def read_distance(self) -> float:
        """Ð§ÑÐµÐ½Ð¸Ðµ ÑÐ»ÑÑÑÐ°Ð·Ð²ÑÐºÐ¾Ð²Ð¾Ð³Ð¾ Ð´Ð°ÑÑÐ¸ÐºÐ° ÑÐ°ÑÑÑÐ¾ÑÐ½Ð¸Ñ."""
        if not self.initialized:
            return 100.0
        
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
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
            # distance = pulse_duration * 17150  # Ð¡ÐºÐ¾ÑÐ¾ÑÑÑ Ð·Ð²ÑÐºÐ°
            # self.distance_cm = round(distance, 2)
            
            # ÐÐ»Ñ Ð´ÐµÐ¼Ð¾Ð½ÑÑÑÐ°ÑÐ¸Ð¸
            import random
            self.distance_cm = random.uniform(10, 200)
            return self.distance_cm
        except:
            return 100.0

    def read_temperature(self) -> float:
        """Ð§ÑÐµÐ½Ð¸Ðµ ÑÐµÐ¼Ð¿ÐµÑÐ°ÑÑÑÑ."""
        if not self.initialized:
            return 20.0
        
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # self.temperature_c = self.dht_sensor.temperature
            
            # ÐÐ»Ñ Ð´ÐµÐ¼Ð¾Ð½ÑÑÑÐ°ÑÐ¸Ð¸
            import random
            self.temperature_c = random.uniform(18, 28)
            return round(self.temperature_c, 1)
        except:
            return 20.0

    def read_humidity(self) -> float:
        """Ð§ÑÐµÐ½Ð¸Ðµ Ð²Ð»Ð°Ð¶Ð½Ð¾ÑÑÐ¸."""
        if not self.initialized:
            return 50.0
        
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # self.humidity_percent = self.dht_sensor.humidity
            
            # ÐÐ»Ñ Ð´ÐµÐ¼Ð¾Ð½ÑÑÑÐ°ÑÐ¸Ð¸
            import random
            self.humidity_percent = random.uniform(30, 70)
            return round(self.humidity_percent, 1)
        except:
            return 50.0

    def read_light(self) -> int:
        """Ð§ÑÐµÐ½Ð¸Ðµ Ð´Ð°ÑÑÐ¸ÐºÐ° Ð¾ÑÐ²ÐµÑÐµÐ½Ð½Ð¾ÑÑÐ¸."""
        if not self.initialized:
            return 500
        
        try:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # import adafruit_mcp3xxx.mcp3008 as MCP
            # from adafruit_mcp3xxx.analog_in import AnalogIn
            # light_value = light.value
            
            # ÐÐ»Ñ Ð´ÐµÐ¼Ð¾Ð½ÑÑÑÐ°ÑÐ¸Ð¸
            import random
            self.light_level = random.randint(0, 1000)
            return self.light_level
        except:
            return 500

    def get_all_readings(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð²ÑÐµ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½Ð¸Ñ Ð´Ð°ÑÑÐ¸ÐºÐ¾Ð²."""
        return {
            "motion": self.read_motion(),
            "distance_cm": self.read_distance(),
            "temperature_c": self.read_temperature(),
            "humidity_percent": self.read_humidity(),
            "light_level": self.read_light()
        }

    def is_someone_present(self) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¿ÑÐ¸ÑÑÑÑÑÐ²Ð¸Ðµ ÑÐµÐ»Ð¾Ð²ÐµÐºÐ°."""
        motion = self.read_motion()
        distance = self.read_distance()
        
        # ÐÑÐ»Ð¸ ÐµÑÑÑ Ð´Ð²Ð¸Ð¶ÐµÐ½Ð¸Ðµ Ð¸Ð»Ð¸ ÐºÑÐ¾-ÑÐ¾ Ð±Ð»Ð¸Ð·ÐºÐ¾
        return motion or distance < 100

    def get_environment_status(self) -> Dict:
        """Ð¡ÑÐ°ÑÑÑ Ð¾ÐºÑÑÐ¶Ð°ÑÑÐµÐ¹ ÑÑÐµÐ´Ñ."""
        temp = self.read_temperature()
        humidity = self.read_humidity()
        light = self.read_light()
        
        status = {
            "temperature": f"{temp}Â°C",
            "humidity": f"{humidity}%",
            "light": light,
            "comfort": "comfortable"
        }
        
        # ÐÑÐµÐ½ÐºÐ° ÐºÐ¾Ð¼ÑÐ¾ÑÑÐ°
        if temp < 18 or temp > 26:
            status["comfort"] = "uncomfortable_temperature"
        elif humidity < 30 or humidity > 60:
            status["comfort"] = "uncomfortable_humidity"
        
        return status

    def cleanup(self):
        """ÐÑÐ¸ÑÑÐºÐ° ÑÐµÑÑÑÑÐ¾Ð²."""
        if self.initialized:
            # Ð ÑÐµÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:
            # GPIO.cleanup()
            self.initialized = False
            self.logger.info("ÐÐ°ÑÑÐ¸ÐºÐ¸ Ð¾ÑÐ¸ÑÐµÐ½Ñ")
