"""
ÃÂ ÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÃÂµÃÃÂ¸ JARVIS
"""

import speech_recognition as sr
from typing import Optional, Dict


class VoiceListener:
    """ÃÂ ÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ³ÃÂ¾ÃÂ»ÃÂ¾ÃÃÂ¾ÃÂ²ÃÃ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´."""

    def __init__(self, brain):
        self.brain = brain
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = brain.config.get("voice", {}).get("wake_word", "ÃÂ´ÃÂ¶ÃÂ°ÃÃÂ²ÃÂ¸Ã")
        
        # ÃÃÂ°ÃÃÃÃÂ¾ÃÂ¹ÃÂºÃÂ° ÃÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300

    def listen(self) -> Optional[str]:
        """ÃÂ¡ÃÂ»ÃÃÃÂ°ÃÃ ÃÂ¸ ÃÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÃ ÃÃÂµÃÃ."""
        try:
            with self.microphone as source:
                self.brain.logger.info("ÃÂ¡ÃÂ»ÃÃÃÂ°Ã...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            self.brain.logger.info("ÃÂ ÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°Ã ÃÃÂµÃÃ...")
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            self.brain.logger.info(f"ÃÂ ÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ½ÃÂ¾: {text}")
            return text

        except sr.WaitTimeoutError:
            self.brain.logger.debug("ÃÂ¢ÃÂ°ÃÂ¹ÃÂ¼ÃÂ°ÃÃ ÃÂ¾ÃÂ¶ÃÂ¸ÃÂ´ÃÂ°ÃÂ½ÃÂ¸Ã ÃÃÂµÃÃÂ¸")
            return None
        except sr.UnknownValueError:
            self.brain.logger.debug("ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÃ ÃÃÂµÃÃ")
            return None
        except sr.RequestError as e:
            self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂµÃÃÂ²ÃÂ¸ÃÃÂ° ÃÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã: {e}")
            return None
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã: {e}")
            return None

    def listen_for_wake_word(self) -> bool:
        """ÃÂ¡ÃÂ»ÃÃÃÂ°ÃÃ wake word."""
        text = self.listen()
        if text and self.wake_word.lower() in text.lower():
            return True
        return False

    def continuous_listen(self, callback):
        """ÃÃÂµÃÂ¿ÃÃÂµÃÃÃÂ²ÃÂ½ÃÂ¾ÃÂµ ÃÂ¿ÃÃÂ¾ÃÃÂ»ÃÃÃÂ¸ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ."""
        while True:
            text = self.listen()
            if text:
                callback(text)
