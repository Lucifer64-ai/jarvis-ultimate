"""
ÃÃÂ¡ÃÃÂºÃÃÃÂ¸ÃÃÂ¿Ã ÃÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂºÃÃÂ¸ ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã ÃÃÂ¿ÃÃÃÂ¾ÃÃÂ²ÃÃÂ¾ÃÃÂ´ÃÃÂ½ÃÃÂ¸ÃÃÂºÃÃÂ° Windows
"""

import winreg
import sys
import os
from pathlib import Path


def install_context_menu():
    """ÃÃÂ£ÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂºÃÃÂ° ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã."""
    try:
        # ÃÃÃÃ ÃÃÂº JARVIS
        jarvis_path = sys.executable
        
        # ÃÃÃÂ»Ã ÃÃÃÂ°ÃÃÂ¹ÃÃÂ»ÃÃÂ¾ÃÃÂ²
        file_key = r"*\shell\JARVIS"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "JARVIS - ÃÃÃÃÂºÃÃÃÃ ÃÃÃÂ°ÃÃÂ¹ÃÃÂ»")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, jarvis_path)
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{file_key}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{jarvis_path}" open "%1"')
        
        # ÃÃÃÂ»Ã ÃÃÂ¿ÃÃÂ°ÃÃÂ¿ÃÃÂ¾ÃÃÂº
        folder_key = r"Directory\shell\JARVIS"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, folder_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "JARVIS - ÃÃÃÃÂºÃÃÃÃ ÃÃÂ¿ÃÃÂ°ÃÃÂ¿ÃÃÂºÃ")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, jarvis_path)
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{folder_key}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{jarvis_path}" open "%1"')
        
        print("ÃÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂµ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã ÃÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¾ ÃÃÃÃÂ¿ÃÃÂµÃÃÃÂ½ÃÃÂ¾")
        return 0
    
    except Exception as e:
        print(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂºÃÃÂ¸ ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(install_context_menu())
