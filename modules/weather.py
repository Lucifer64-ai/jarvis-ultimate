"""
Weather Module - ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð¸ Ð¾ Ð¿Ð¾Ð³Ð¾Ð´Ðµ
"""

import requests
from typing import Dict, Optional
import logging


class WeatherModule:
    """ÐÐ¾Ð´ÑÐ»Ñ Ð´Ð»Ñ Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.api_key = brain.config.get_env("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # ÐÑÑ Ð´Ð»Ñåå° Ð·Ð°Ð¿ÑÐ¾ÑÐ¾Ð²
        self.cache = {}
        self.cache_timeout = 600  # 10 Ð¼Ð¸Ð½ÑÑ

    def get_weather(self, city: str = "ÐÐ¾ÑÐºÐ²Ð°") -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐµÐºÑÑÑÑ Ð¿Ð¾Ð³Ð¾Ð´Ñ."""
        if not self.api_key:
            return {"status": "error", "message": "API ÐºÐ»ÑÑ OpenWeather Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½"}
        
        try:
            # ÐÑÐ¾Ð²ÐµÑÐºÐ° ÐºÑÑÐ°
            cache_key = f"weather_{city}"
            if cache_key in self.cache:
                import time
                if time.time() - self.cache[cache_key]["time"] < self.cache_timeout:
                    return self.cache[cache_key]["data"]
            
            # ÐÐ°Ð¿ÑÐ¾Ñ Ðº API
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
            
            # Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¾ÑÐ²ÐµÑÐ°
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
            
            # Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð² ÐºÑÑ
            import time
            self.cache[cache_key] = {
                "data": weather_info,
                "time": time.time()
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ Ð¿Ð¾Ð³Ð¾Ð´Ñ: {e}")
            return {"status": "error", "message": f"ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ Ð¿Ð¾Ð³Ð¾Ð´Ñ: {e}"}
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¾Ð±ÑÐ°Ð±Ð¾ÑÐºÐ¸ Ð¿Ð¾Ð³Ð¾Ð´Ñ: {e}")
            return {"status": "error", "message": str(e)}

    def get_forecast(self, city: str = "ÐÐ¾ÑÐºÐ²Ð°", days: int = 5) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð¿ÑÐ¾Ð³Ð½Ð¾Ð· Ð¿Ð¾Ð³Ð¾Ð´Ñ."""
        if not self.api_key:
            return {"status": "error", "message": "API ÐºÐ»ÑÑ OpenWeather Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½"}
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru",
                "cnt": days * 8  # 8 Ð¸Ð½ÑÐµÑÐ²Ð°Ð»Ð¾Ð² Ð² Ð´ÐµÐ½Ñ (ÐºÐ°Ð¶Ð´ÑÐµ 3 ÑÐ°ÑÐ°)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # ÐÑÑÐ¿Ð¿Ð¸ÑÐ¾Ð²ÐºÐ° Ð¿Ð¾ Ð´Ð½ÑÐ¼
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
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ Ð¿ÑÐ¾Ð³Ð½Ð¾Ð·Ð°: {e}")
            return {"status": "error", "message": str(e)}

    def format_weather_message(self, weather: Dict) -> str:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¿Ð¾Ð³Ð¾Ð´Ñ Ð² ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ."""
        if weather["status"] != "ok":
            return weather["message"]
        
        return (
            f"Ð Ð³Ð¾ÑÐ¾Ð´Ðµ {weather['city']} ÑÐµÐ¹ÑÐ°Ñ {weather['temperature']}Â°C, "
            f"{weather['description']}. "
            f"ÐÑÑÑÐ°ÐµÑÑÑ ÐºÐ°Ðº {weather['feels_like']}Â°C. "
            f"ÐÐ»Ð°Ð¶Ð½Ð¾ÑÑÑ {weather['humidity']}%, Ð²ÐµÑÐµÑ {weather['wind_speed']} Ð¼/Ñ."
        )

    def format_forecast_message(self, forecast: Dict) -> str:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð¿ÑÐ¾Ð³Ð½Ð¾Ð·Ð° Ð² ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ."""
        if forecast["status"] != "ok":
            return forecast["message"]
        
        message = f"ÐÑÐ¾Ð³Ð½Ð¾Ð· Ð´Ð»Ñ {forecast['city']}:\n"
        for day in forecast["forecast"]:
            message += f"{day['date']}: Ð¾Ñ {day['temp_min']}Â°C Ð´Ð¾ {day['temp_max']}Â°C, {day['description']}\n"
        
        return message
