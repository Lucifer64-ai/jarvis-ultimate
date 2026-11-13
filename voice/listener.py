"""
ÃÃÂ ÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÃÂµÃÃÃÂ¸ JARVIS
"""

import speech_recognition as sr
from typing import Optional, Dict


class VoiceListener:
    """ÃÃÂ ÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ³ÃÃÂ¾ÃÃÂ»ÃÃÂ¾ÃÃÃÂ¾ÃÃÂ²ÃÃ ÃÃÂºÃÃÂ¾ÃÃÂ¼ÃÃÂ°ÃÃÂ½ÃÃÂ´."""

    def __init__(self, brain):
        self.brain = brain
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = brain.config.get("voice", {}).get("wake_word", "ÃÃÂ´ÃÃÂ¶ÃÃÂ°ÃÃÃÂ²ÃÃÂ¸Ã")
        
        # ÃÃÃÂ°ÃÃÃÃÃÂ¾ÃÃÂ¹ÃÃÂºÃÃÂ° ÃÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸Ã
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300

    def listen(self) -> Optional[str]:
        """ÃÃÂ¡ÃÃÂ»ÃÃÃÃÂ°ÃÃ ÃÃÂ¸ ÃÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃ ÃÃÃÂµÃÃ."""
        try:
            with self.microphone as source:
                self.brain.logger.info("ÃÃÂ¡ÃÃÂ»ÃÃÃÃÂ°Ã...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            self.brain.logger.info("ÃÃÂ ÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°Ã ÃÃÃÂµÃÃ...")
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            self.brain.logger.info(f"ÃÃÂ ÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃÂ½ÃÃÂ¾: {text}")
            return text

        except sr.WaitTimeoutError:
            self.brain.logger.debug("ÃÃÂ¢ÃÃÂ°ÃÃÂ¹ÃÃÂ¼ÃÃÂ°ÃÃ ÃÃÂ¾ÃÃÂ¶ÃÃÂ¸ÃÃÂ´ÃÃÂ°ÃÃÂ½ÃÃÂ¸Ã ÃÃÃÂµÃÃÃÂ¸")
            return None
        except sr.UnknownValueError:
            self.brain.logger.debug("ÃÃÃÂµ ÃÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂ¾ÃÃ ÃÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃ ÃÃÃÂµÃÃ")
            return None
        except sr.RequestError as e:
            self.brain.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÃÂµÃÃÃÂ²ÃÃÂ¸ÃÃÃÂ° ÃÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸Ã: {e}")
            return None
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÃÂ°ÃÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ½ÃÃÂ°ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸Ã: {e}")
            return None

    def listen_for_wake_word(self) -> bool:
        """ÃÃÂ¡ÃÃÂ»ÃÃÃÃÂ°ÃÃ wake word."""
        text = self.listen()
        if text and self.wake_word.lower() in text.lower():
            return True
        return False

    def continuous_listen(self, callback):
        """ÃÃÃÂµÃÃÂ¿ÃÃÃÂµÃÃÃÃÂ²ÃÃÂ½ÃÃÂ¾ÃÃÂµ ÃÃÂ¿ÃÃÃÂ¾ÃÃÃÂ»ÃÃÃÃÂ¸ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ."""
        while True:
            text = self.listen()
            if text:
                callback(text)
