"""
JARVIS Ultimate - Ð¢Ð¾ÑÐºÐ° Ð²ÑÐ¾Ð´Ð° Ñ HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹ÑÐ¾Ð¼
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from core.brain import JarvisBrain
from hud.holographic_ui import HolographicHUD


def main():
    """ÐÐ»Ð°Ð²Ð½Ð°Ñ ÑÑÐ½ÐºÑÐ¸Ñ."""
    print("=" * 50)
    print("  JARVIS Ultimate v2.0.0")
    print("  Holographic HUD Interface")
    print("=" * 50)
    print()
    
    # Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Qt Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ
    app = QApplication(sys.argv)
    
    # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ JARVIS Brain
    brain = JarvisBrain()
    
    try:
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð²ÑÐµÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹
        brain.initialize()
        
        # Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹ÑÐ°
        hud = HolographicHUD(brain)
        brain.hud = hud
        
        # ÐÐ°Ð¿ÑÑÐº
        brain.start()
        
        print("\nJARVIS Ð³Ð¾ÑÐ¾Ð² Ðº ÑÐ°Ð±Ð¾ÑÐµ.")
        print("HUD Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ Ð°ÐºÑÐ¸Ð²ÐµÐ½.")
        print("ÐÑÐ°Ð²ÑÐ¹ ÐºÐ»Ð¸Ðº Ð½Ð° HUD - Ð·Ð°ÐºÑÑÑÑ Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ.")
        print()
        
        # ÐÐ°Ð¿ÑÑÐº Qt event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"ÐÑÐ¸ÑÐ¸ÑÐµÑÐºÐ°Ñ Ð¾ÑÐ¸Ð±ÐºÐ°: {e}")
        sys.exit(1)
    
    finally:
        brain.stop()
        print("\nÐÐ¾ ÑÐ²Ð¸Ð´Ð°Ð½Ð¸Ñ!")


if __name__ == "__main__":
    main()
