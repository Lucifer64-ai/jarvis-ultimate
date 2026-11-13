"""
News Module - ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹
"""

import requests
from typing import Dict, List, Optional
import logging


class NewsModule:
    """ÐÐ¾Ð´ÑÐ»Ñ Ð´Ð»Ñ Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.api_key = brain.config.get_env("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        
        # ÐÑÑ
        self.cache = {}
        self.cache_timeout = 900  # 15 Ð¼Ð¸Ð½ÑÑ

    def get_top_headlines(self, country: str = "ru", category: str = "general", page_size: int = 5) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð³Ð»Ð°Ð²Ð½ÑÐµ Ð½Ð¾Ð²Ð¾ÑÑÐ¸."""
        if not self.api_key:
            return {"status": "error", "message": "API ÐºÐ»ÑÑ NewsAPI Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½"}
        
        try:
            # ÐÑÐ¾Ð²ÐµÑÐºÐ° ÐºÑÑÐ°
            cache_key = f"news_{country}_{category}"
            if cache_key in self.cache:
                import time
                if time.time() - self.cache[cache_key]["time"] < self.cache_timeout:
                    return self.cache[cache_key]["data"]
            
            # ÐÐ°Ð¿ÑÐ¾Ñ Ðº API
            url = f"{self.base_url}/top-headlines"
            params = {
                "country": country,
                "category": category,
                "pageSize": page_size,
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "url": article.get("url", ""),
                    "published_at": article.get("publishedAt", "")
                })
            
            result = {
                "status": "ok",
                "total": data.get("totalResults", 0),
                "articles": articles
            }
            
            # Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð² ÐºÑÑ
            import time
            self.cache[cache_key] = {
                "data": result,
                "time": time.time()
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹: {e}")
            return {"status": "error", "message": str(e)}

    def get_tech_news(self, page_size: int = 5) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð½Ð¾Ð²Ð¾ÑÑÐ¸ ÑÐµÑÐ½Ð¾Ð»Ð¾Ð³Ð¸Ð¹."""
        return self.get_top_headlines(country="ru", category="technology", page_size=page_size)

    def get_business_news(self, page_size: int = 5) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð±Ð¸Ð·Ð½ÐµÑ Ð½Ð¾Ð²Ð¾ÑÑÐ¸."""
        return self.get_top_headlines(country="ru", category="business", page_size=page_size)

    def get_sports_news(self, page_size: int = 5) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÐ¿Ð¾ÑÑÐ¸Ð²Ð½ÑÐµ Ð½Ð¾Ð²Ð¾ÑÑÐ¸."""
        return self.get_top_headlines(country="ru", category="sports", page_size=page_size)

    def format_news_message(self, news: Dict, max_items: int = 3) -> str:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹ Ð² ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ."""
        if news["status"] != "ok":
            return news["message"]
        
        if not news["articles"]:
            return "ÐÐ¾Ð²Ð¾ÑÑÐ¸ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ñ"
        
        message = f"ÐÐ»Ð°Ð²Ð½ÑÐµ Ð½Ð¾Ð²Ð¾ÑÑÐ¸ ({news['total']} Ð²ÑÐµÐ³Ð¾):\n\n"
        
        for i, article in enumerate(news["articles"][:max_items], 1):
            message += f"{i}. {article['title']}\n"
            if article['description']:
                message += f"   {article['description'][:100]}...\n"
            message += f"   ÐÑÑÐ¾ÑÐ½Ð¸Ðº: {article['source']}\n\n"
        
        return message

    def search_news(self, query: str, page_size: int = 5) -> Dict:
        """ÐÐ¾Ð¸ÑÐº Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹ Ð¿Ð¾ Ð·Ð°Ð¿ÑÐ¾ÑÑ."""
        if not self.api_key:
            return {"status": "error", "message": "API ÐºÐ»ÑÑ NewsAPI Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½"}
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                "q": query,
                "pageSize": page_size,
                "sortBy": "publishedAt",
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "url": article.get("url", "")
                })
            
            return {
                "status": "ok",
                "total": data.get("totalResults", 0),
                "articles": articles
            }
            
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð¸ÑÐºÐ° Ð½Ð¾Ð²Ð¾ÑÑÐµÐ¹: {e}")
            return {"status": "error", "message": str(e)}
