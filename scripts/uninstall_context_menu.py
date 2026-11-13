"""
ÃÂ¡ÃÂºÃÃÂ¸ÃÂ¿Ã ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂ¾ÃÂ´ÃÂ½ÃÂ¸ÃÂºÃÂ° Windows
"""

import winreg
import sys


def uninstall_context_menu():
    """ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã."""
    try:
        # ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ»Ã ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JARVIS\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JARVIS")
        except:
            pass
        
        # ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ»Ã ÃÂ¿ÃÂ°ÃÂ¿ÃÂ¾ÃÂº
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\JARVIS\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\JARVIS")
        except:
            pass
        
        print("ÃÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂµ ÃÂ¼ÃÂµÃÂ½Ã ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¾ ÃÃÃÂ¿ÃÂµÃÃÂ½ÃÂ¾")
        return 0
    
    except Exception as e:
        print(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã ÃÂºÃÂ¾ÃÂ½ÃÃÂµÃÂºÃÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¼ÃÂµÃÂ½Ã: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(uninstall_context_menu())
