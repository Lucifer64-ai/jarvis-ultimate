"""
ÃÂ¡ÃÂ¸ÃÂ½ÃÃÂµÃÂ· ÃÃÂµÃÃÂ¸ JARVIS
"""

import pyttsx3
from typing import Optional


class VoiceSpeaker:
    """ÃÂ¡ÃÂ¸ÃÂ½ÃÃÂµÃÂ· ÃÃÂµÃÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain
        self.engine = pyttsx3.init()
        
        # ÃÃÂ°ÃÃÃÃÂ¾ÃÂ¹ÃÂºÃÂ° ÃÂ³ÃÂ¾ÃÂ»ÃÂ¾ÃÃÂ°
        voice_config = brain.config.get("voice", {})
        self.engine.setProperty('rate', voice_config.get("rate", 180))
        self.engine.setProperty('volume', voice_config.get("volume", 1.0))
        
        # ÃÃÃÂ±ÃÂ¾Ã ÃÃÃÃÃÂºÃÂ¾ÃÂ³ÃÂ¾ ÃÂ³ÃÂ¾ÃÂ»ÃÂ¾ÃÃÂ°
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def speak(self, text: str):
        """ÃÃÃÂ¾ÃÂ¸ÃÂ·ÃÂ½ÃÂµÃÃÃÂ¸ ÃÃÂµÃÂºÃÃ."""
        try:
            self.brain.logger.info(f"ÃÃÂ¾ÃÂ²ÃÂ¾ÃÃ: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ¸ÃÂ½ÃÃÂµÃÂ·ÃÂ° ÃÃÂµÃÃÂ¸: {e}")

    def set_rate(self, rate: int):
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ¸ÃÃ ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃ ÃÃÂµÃÃÂ¸."""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ¸ÃÃ ÃÂ³ÃÃÂ¾ÃÂ¼ÃÂºÃÂ¾ÃÃÃ."""
        self.engine.setProperty('volume', volume)
