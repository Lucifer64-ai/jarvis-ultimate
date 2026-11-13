"""
ÐÐ¾ÐºÐ°Ð»ÑÐ½Ð°Ñ ÑÐ·ÑÐºÐ¾Ð²Ð°Ñ Ð¼Ð¾Ð´ÐµÐ»Ñ JARVIS (Ollama Ð¸Ð½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ)
"""

import requests
import json
from typing import Dict, List, Optional
import logging


class LocalLLM:
    """ÐÐ½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ Ñ Ð»Ð¾ÐºÐ°Ð»ÑÐ½Ð¾Ð¹ ÑÐ·ÑÐºÐ¾Ð²Ð¾Ð¹ Ð¼Ð¾Ð´ÐµÐ»ÑÑ ÑÐµÑÐµÐ· Ollama."""

    def __init__(self, brain):
        self.brain = brain
        self.ollama_url = brain.config.get("local_llm", {}).get("ollama_url", "http://localhost:11434")
        self.model = brain.config.get("local_llm", {}).get("model", "llama3.2")
        self.enabled = brain.config.get("local_llm", {}).get("enabled", False)
        
        if self.enabled:
            self.brain.logger.info(f"ÐÐ¾ÐºÐ°Ð»ÑÐ½Ð°Ñ LLM Ð²ÐºÐ»ÑÑÐµÐ½Ð°: {self.model} ÑÐµÑÐµÐ· {self.ollama_url}")
        else:
            self.brain.logger.info("ÐÐ¾ÐºÐ°Ð»ÑÐ½Ð°Ñ LLM Ð¾ÑÐºÐ»ÑÑÐµÐ½Ð°")

    def is_available(self) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐºÐ° Ð´Ð¾ÑÑÑÐ¿Ð½Ð¾ÑÑÐ¸ Ollama."""
        if not self.enabled:
            return False
        
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> List[str]:
        """Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð´Ð¾ÑÑÑÐ¿Ð½ÑÑ Ð¼Ð¾Ð´ÐµÐ»ÐµÐ¹."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿Ð¾Ð»ÑÑÐµÐ½Ð¸Ñ ÑÐ¿Ð¸ÑÐºÐ° Ð¼Ð¾Ð´ÐµÐ»ÐµÐ¹: {e}")
        
        return []

    def generate(self, prompt: str, system: str = None) -> Dict:
        """ÐÐµÐ½ÐµÑÐ°ÑÐ¸Ñ Ð¾ÑÐ²ÐµÑÐ°."""
        if not self.is_available():
            return {
                "status": "error",
                "message": "Ollama Ð½Ðµ Ð´Ð¾ÑÑÑÐ¿Ð½Ð°. Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÐµ Ñ https://ollama.ai"
            }
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "ok",
                    "response": data.get("response", ""),
                    "model": self.model,
                    "done": data.get("done", False)
                }
            else:
                return {
                    "status": "error",
                    "message": f"ÐÑÐ¸Ð±ÐºÐ° Ollama: {response.status_code}"
                }
        
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Ð¢Ð°Ð¹Ð¼Ð°ÑÑ Ð·Ð°Ð¿ÑÐ¾ÑÐ° Ðº Ollama"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def chat(self, messages: List[Dict]) -> Dict:
        """Ð§Ð°Ñ Ñ Ð¼Ð¾Ð´ÐµÐ»ÑÑ."""
        if not self.is_available():
            return {
                "status": "error",
                "message": "Ollama Ð½Ðµ Ð´Ð¾ÑÑÑÐ¿Ð½Ð°"
            }
        
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                message = data.get("message", {})
                return {
                    "status": "ok",
                    "response": message.get("content", ""),
                    "role": message.get("role", "assistant"),
                    "model": self.model
                }
            else:
                return {
                    "status": "error",
                    "message": f"ÐÑÐ¸Ð±ÐºÐ° Ollama: {response.status_code}"
                }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def set_model(self, model: str) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¼Ð¾Ð´ÐµÐ»Ð¸."""
        available = self.list_models()
        
        if model not in available:
            return {
                "status": "error",
                "message": f"ÐÐ¾Ð´ÐµÐ»Ñ '{model}' Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°. ÐÐ¾ÑÑÑÐ¿Ð½ÑÐµ: {', '.join(available)}"
            }
        
        self.model = model
        self.brain.config.set("local_llm.model", model)
        
        return {
            "status": "ok",
            "message": f"ÐÐ¾Ð´ÐµÐ»Ñ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð°: {model}"
        }

    def enable(self) -> Dict:
        """ÐÐºÐ»ÑÑÐµÐ½Ð¸Ðµ Ð»Ð¾ÐºÐ°Ð»ÑÐ½Ð¾Ð¹ LLM."""
        self.enabled = True
        self.brain.config.set("local_llm.enabled", True)
        return {"status": "ok", "message": "ÐÐ¾ÐºÐ°Ð»ÑÐ½Ð°Ñ LLM Ð²ÐºÐ»ÑÑÐµÐ½Ð°"}

    def disable(self) -> Dict:
        """ÐÑÐºÐ»ÑÑÐµÐ½Ð¸Ðµ Ð»Ð¾ÐºÐ°Ð»ÑÐ½Ð¾Ð¹ LLM."""
        self.enabled = False
        self.brain.config.set("local_llm.enabled", False)
        return {"status": "ok", "message": "ÐÐ¾ÐºÐ°Ð»ÑÐ½Ð°Ñ LLM Ð¾ÑÐºÐ»ÑÑÐµÐ½Ð°"}

    def get_status(self) -> Dict:
        """Ð¡ÑÐ°ÑÑÑ Ð»Ð¾ÐºÐ°Ð»ÑÐ½Ð¾Ð¹ LLM."""
        return {
            "enabled": self.enabled,
            "available": self.is_available(),
            "model": self.model,
            "ollama_url": self.ollama_url,
            "available_models": self.list_models() if self.is_available() else []
        }
