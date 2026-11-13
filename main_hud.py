"""
JARVIS Ultimate - ÃÂ¢ÃÂ¾ÃÃÂºÃÂ° ÃÂ²ÃÃÂ¾ÃÂ´ÃÂ° Ã HUD ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹ÃÃÂ¾ÃÂ¼
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from core.brain import JarvisBrain
from hud.holographic_ui import HolographicHUD


def main():
    """ÃÃÂ»ÃÂ°ÃÂ²ÃÂ½ÃÂ°Ã ÃÃÃÂ½ÃÂºÃÃÂ¸Ã."""
    print("=" * 50)
    print("  JARVIS Ultimate v2.0.0")
    print("  Holographic HUD Interface")
    print("=" * 50)
    print()
    
    # ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ Qt ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã
    app = QApplication(sys.argv)
    
    # ÃÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã JARVIS Brain
    brain = JarvisBrain()
    
    try:
        # ÃÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã ÃÂ²ÃÃÂµÃ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂµÃÂ¹
        brain.initialize()
        
        # ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ HUD ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹ÃÃÂ°
        hud = HolographicHUD(brain)
        brain.hud = hud
        
        # ÃÃÂ°ÃÂ¿ÃÃÃÂº
        brain.start()
        
        print("\nJARVIS ÃÂ³ÃÂ¾ÃÃÂ¾ÃÂ² ÃÂº ÃÃÂ°ÃÂ±ÃÂ¾ÃÃÂµ.")
        print("HUD ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹Ã ÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂµÃÂ½.")
        print("ÃÃÃÂ°ÃÂ²ÃÃÂ¹ ÃÂºÃÂ»ÃÂ¸ÃÂº ÃÂ½ÃÂ° HUD - ÃÂ·ÃÂ°ÃÂºÃÃÃÃ ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹Ã.")
        print()
        
        # ÃÃÂ°ÃÂ¿ÃÃÃÂº Qt event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"ÃÃÃÂ¸ÃÃÂ¸ÃÃÂµÃÃÂºÃÂ°Ã ÃÂ¾ÃÃÂ¸ÃÂ±ÃÂºÃÂ°: {e}")
        sys.exit(1)
    
    finally:
        brain.stop()
        print("\nÃÃÂ¾ ÃÃÂ²ÃÂ¸ÃÂ´ÃÂ°ÃÂ½ÃÂ¸Ã!")


if __name__ == "__main__":
    main()
