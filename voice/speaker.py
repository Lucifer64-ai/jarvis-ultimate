"""
Ð¡Ð¸Ð½ÑÐµÐ· ÑÐµÑÐ¸ JARVIS
"""

import pyttsx3
from typing import Optional


class VoiceSpeaker:
    """Ð¡Ð¸Ð½ÑÐµÐ· ÑÐµÑÐ¸."""

    def __init__(self, brain):
        self.brain = brain
        self.engine = pyttsx3.init()
        
        # ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° Ð³Ð¾Ð»Ð¾ÑÐ°
        voice_config = brain.config.get("voice", {})
        self.engine.setProperty('rate', voice_config.get("rate", 180))
        self.engine.setProperty('volume', voice_config.get("volume", 1.0))
        
        # ÐÑÐ±Ð¾Ñ ÑÑÑÑÐºÐ¾Ð³Ð¾ Ð³Ð¾Ð»Ð¾ÑÐ°
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def speak(self, text: str):
        """ÐÑÐ¾Ð¸Ð·Ð½ÐµÑÑÐ¸ ÑÐµÐºÑÑ."""
        try:
            self.brain.logger.info(f"ÐÐ¾Ð²Ð¾ÑÑ: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ¸Ð½ÑÐµÐ·Ð° ÑÐµÑÐ¸: {e}")

    def set_rate(self, rate: int):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÐºÐ¾ÑÐ¾ÑÑÑ ÑÐµÑÐ¸."""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑ."""
        self.engine.setProperty('volume', volume)
