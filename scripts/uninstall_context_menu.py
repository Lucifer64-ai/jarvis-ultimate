"""
ÃÃÂ¡ÃÃÂºÃÃÃÂ¸ÃÃÂ¿Ã ÃÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸Ã ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã ÃÃÂ¿ÃÃÃÂ¾ÃÃÂ²ÃÃÂ¾ÃÃÂ´ÃÃÂ½ÃÃÂ¸ÃÃÂºÃÃÂ° Windows
"""

import winreg
import sys


def uninstall_context_menu():
    """ÃÃÂ£ÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã."""
    try:
        # ÃÃÂ£ÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ´ÃÃÂ»Ã ÃÃÃÂ°ÃÃÂ¹ÃÃÂ»ÃÃÂ¾ÃÃÂ²
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JARVIS\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JARVIS")
        except:
            pass
        
        # ÃÃÂ£ÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ´ÃÃÂ»Ã ÃÃÂ¿ÃÃÂ°ÃÃÂ¿ÃÃÂ¾ÃÃÂº
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\JARVIS\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\JARVIS")
        except:
            pass
        
        print("ÃÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂµ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã ÃÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¾ ÃÃÃÃÂ¿ÃÃÂµÃÃÃÂ½ÃÃÂ¾")
        return 0
    
    except Exception as e:
        print(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÃÂ´ÃÃÂ°ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸Ã ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÃÂµÃÃÂºÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ³ÃÃÂ¾ ÃÃÂ¼ÃÃÂµÃÃÂ½Ã: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(uninstall_context_menu())
