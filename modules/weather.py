"""
Weather Module - ÃÃÃÂ¾ÃÃÂ»ÃÃÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ¸ÃÃÂ½ÃÃÃÂ¾ÃÃÃÂ¼ÃÃÂ°ÃÃÃÂ¸ÃÃÂ¸ ÃÃÂ¾ ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´ÃÃÂµ
"""

import requests
from typing import Dict, Optional
import logging


class WeatherModule:
    """ÃÃÃÂ¾ÃÃÂ´ÃÃÃÂ»Ã ÃÃÂ´ÃÃÂ»Ã ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÃÂµÃÃÂ½ÃÃÂ¸Ã ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.api_key = brain.config.get_env("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # ÃÃÃ ÃÃÂ´ÃÃÂ»ÃÃÂ¥ÃÂ¥ÃÂ° ÃÃÂ·ÃÃÂ°ÃÃÂ¿ÃÃÃÂ¾ÃÃÃÂ¾ÃÃÂ²
        self.cache = {}
        self.cache_timeout = 600  # 10 ÃÃÂ¼ÃÃÂ¸ÃÃÂ½ÃÃ

    def get_weather(self, city: str = "ÃÃÃÂ¾ÃÃÃÂºÃÃÂ²ÃÃÂ°") -> Dict:
        """ÃÃÃÂ¾ÃÃÂ»ÃÃÃÃÂ¸ÃÃ ÃÃÃÂµÃÃÂºÃÃÃÃ ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã."""
        if not self.api_key:
            return {"status": "error", "message": "API ÃÃÂºÃÃÂ»ÃÃ OpenWeather ÃÃÂ½ÃÃÂµ ÃÃÂ½ÃÃÂ°ÃÃÃÃÃÂ¾ÃÃÂµÃÃÂ½"}
        
        try:
            # ÃÃÃÃÂ¾ÃÃÂ²ÃÃÂµÃÃÃÂºÃÃÂ° ÃÃÂºÃÃÃÃÂ°
            cache_key = f"weather_{city}"
            if cache_key in self.cache:
                import time
                if time.time() - self.cache[cache_key]["time"] < self.cache_timeout:
                    return self.cache[cache_key]["data"]
            
            # ÃÃÃÂ°ÃÃÂ¿ÃÃÃÂ¾Ã ÃÃÂº API
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
            
            # ÃÃÂ¤ÃÃÂ¾ÃÃÃÂ¼ÃÃÂ°ÃÃÃÂ¸ÃÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ¾ÃÃÃÂ²ÃÃÂµÃÃÃÂ°
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
            
            # ÃÃÂ¡ÃÃÂ¾ÃÃÃÃÂ°ÃÃÂ½ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ² ÃÃÂºÃÃ
            import time
            self.cache[cache_key] = {
                "data": weather_info,
                "time": time.time()
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÃÂµÃÃÂ½ÃÃÂ¸Ã ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã: {e}")
            return {"status": "error", "message": f"ÃÃÃÂµ ÃÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂ¾ÃÃ ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÃÂ¸ÃÃ ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã: {e}"}
        except Exception as e:
            self.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÂ¾ÃÃÂ±ÃÃÃÂ°ÃÃÂ±ÃÃÂ¾ÃÃÃÂºÃÃÂ¸ ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã: {e}")
            return {"status": "error", "message": str(e)}

    def get_forecast(self, city: str = "ÃÃÃÂ¾ÃÃÃÂºÃÃÂ²ÃÃÂ°", days: int = 5) -> Dict:
        """ÃÃÃÂ¾ÃÃÂ»ÃÃÃÃÂ¸ÃÃ ÃÃÂ¿ÃÃÃÂ¾ÃÃÂ³ÃÃÂ½ÃÃÂ¾ÃÃÂ· ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã."""
        if not self.api_key:
            return {"status": "error", "message": "API ÃÃÂºÃÃÂ»ÃÃ OpenWeather ÃÃÂ½ÃÃÂµ ÃÃÂ½ÃÃÂ°ÃÃÃÃÃÂ¾ÃÃÂµÃÃÂ½"}
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru",
                "cnt": days * 8  # 8 ÃÃÂ¸ÃÃÂ½ÃÃÃÂµÃÃÃÂ²ÃÃÂ°ÃÃÂ»ÃÃÂ¾ÃÃÂ² ÃÃÂ² ÃÃÂ´ÃÃÂµÃÃÂ½Ã (ÃÃÂºÃÃÂ°ÃÃÂ¶ÃÃÂ´ÃÃÃÂµ 3 ÃÃÃÂ°ÃÃÃÂ°)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # ÃÃÃÃÃÂ¿ÃÃÂ¿ÃÃÂ¸ÃÃÃÂ¾ÃÃÂ²ÃÃÂºÃÃÂ° ÃÃÂ¿ÃÃÂ¾ ÃÃÂ´ÃÃÂ½ÃÃÃÂ¼
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
            self.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÃÂµÃÃÂ½ÃÃÂ¸Ã ÃÃÂ¿ÃÃÃÂ¾ÃÃÂ³ÃÃÂ½ÃÃÂ¾ÃÃÂ·ÃÃÂ°: {e}")
            return {"status": "error", "message": str(e)}

    def format_weather_message(self, weather: Dict) -> str:
        """ÃÃÂ¤ÃÃÂ¾ÃÃÃÂ¼ÃÃÂ°ÃÃÃÂ¸ÃÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ¿ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ÃÃÂ´Ã ÃÃÂ² ÃÃÃÂ¾ÃÃÂ¾ÃÃÂ±ÃÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ."""
        if weather["status"] != "ok":
            return weather["message"]
        
        return (
            f"Ã ÃÃÂ³ÃÃÂ¾ÃÃÃÂ¾ÃÃÂ´ÃÃÂµ {weather['city']} ÃÃÃÂµÃÃÂ¹ÃÃÃÂ°Ã {weather['temperature']}ÃÃÂ°C, "
            f"{weather['description']}. "
            f"ÃÃÃÃÃÃÂ°ÃÃÂµÃÃÃ ÃÃÂºÃÃÂ°ÃÃÂº {weather['feels_like']}ÃÃÂ°C. "
            f"ÃÃÃÂ»ÃÃÂ°ÃÃÂ¶ÃÃÂ½ÃÃÂ¾ÃÃÃ {weather['humidity']}%, ÃÃÂ²ÃÃÂµÃÃÃÂµÃ {weather['wind_speed']} ÃÃÂ¼/Ã."
        )

    def format_forecast_message(self, forecast: Dict) -> str:
        """ÃÃÂ¤ÃÃÂ¾ÃÃÃÂ¼ÃÃÂ°ÃÃÃÂ¸ÃÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ¿ÃÃÃÂ¾ÃÃÂ³ÃÃÂ½ÃÃÂ¾ÃÃÂ·ÃÃÂ° ÃÃÂ² ÃÃÃÂ¾ÃÃÂ¾ÃÃÂ±ÃÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ."""
        if forecast["status"] != "ok":
            return forecast["message"]
        
        message = f"ÃÃÃÃÂ¾ÃÃÂ³ÃÃÂ½ÃÃÂ¾ÃÃÂ· ÃÃÂ´ÃÃÂ»Ã {forecast['city']}:\n"
        for day in forecast["forecast"]:
            message += f"{day['date']}: ÃÃÂ¾Ã {day['temp_min']}ÃÃÂ°C ÃÃÂ´ÃÃÂ¾ {day['temp_max']}ÃÃÂ°C, {day['description']}\n"
        
        return message
