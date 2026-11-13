"""
ÃÃÂ¡ÃÃÂ¸ÃÃÂ½ÃÃÃÂµÃÃÂ· ÃÃÃÂµÃÃÃÂ¸ JARVIS
"""

import pyttsx3
from typing import Optional


class VoiceSpeaker:
    """ÃÃÂ¡ÃÃÂ¸ÃÃÂ½ÃÃÃÂµÃÃÂ· ÃÃÃÂµÃÃÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain
        self.engine = pyttsx3.init()
        
        # ÃÃÃÂ°ÃÃÃÃÃÂ¾ÃÃÂ¹ÃÃÂºÃÃÂ° ÃÃÂ³ÃÃÂ¾ÃÃÂ»ÃÃÂ¾ÃÃÃÂ°
        voice_config = brain.config.get("voice", {})
        self.engine.setProperty('rate', voice_config.get("rate", 180))
        self.engine.setProperty('volume', voice_config.get("volume", 1.0))
        
        # ÃÃÃÃÂ±ÃÃÂ¾Ã ÃÃÃÃÃÃÂºÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ³ÃÃÂ¾ÃÃÂ»ÃÃÂ¾ÃÃÃÂ°
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def speak(self, text: str):
        """ÃÃÃÃÂ¾ÃÃÂ¸ÃÃÂ·ÃÃÂ½ÃÃÂµÃÃÃÃÂ¸ ÃÃÃÂµÃÃÂºÃÃ."""
        try:
            self.brain.logger.info(f"ÃÃÃÂ¾ÃÃÂ²ÃÃÂ¾ÃÃ: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÃÂ¸ÃÃÂ½ÃÃÃÂµÃÃÂ·ÃÃÂ° ÃÃÃÂµÃÃÃÂ¸: {e}")

    def set_rate(self, rate: int):
        """ÃÃÂ£ÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ¸ÃÃ ÃÃÃÂºÃÃÂ¾ÃÃÃÂ¾ÃÃÃ ÃÃÃÂµÃÃÃÂ¸."""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        """ÃÃÂ£ÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ¸ÃÃ ÃÃÂ³ÃÃÃÂ¾ÃÃÂ¼ÃÃÂºÃÃÂ¾ÃÃÃ."""
        self.engine.setProperty('volume', volume)
