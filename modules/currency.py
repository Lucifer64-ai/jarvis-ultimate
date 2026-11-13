"""
Currency Module - ÃÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÃÃÃÂ¾ÃÂ² ÃÂ²ÃÂ°ÃÂ»ÃÃ
"""

import requests
from typing import Dict, Optional
import logging


class CurrencyModule:
    """ÃÃÂ¾ÃÂ´ÃÃÂ»Ã ÃÂ´ÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂºÃÃÃÃÂ¾ÃÂ² ÃÂ²ÃÂ°ÃÂ»ÃÃ."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        
        # ÃÃÃ
        self.cache = {}
        self.cache_timeout = 3600  # 1 ÃÃÂ°Ã

    def get_rate(self, from_currency: str = "USD", to_currency: str = "RUB") -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂºÃÃÃ ÃÂ²ÃÂ°ÃÂ»ÃÃÃ."""
        try:
            # ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° ÃÂºÃÃÃÂ°
            cache_key = f"rate_{from_currency}_{to_currency}"
            if cache_key in self.cache:
                import time
                if time.time() - self.cache[cache_key]["time"] < self.cache_timeout:
                    return self.cache[cache_key]["data"]
            
            # ÃÃÂ°ÃÂ¿ÃÃÂ¾Ã ÃÂº API
            url = f"{self.base_url}/{from_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if to_currency not in data["rates"]:
                return {"status": "error", "message": f"ÃÃÂ°ÃÂ»ÃÃÃÂ° {to_currency} ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ°"}
            
            rate = data["rates"][to_currency]
            
            result = {
                "status": "ok",
                "from": from_currency,
                "to": to_currency,
                "rate": round(rate, 2),
                "date": data["date"]
            }
            
            # ÃÂ¡ÃÂ¾ÃÃÃÂ°ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ² ÃÂºÃÃ
            import time
            self.cache[cache_key] = {
                "data": result,
                "time": time.time()
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂºÃÃÃÃÂ°: {e}")
            return {"status": "error", "message": str(e)}

    def get_usd_rub(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂºÃÃÃ USD ÃÂº RUB."""
        return self.get_rate("USD", "RUB")

    def get_eur_rub(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂºÃÃÃ EUR ÃÂº RUB."""
        return self.get_rate("EUR", "RUB")

    def get_btc_usd(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂºÃÃÃ Bitcoin ÃÂº USD."""
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
            self.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÂºÃÃÃÃÂ° BTC: {e}")
            return {"status": "error", "message": str(e)}

    def format_rate_message(self, rate: Dict) -> str:
        """ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÃÃÃÂ° ÃÂ² ÃÃÂ¾ÃÂ¾ÃÂ±ÃÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        if rate["status"] != "ok":
            return rate["message"]
        
        return f"ÃÃÃÃ {rate['from']} ÃÂº {rate['to']}: {rate['rate']}"

    def get_multiple_rates(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ½ÃÂµÃÃÂºÃÂ¾ÃÂ»ÃÃÂºÃÂ¾ ÃÂ¾ÃÃÂ½ÃÂ¾ÃÂ²ÃÂ½ÃÃ ÃÂºÃÃÃÃÂ¾ÃÂ²."""
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
        """ÃÂ¤ÃÂ¾ÃÃÂ¼ÃÂ°ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ½ÃÂµÃÃÂºÃÂ¾ÃÂ»ÃÃÂºÃÂ¸Ã ÃÂºÃÃÃÃÂ¾ÃÂ²."""
        if rates["status"] != "ok":
            return "ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂºÃÃÃÃ ÃÂ²ÃÂ°ÃÂ»ÃÃ"
        
        message = "ÃÃÃÃÃ ÃÂ²ÃÂ°ÃÂ»ÃÃ:\n"
        if rates["usd_rub"]:
            message += f"USD/RUB: {rates['usd_rub']}\n"
        if rates["eur_rub"]:
            message += f"EUR/RUB: {rates['eur_rub']}\n"
        if rates["btc_usd"]:
            message += f"BTC/USD: ${rates['btc_usd']}"
        
        return message
