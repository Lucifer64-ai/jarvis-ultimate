"""
ÃÂ¡ÃÂºÃÃÂ¸ÃÂ¿Ã ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ¸ ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ´ÃÂ½ÃÂ¸ÃÂºÃÂ° Windows
"""

import winreg
import sys
import os
from pathlib import Path


def install_context_menu():
    """ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã."""
    try:
        # ÃÃÃÃ ÃÂº JARVIS
        jarvis_path = sys.executable
        
        # ÃÃÂ»Ã ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²
        file_key = r"*\shell\JARVIS"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "JARVIS - ÃÃÃÂºÃÃÃÃ ÃÃÂ°ÃÂ¹ÃÂ»")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, jarvis_path)
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{file_key}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{jarvis_path}" open "%1"')
        
        # ÃÃÂ»Ã ÃÂ¿ÃÂ°ÃÂ¿ÃÂ¾ÃÂº
        folder_key = r"Directory\shell\JARVIS"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, folder_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "JARVIS - ÃÃÃÂºÃÃÃÃ ÃÂ¿ÃÂ°ÃÂ¿ÃÂºÃ")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, jarvis_path)
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{folder_key}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{jarvis_path}" open "%1"')
        
        print("ÃÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¾ ÃÃÃÂ¿ÃÂµÃÃÂ½ÃÂ¾")
        return 0
    
    except Exception as e:
        print(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ¸ ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(install_context_menu())
