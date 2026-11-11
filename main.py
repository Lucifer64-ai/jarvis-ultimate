"""
JARVIS Ultimate - ÃÂ¢ÃÂ¾ÃÂÃÂºÃÂ° ÃÂ²ÃÂÃÂ¾ÃÂ´ÃÂ°
"""

import sys
import time

# Явный импорт для PyInstaller
import dotenv
from dotenv import load_dotenv

from core.brain import JarvisBrain


def main():
    """ÃÂÃÂ»ÃÂ°ÃÂ²ÃÂ½ÃÂ°ÃÂ ÃÂÃÂÃÂ½ÃÂºÃÂÃÂ¸ÃÂ."""
    print("=" * 50)
    print("  JARVIS Ultimate v2.0.0")
    print("  AI Assistant with Learning Capabilities")
    print("=" * 50)
    print()

    # ÃÂÃÂ½ÃÂ¸ÃÂÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÂÃÂ¸ÃÂ
    brain = JarvisBrain()

    try:
        # ÃÂÃÂ½ÃÂ¸ÃÂÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÂÃÂ¸ÃÂ ÃÂ²ÃÂÃÂµÃÂ ÃÂ¼ÃÂ¾ÃÂ´ÃÂÃÂ»ÃÂµÃÂ¹
        brain.initialize()

        # ÃÂÃÂ°ÃÂ¿ÃÂÃÂÃÂº
        brain.start()

        # ÃÂÃÂ»ÃÂ°ÃÂ²ÃÂ½ÃÂÃÂ¹ ÃÂÃÂ¸ÃÂºÃÂ»
        print("\nJARVIS ÃÂ³ÃÂ¾ÃÂÃÂ¾ÃÂ² ÃÂº ÃÂÃÂ°ÃÂ±ÃÂ¾ÃÂÃÂµ. ÃÂÃÂ²ÃÂµÃÂ´ÃÂ¸ÃÂÃÂµ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ ÃÂ¸ÃÂ»ÃÂ¸ 'ÃÂ²ÃÂÃÂÃÂ¾ÃÂ´' ÃÂ´ÃÂ»ÃÂ ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÂÃÂÃÂµÃÂ½ÃÂ¸ÃÂ.\n")

        while brain.running:
            try:
                # ÃÂÃÂ²ÃÂ¾ÃÂ´ ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ
                command = input("ÃÂÃÂ: ").strip()

                if not command:
                    continue

                # ÃÂÃÂÃÂÃÂ¾ÃÂ´
                if command.lower() in ["ÃÂ²ÃÂÃÂÃÂ¾ÃÂ´", "exit", "quit", "ÃÂÃÂÃÂ¾ÃÂ¿"]:
                    print("ÃÂÃÂ°ÃÂ²ÃÂµÃÂÃÂÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂÃÂ°ÃÂ±ÃÂ¾ÃÂÃÂ...")
                    break

                # ÃÂÃÂ±ÃÂÃÂ°ÃÂ±ÃÂ¾ÃÂÃÂºÃÂ° ÃÂºÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ
                result = brain.process_command(command)

                # ÃÂÃÂÃÂ²ÃÂ¾ÃÂ´ ÃÂÃÂµÃÂ·ÃÂÃÂ»ÃÂÃÂÃÂ°ÃÂÃÂ°
                if result.get("status") == "ok":
                    if "message" in result:
                        print(f"JARVIS: {result['message']}")
                    elif "response" in result:
                        print(f"JARVIS: {result['response']}")
                    else:
                        print(f"JARVIS: ÃÂÃÂ¾ÃÂ¼ÃÂ°ÃÂ½ÃÂ´ÃÂ° ÃÂ²ÃÂÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂµÃÂ½ÃÂ°")
                else:
                    print(f"JARVIS: ÃÂÃÂÃÂ¸ÃÂ±ÃÂºÃÂ° - {result.get('message', 'ÃÂÃÂµÃÂ¸ÃÂ·ÃÂ²ÃÂµÃÂÃÂÃÂ½ÃÂ°ÃÂ ÃÂ¾ÃÂÃÂ¸ÃÂ±ÃÂºÃÂ°')}")

                # ÃÂÃÂ½ÃÂÃÂ¾ÃÂÃÂ¼ÃÂ°ÃÂÃÂ¸ÃÂ ÃÂ¾ÃÂ± ÃÂ¾ÃÂ±ÃÂÃÂÃÂµÃÂ½ÃÂ¸ÃÂ¸
                if "learning_info" in result:
                    learning = result["learning_info"]
                    if learning.get("learning_suggestion"):
                        print(f"\nÃ°ÂÂÂ¡ {learning['learning_suggestion']}\n")

                print()

            except KeyboardInterrupt:
                print("\n\nÃÂÃÂÃÂµÃÂÃÂ²ÃÂ°ÃÂ½ÃÂ¾ ÃÂ¿ÃÂ¾ÃÂ»ÃÂÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÂÃÂµÃÂ»ÃÂµÃÂ¼")
                break
            except Exception as e:
                print(f"ÃÂÃÂÃÂ¸ÃÂ±ÃÂºÃÂ°: {e}")

    except Exception as e:
        print(f"ÃÂÃÂÃÂ¸ÃÂÃÂ¸ÃÂÃÂµÃÂÃÂºÃÂ°ÃÂ ÃÂ¾ÃÂÃÂ¸ÃÂ±ÃÂºÃÂ°: {e}")
        sys.exit(1)

    finally:
        # ÃÂÃÂÃÂÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ°
        brain.stop()
        print("\nÃÂÃÂ¾ ÃÂÃÂ²ÃÂ¸ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂ!")


if __name__ == "__main__":
    main()
