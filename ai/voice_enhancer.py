"""
Ð£Ð»ÑÑÑÐµÐ½Ð¸Ðµ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ ÑÐµÑÐ¸ JARVIS
"""

import re
from typing import List, Dict


class VoiceEnhancer:
    """Ð£Ð»ÑÑÑÐµÐ½Ð¸Ðµ ÐºÐ°ÑÐµÑÑÐ²Ð° ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ ÑÐµÑÐ¸."""

    def __init__(self, brain):
        self.brain = brain
        self.corrections = self._load_corrections()

    def _load_corrections(self) -> Dict[str, str]:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° ÑÐ»Ð¾Ð²Ð°ÑÑ Ð¸ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ð¹."""
        return {
            # Ð§Ð°ÑÑÑÐµ Ð¾ÑÐ¸Ð±ÐºÐ¸ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ñ
            "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ": "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ",
            "jarvis": "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ",
            "Ð¶Ð°ÑÐ²Ð¸Ñ": "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ",
            "ÑÐ²Ð¸Ñ": "Ð´Ð¶Ð°ÑÐ²Ð¸Ñ",
            
            # Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
            "Ð²ÑÐºÐ»ÑÑÐ¸": "Ð²ÑÐºÐ»ÑÑÐ¸",
            "Ð²ÐºÐ»ÑÑÐ¸": "Ð²ÐºÐ»ÑÑÐ¸",
            "Ð¾ÑÐºÑÐ¾Ð¹": "Ð¾ÑÐºÑÐ¾Ð¹",
            "Ð·Ð°Ð¿ÑÑÑÐ¸": "Ð·Ð°Ð¿ÑÑÑÐ¸",
            "Ð¿Ð¾ÐºÐ°Ð¶Ð¸": "Ð¿Ð¾ÐºÐ°Ð¶Ð¸",
            
            # ÐÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ
            "Ð±Ð»Ð¾ÐºÐ½Ð¾Ñ": "Ð±Ð»Ð¾ÐºÐ½Ð¾Ñ",
            "notepad": "Ð±Ð»Ð¾ÐºÐ½Ð¾Ñ",
            "ÐºÐ°Ð»ÑÐºÑÐ»ÑÑÐ¾Ñ": "ÐºÐ°Ð»ÑÐºÑÐ»ÑÑÐ¾Ñ",
            "ÑÑÑÐ±": "youtube",
            "youtube": "youtube",
            "Ð³Ð¸ÑÑÐ°Ð±": "github",
            "github": "github",
            
            # ÐÐµÐ¹ÑÑÐ²Ð¸Ñ
            "Ð²ÑÐµÐ¼Ñ": "Ð²ÑÐµÐ¼Ñ",
            "Ð´Ð°ÑÐ°": "Ð´Ð°ÑÐ°",
            "Ð¿Ð¾Ð³Ð¾Ð´Ð°": "Ð¿Ð¾Ð³Ð¾Ð´Ð°",
            "ÑÐºÐ¾ÑÐ¾ÑÑÑ": "ÑÐºÐ¾ÑÐ¾ÑÑÑ",
            "Ð¸Ð½ÑÐµÑÐ½ÐµÑ": "Ð¸Ð½ÑÐµÑÐ½ÐµÑ",
        }

    def enhance(self, text: str) -> str:
        """Ð£Ð»ÑÑÑÐµÐ½Ð¸Ðµ ÑÐ°ÑÐ¿Ð¾Ð·Ð½Ð°Ð½Ð½Ð¾Ð³Ð¾ ÑÐµÐºÑÑÐ°."""
        if not text:
            return text
        
        # ÐÑÐ¸Ð²ÐµÐ´ÐµÐ½Ð¸Ðµ Ðº Ð½Ð¸Ð¶Ð½ÐµÐ¼Ñ ÑÐµÐ³Ð¸ÑÑÑÑ
        text = text.lower().strip()
        
        # Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ð»Ð¸ÑÐ½Ð¸Ñ Ð¿ÑÐ¾Ð±ÐµÐ»Ð¾Ð²
        text = re.sub(r'\s+', ' ', text)
        
        # ÐÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ°ÑÑÑÑ Ð¾ÑÐ¸Ð±Ð¾Ðº
        for wrong, correct in self.corrections.items():
            text = text.replace(wrong, correct)
        
        # Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ ÑÐ»Ð¾Ð²-Ð¿Ð°ÑÐ°Ð·Ð¸ÑÐ¾Ð²
        parasites = ["ÑÐ¼", "ÑÑ", "Ð½Ñ", "ÑÐ¸Ð¿Ð°", "ÐºÐ¾ÑÐ¾ÑÐµ"]
        for parasite in parasites:
            text = text.replace(parasite, "")
        
        # ÐÑÐ¸ÑÑÐºÐ° Ð¾Ñ Ð»Ð¸ÑÐ½Ð¸Ñ Ð¿ÑÐ¾Ð±ÐµÐ»Ð¾Ð² Ð¿Ð¾ÑÐ»Ðµ ÑÐ´Ð°Ð»ÐµÐ½Ð¸Ñ
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def extract_numbers(self, text: str) -> List[int]:
        """ÐÐ·Ð²Ð»ÐµÑÐµÐ½Ð¸Ðµ ÑÐ¸ÑÐµÐ» Ð¸Ð· ÑÐµÐºÑÑÐ°."""
        numbers = re.findall(r'\d+', text)
        return [int(n) for n in numbers]

    def extract_time(self, text: str) -> Dict:
        """ÐÐ·Ð²Ð»ÐµÑÐµÐ½Ð¸Ðµ Ð²ÑÐµÐ¼ÐµÐ½Ð¸ Ð¸Ð· ÑÐµÐºÑÑÐ°."""
        # ÐÐ°ÑÑÐµÑÐ½ Ð´Ð»Ñ Ð²ÑÐµÐ¼ÐµÐ½Ð¸ HH:MM
        time_pattern = r'(\d{1,2}):(\d{2})'
        match = re.search(time_pattern, text)
        
        if match:
            return {
                "hour": int(match.group(1)),
                "minute": int(match.group(2))
            }
        
        # ÐÐ°ÑÑÐµÑÐ½ Ð´Ð»Ñ "ÑÐµÑÐµÐ· N Ð¼Ð¸Ð½ÑÑ/ÑÐ°ÑÐ¾Ð²"
        relative_pattern = r'ÑÐµÑÐµÐ·\s+(\d+)\s+(Ð¼Ð¸Ð½ÑÑ|ÑÐ°Ñ|ÑÐµÐºÑÐ½Ð´)'
        match = re.search(relative_pattern, text)
        
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            return {
                "value": value,
                "unit": unit,
                "relative": True
            }
        
        return {}

    def extract_date(self, text: str) -> Dict:
        """ÐÐ·Ð²Ð»ÐµÑÐµÐ½Ð¸Ðµ Ð´Ð°ÑÑ Ð¸Ð· ÑÐµÐºÑÑÐ°."""
        # ÐÐ°ÑÑÐµÑÐ½ Ð´Ð»Ñ Ð´Ð°ÑÑ DD.MM.YYYY
        date_pattern = r'(\d{1,2})[.\-\/](\d{1,2})[.\-\/](\d{4})'
        match = re.search(date_pattern, text)
        
        if match:
            return {
                "day": int(match.group(1)),
                "month": int(match.group(2)),
                "year": int(match.group(3))
            }
        
        # ÐÑÐ½Ð¾ÑÐ¸ÑÐµÐ»ÑÐ½ÑÐµ Ð´Ð°ÑÑ
        if "Ð·Ð°Ð²ÑÑÐ°" in text:
            return {"relative": "tomorrow"}
        elif "Ð²ÑÐµÑÐ°" in text:
            return {"relative": "yesterday"}
        elif "ÑÐµÐ³Ð¾Ð´Ð½Ñ" in text:
            return {"relative": "today"}
        
        return {}

    def normalize_command(self, text: str) -> str:
        """ÐÐ¾ÑÐ¼Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð´Ð»Ñ Ð¾Ð±ÑÐ°Ð±Ð¾ÑÐºÐ¸."""
        text = self.enhance(text)
        
        # Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ wake word ÐµÑÐ»Ð¸ ÐµÑÑÑ
        wake_words = ["Ð´Ð¶Ð°ÑÐ²Ð¸Ñ", "jarvis"]
        for wake in wake_words:
            if text.startswith(wake):
                text = text[len(wake):].strip()
                break
        
        return text
