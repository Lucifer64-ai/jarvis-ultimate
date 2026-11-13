"""
Wake Word ÑÐµÑÐ²Ð¸Ñ - ÑÐ¾Ð½Ð¾Ð²Ð¾Ðµ Ð¿ÑÐ¾ÑÐ»ÑÑÐ¸Ð²Ð°Ð½Ð¸Ðµ "ÐÐ¶Ð°ÑÐ²Ð¸Ñ"
"""

import threading
import queue
import time
from typing import Dict, Optional, Callable
import logging


class WakeWordService:
    """Ð¡ÐµÑÐ²Ð¸Ñ ÑÐ¾Ð½Ð¾Ð²Ð¾Ð³Ð¾ Ð¿ÑÐ¾ÑÐ»ÑÑÐ¸Ð²Ð°Ð½Ð¸Ñ wake word."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.wake_word = brain.config.get("voice.wake_word", "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ")
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.callback: Optional[Callable] = None

    def start(self, callback: Callable = None) -> Dict:
        """ÐÐ°Ð¿ÑÑÐº ÑÐµÑÐ²Ð¸ÑÐ°."""
        if self.running:
            return {"status": "error", "message": "Ð¡ÐµÑÐ²Ð¸Ñ ÑÐ¶Ðµ Ð·Ð°Ð¿ÑÑÐµÐ½"}
        
        self.callback = callback
        self.running = True
        
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        
        self.logger.info(f"Wake word ÑÐµÑÐ²Ð¸Ñ Ð·Ð°Ð¿ÑÑÐµÐ½. Ð¡Ð»ÑÑÐ°Ñ '{self.wake_word}'")
        return {"status": "ok", "message": f"Ð¡Ð»ÑÑÐ°Ñ '{self.wake_word}'"}

    def stop(self) -> Dict:
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÑÐµÑÐ²Ð¸ÑÐ°."""
        if not self.running:
            return {"status": "error", "message": "Ð¡ÐµÑÐ²Ð¸Ñ Ð½Ðµ Ð·Ð°Ð¿ÑÑÐµÐ½"}
        
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=2)
        
        self.logger.info("Wake word ÑÐµÑÐ²Ð¸Ñ Ð¾ÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½")
        return {"status": "ok", "message": "Ð¡ÐµÑÐ²Ð¸Ñ Ð¾ÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½"}

    def _listen_loop(self):
        """Ð¦Ð¸ÐºÐ» Ð¿ÑÐ¾ÑÐ»ÑÑÐ¸Ð²Ð°Ð½Ð¸Ñ."""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            self.logger.info("Wake word: Ð¼Ð¸ÐºÑÐ¾ÑÐ¾Ð½ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½")
            
            while self.running:
                try:
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
                    
                    # Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ðµ
                    try:
                        text = recognizer.recognize_google(audio, language="ru-RU")
                        text_lower = text.lower().strip()
                        
                        # ÐÑÐ¾Ð²ÐµÑÐºÐ° wake word
                        if self.wake_word in text_lower:
                            self.logger.info(f"Wake word Ð¾Ð±Ð½Ð°ÑÑÐ¶ÐµÐ½: {text}")
                            
                            if self.callback:
                                self.callback(text)
                    
                    except sr.UnknownValueError:
                        pass  # ÐÐµ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð½Ð¾
                    except sr.RequestError as e:
                        self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ: {e}")
                
                except Exception as e:
                    # Ð¢Ð°Ð¹Ð¼Ð°ÑÑ Ð¸Ð»Ð¸ Ð´ÑÑÐ³Ð°Ñ Ð¾ÑÐ¸Ð±ÐºÐ° - Ð¿ÑÐ¾Ð´Ð¾Ð»Ð¶Ð°ÐµÐ¼
                    pass
                
                time.sleep(0.1)
        
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° wake word ÑÐµÑÐ²Ð¸ÑÐ°: {e}")

    def is_running(self) -> bool:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ, Ð·Ð°Ð¿ÑÑÐµÐ½ Ð»Ð¸ ÑÐµÑÐ²Ð¸Ñ."""
        return self.running

    def set_wake_word(self, wake_word: str) -> Dict:
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ wake word."""
        self.wake_word = wake_word.lower().strip()
        self.brain.config.set("voice.wake_word", self.wake_word)
        self.logger.info(f"Wake word ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½: {self.wake_word}")
        return {"status": "ok", "message": f"Wake word: {self.wake_word}"}
