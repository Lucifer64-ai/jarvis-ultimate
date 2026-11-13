"""
Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ðµ ÑÐµÑÐ¸ JARVIS
"""

import speech_recognition as sr
from typing import Optional, Dict


class VoiceListener:
    """Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ðµ Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´."""

    def __init__(self, brain):
        self.brain = brain
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = brain.config.get("voice", {}).get("wake_word", "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ")
        
        # ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300

    def listen(self) -> Optional[str]:
        """Ð¡Ð»ÑÑÐ°ÑÑ Ð¸ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°ÑÑ ÑÐµÑÑ."""
        try:
            with self.microphone as source:
                self.brain.logger.info("Ð¡Ð»ÑÑÐ°Ñ...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            self.brain.logger.info("Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ñ ÑÐµÑÑ...")
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            self.brain.logger.info(f"Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð½Ð¾: {text}")
            return text

        except sr.WaitTimeoutError:
            self.brain.logger.debug("Ð¢Ð°Ð¹Ð¼Ð°ÑÑ Ð¾Ð¶Ð¸Ð´Ð°Ð½Ð¸Ñ ÑÐµÑÐ¸")
            return None
        except sr.UnknownValueError:
            self.brain.logger.debug("ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°ÑÑ ÑÐµÑÑ")
            return None
        except sr.RequestError as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐµÑÐ²Ð¸ÑÐ° ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ: {e}")
            return None
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ: {e}")
            return None

    def listen_for_wake_word(self) -> bool:
        """Ð¡Ð»ÑÑÐ°ÑÑ wake word."""
        text = self.listen()
        if text and self.wake_word.lower() in text.lower():
            return True
        return False

    def continuous_listen(self, callback):
        """ÐÐµÐ¿ÑÐµÑÑÐ²Ð½Ð¾Ðµ Ð¿ÑÐ¾ÑÐ»ÑÑÐ¸Ð²Ð°Ð½Ð¸Ðµ."""
        while True:
            text = self.listen()
            if text:
                callback(text)
