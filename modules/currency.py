"""
Currency Module - ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ ÐºÑÑÑÐ¾Ð² Ð²Ð°Ð»ÑÑ
"""

import requests
from typing import Dict, Optional
import logging


class CurrencyModule:
    """ÐÐ¾Ð´ÑÐ»Ñ Ð´Ð»Ñ Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ ÐºÑÑÑÐ¾Ð² Ð²Ð°Ð»ÑÑ."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        
        # ÐÑÑ
        self.cache = {}
        self.cache_timeout = 3600  # 1 ÑÐ°Ñ

    def get_rate(self, from_currency: str = "USD", to_currency: str = "RUB") -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÐºÑÑÑ Ð²Ð°Ð»ÑÑÑ."""
        try:
            # ÐÑÐ¾Ð²ÐµÑÐºÐ° ÐºÑÑÐ°
            cache_key = f"rate_{from_currency}_{to_currency}"
            if cache_key in self.cache:
                import time
                if time.time() - self.cache[cache_key]["time"] < self.cache_timeout:
                    return self.cache[cache_key]["data"]
            
            # ÐÐ°Ð¿ÑÐ¾Ñ Ðº API
            url = f"{self.base_url}/{from_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if to_currency not in data["rates"]:
                return {"status": "error", "message": f"ÐÐ°Ð»ÑÑÐ° {to_currency} Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}
            
            rate = data["rates"][to_currency]
            
            result = {
                "status": "ok",
                "from": from_currency,
                "to": to_currency,
                "rate": round(rate, 2),
                "date": data["date"]
            }
            
            # Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð² ÐºÑÑ
            import time
            self.cache[cache_key] = {
                "data": result,
                "time": time.time()
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ ÐºÑÑÑÐ°: {e}")
            return {"status": "error", "message": str(e)}

    def get_usd_rub(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÐºÑÑÑ USD Ðº RUB."""
        return self.get_rate("USD", "RUB")

    def get_eur_rub(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÐºÑÑÑ EUR Ðº RUB."""
        return self.get_rate("EUR", "RUB")

    def get_btc_usd(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÐºÑÑÑ Bitcoin Ðº USD."""
        try:
            url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            rate = data["bpi"]["USD"]["rate_float"]
            
            return {
                "status": "ok",
                "from": "BTC",
                "to": "USD",
                "rate": round(rate, 2)
            }
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ ÐºÑÑÑÐ° BTC: {e}")
            return {"status": "error", "message": str(e)}

    def format_rate_message(self, rate: Dict) -> str:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÐºÑÑÑÐ° Ð² ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ."""
        if rate["status"] != "ok":
            return rate["message"]
        
        return f"ÐÑÑÑ {rate['from']} Ðº {rate['to']}: {rate['rate']}"

    def get_multiple_rates(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð½ÐµÑÐºÐ¾Ð»ÑÐºÐ¾ Ð¾ÑÐ½Ð¾Ð²Ð½ÑÑ ÐºÑÑÑÐ¾Ð²."""
        usd_rub = self.get_usd_rub()
        eur_rub = self.get_eur_rub()
        btc_usd = self.get_btc_usd()
        
        return {
            "status": "ok",
            "usd_rub": usd_rub.get("rate") if usd_rub["status"] == "ok" else None,
            "eur_rub": eur_rub.get("rate") if eur_rub["status"] == "ok" else None,
            "btc_usd": btc_usd.get("rate") if btc_usd["status"] == "ok" else None
        }

    def format_multiple_rates_message(self, rates: Dict) -> str:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð½ÐµÑÐºÐ¾Ð»ÑÐºÐ¸Ñ ÐºÑÑÑÐ¾Ð²."""
        if rates["status"] != "ok":
            return "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ ÐºÑÑÑÑ Ð²Ð°Ð»ÑÑ"
        
        message = "ÐÑÑÑÑ Ð²Ð°Ð»ÑÑ:\n"
        if rates["usd_rub"]:
            message += f"USD/RUB: {rates['usd_rub']}\n"
        if rates["eur_rub"]:
            message += f"EUR/RUB: {rates['eur_rub']}\n"
        if rates["btc_usd"]:
            message += f"BTC/USD: ${rates['btc_usd']}"
        
        return message
