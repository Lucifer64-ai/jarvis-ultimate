"""
Ð¡ÐºÑÐ¸Ð¿Ñ ÑÑÑÐ°Ð½Ð¾Ð²ÐºÐ¸ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ Ð¿ÑÐ¾Ð²Ð¾Ð´Ð½Ð¸ÐºÐ° Windows
"""

import winreg
import sys
import os
from pathlib import Path


def install_context_menu():
    """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ."""
    try:
        # ÐÑÑÑ Ðº JARVIS
        jarvis_path = sys.executable
        
        # ÐÐ»Ñ ÑÐ°Ð¹Ð»Ð¾Ð²
        file_key = r"*\shell\JARVIS"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "JARVIS - ÐÑÐºÑÑÑÑ ÑÐ°Ð¹Ð»")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, jarvis_path)
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{file_key}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{jarvis_path}" open "%1"')
        
        # ÐÐ»Ñ Ð¿Ð°Ð¿Ð¾Ðº
        folder_key = r"Directory\shell\JARVIS"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, folder_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "JARVIS - ÐÑÐºÑÑÑÑ Ð¿Ð°Ð¿ÐºÑ")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, jarvis_path)
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{folder_key}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{jarvis_path}" open "%1"')
        
        print("ÐÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½Ð¾ ÑÑÐ¿ÐµÑÐ½Ð¾")
        return 0
    
    except Exception as e:
        print(f"ÐÑÐ¸Ð±ÐºÐ° ÑÑÑÐ°Ð½Ð¾Ð²ÐºÐ¸ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(install_context_menu())
