"""
Ð¡ÐºÑÐ¸Ð¿Ñ ÑÐ´Ð°Ð»ÐµÐ½Ð¸Ñ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ Ð¿ÑÐ¾Ð²Ð¾Ð´Ð½Ð¸ÐºÐ° Windows
"""

import winreg
import sys


def uninstall_context_menu():
    """Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ."""
    try:
        # Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ð´Ð»Ñ ÑÐ°Ð¹Ð»Ð¾Ð²
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JARVIS\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JARVIS")
        except:
            pass
        
        # Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ð´Ð»Ñ Ð¿Ð°Ð¿Ð¾Ðº
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\JARVIS\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\JARVIS")
        except:
            pass
        
        print("ÐÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ðµ Ð¼ÐµÐ½Ñ ÑÐ´Ð°Ð»ÐµÐ½Ð¾ ÑÑÐ¿ÐµÑÐ½Ð¾")
        return 0
    
    except Exception as e:
        print(f"ÐÑÐ¸Ð±ÐºÐ° ÑÐ´Ð°Ð»ÐµÐ½Ð¸Ñ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÐ½Ñ: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(uninstall_context_menu())
