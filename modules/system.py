"""
Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐµ Ð¾Ð¿ÐµÑÐ°ÑÐ¸Ð¸ JARVIS
"""

import os
import subprocess
import ctypes
from typing import Dict


class SystemModule:
    """Ð£Ð¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ¸ÑÑÐµÐ¼Ð½ÑÐ¼Ð¸ Ð¾Ð¿ÐµÑÐ°ÑÐ¸ÑÐ¼Ð¸."""

    def __init__(self, brain):
        self.brain = brain

    def shutdown(self) -> Dict:
        """ÐÑÐºÐ»ÑÑÐµÐ½Ð¸Ðµ ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑÐ°."""
        try:
            os.system("shutdown /s /t 60")
            return {"status": "ok", "message": "ÐÐ¾Ð¼Ð¿ÑÑÑÐµÑ Ð±ÑÐ´ÐµÑ Ð²ÑÐºÐ»ÑÑÐµÐ½ ÑÐµÑÐµÐ· 60 ÑÐµÐºÑÐ½Ð´"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def restart(self) -> Dict:
        """ÐÐµÑÐµÐ·Ð°Ð³ÑÑÐ·ÐºÐ° ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑÐ°."""
        try:
            os.system("shutdown /r /t 60")
            return {"status": "ok", "message": "ÐÐ¾Ð¼Ð¿ÑÑÑÐµÑ Ð±ÑÐ´ÐµÑ Ð¿ÐµÑÐµÐ·Ð°Ð³ÑÑÐ¶ÐµÐ½ ÑÐµÑÐµÐ· 60 ÑÐµÐºÑÐ½Ð´"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def cancel_shutdown(self) -> Dict:
        """ÐÑÐ¼ÐµÐ½Ð° Ð²ÑÐºÐ»ÑÑÐµÐ½Ð¸Ñ."""
        try:
            os.system("shutdown /a")
            return {"status": "ok", "message": "ÐÑÐºÐ»ÑÑÐµÐ½Ð¸Ðµ Ð¾ÑÐ¼ÐµÐ½ÐµÐ½Ð¾"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def lock_screen(self) -> Dict:
        """ÐÐ»Ð¾ÐºÐ¸ÑÐ¾Ð²ÐºÐ° ÑÐºÑÐ°Ð½Ð°."""
        try:
            ctypes.windll.user32.LockWorkStation()
            return {"status": "ok", "message": "Ð­ÐºÑÐ°Ð½ Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÐ¾Ð²Ð°Ð½"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def sleep(self) -> Dict:
        """Ð¡Ð¿ÑÑÐ¸Ð¹ ÑÐµÐ¶Ð¸Ð¼."""
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return {"status": "ok", "message": "ÐÐµÑÐµÑÐ¾Ð´ Ð² ÑÐ¿ÑÑÐ¸Ð¹ ÑÐµÐ¶Ð¸Ð¼"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def hibernate(self) -> Dict:
        """ÐÐ¸Ð±ÐµÑÐ½Ð°ÑÐ¸Ñ."""
        try:
            os.system("shutdown /h")
            return {"status": "ok", "message": "ÐÐµÑÐµÑÐ¾Ð´ Ð² ÑÐµÐ¶Ð¸Ð¼ Ð³Ð¸Ð±ÐµÑÐ½Ð°ÑÐ¸Ð¸"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def logoff(self) -> Dict:
        """ÐÑÑÐ¾Ð´ Ð¸Ð· ÑÐ¸ÑÑÐµÐ¼Ñ."""
        try:
            os.system("shutdown /l")
            return {"status": "ok", "message": "ÐÑÑÐ¾Ð´ Ð¸Ð· ÑÐ¸ÑÑÐµÐ¼Ñ"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
