"""
Weather Module - ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÂ½ÃÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´ÃÂµ
"""

import requests
from typing import Dict, Optional
import logging


class WeatherModule:
    """ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ´ÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.api_key = brain.config.get_env("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # ÃÃÃ ÃÂ´ÃÂ»ÃÃ¥Ã¥Â° ÃÂ·ÃÂ°ÃÂ¿ÃÃÂ¾ÃÃÂ¾ÃÂ²
        self.cache = {}
        self.cache_timeout = 600  # 10 ÃÂ¼ÃÂ¸ÃÂ½ÃÃ

    def get_weather(self, city: str = "ÃÃÂ¾ÃÃÂºÃÂ²ÃÂ°") -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÃÂµÃÂºÃÃÃÃ ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã."""
        if not self.api_key:
            return {"status": "error", "message": "API ÃÂºÃÂ»ÃÃ OpenWeather ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÃÃÃÂ¾ÃÂµÃÂ½"}
        
        try:
            # ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° ÃÂºÃÃÃÂ°
            cache_key = f"weather_{city}"
            if cache_key in self.cache:
                import time
                if time.time() - self.cache[cache_key]["time"] < self.cache_timeout:
                    return self.cache[cache_key]["data"]
            
            # ÃÃÂ°ÃÂ¿ÃÃÂ¾Ã ÃÂº API
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¾ÃÃÂ²ÃÂµÃÃÂ°
            weather_info = {
                "status": "ok",
                "city": city,
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"]
            }
            
            # ÃÂ¡ÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ² ÃÂºÃÃ
            import time
            self.cache[cache_key] = {
                "data": weather_info,
                "time": time.time()
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã: {e}")
            return {"status": "error", "message": f"ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã: {e}"}
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¾ÃÂ±ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂºÃÂ¸ ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã: {e}")
            return {"status": "error", "message": str(e)}

    def get_forecast(self, city: str = "ÃÃÂ¾ÃÃÂºÃÂ²ÃÂ°", days: int = 5) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ¿ÃÃÂ¾ÃÂ³ÃÂ½ÃÂ¾ÃÂ· ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã."""
        if not self.api_key:
            return {"status": "error", "message": "API ÃÂºÃÂ»ÃÃ OpenWeather ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÃÃÃÂ¾ÃÂµÃÂ½"}
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru",
                "cnt": days * 8  # 8 ÃÂ¸ÃÂ½ÃÃÂµÃÃÂ²ÃÂ°ÃÂ»ÃÂ¾ÃÂ² ÃÂ² ÃÂ´ÃÂµÃÂ½Ã (ÃÂºÃÂ°ÃÂ¶ÃÂ´ÃÃÂµ 3 ÃÃÂ°ÃÃÂ°)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # ÃÃÃÃÂ¿ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¿ÃÂ¾ ÃÂ´ÃÂ½ÃÃÂ¼
            forecast = []
            for i in range(0, len(data["list"]), 8):
                day_data = data["list"][i:i+8]
                if day_data:
                    temps = [d["main"]["temp"] for d in day_data]
                    forecast.append({
                        "date": day_data[0]["dt_txt"].split()[0],
                        "temp_min": round(min(temps)),
                        "temp_max": round(max(temps)),
                        "description": day_data[4]["weather"]["description"] if len(day_data) > 4 else day_data[0]["weather"]["description"]
                    })
            
            return {
                "status": "ok",
                "city": city,
                "forecast": forecast[:days]
            }
            
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂ¿ÃÃÂ¾ÃÂ³ÃÂ½ÃÂ¾ÃÂ·ÃÂ°: {e}")
            return {"status": "error", "message": str(e)}

    def format_weather_message(self, weather: Dict) -> str:
        """ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÂ¾ÃÂ³ÃÂ¾ÃÂ´Ã ÃÂ² ÃÃÂ¾ÃÂ¾ÃÂ±ÃÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        if weather["status"] != "ok":
            return weather["message"]
        
        return (
            f"Ã ÃÂ³ÃÂ¾ÃÃÂ¾ÃÂ´ÃÂµ {weather['city']} ÃÃÂµÃÂ¹ÃÃÂ°Ã {weather['temperature']}ÃÂ°C, "
            f"{weather['description']}. "
            f"ÃÃÃÃÃÂ°ÃÂµÃÃÃ ÃÂºÃÂ°ÃÂº {weather['feels_like']}ÃÂ°C. "
            f"ÃÃÂ»ÃÂ°ÃÂ¶ÃÂ½ÃÂ¾ÃÃÃ {weather['humidity']}%, ÃÂ²ÃÂµÃÃÂµÃ {weather['wind_speed']} ÃÂ¼/Ã."
        )

    def format_forecast_message(self, forecast: Dict) -> str:
        """ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¾ÃÂ³ÃÂ½ÃÂ¾ÃÂ·ÃÂ° ÃÂ² ÃÃÂ¾ÃÂ¾ÃÂ±ÃÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        if forecast["status"] != "ok":
            return forecast["message"]
        
        message = f"ÃÃÃÂ¾ÃÂ³ÃÂ½ÃÂ¾ÃÂ· ÃÂ´ÃÂ»Ã {forecast['city']}:\n"
        for day in forecast["forecast"]:
            message += f"{day['date']}: ÃÂ¾Ã {day['temp_min']}ÃÂ°C ÃÂ´ÃÂ¾ {day['temp_max']}ÃÂ°C, {day['description']}\n"
        
        return message
