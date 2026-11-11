"""
JARVIS Ultimate - Ð¢Ð¾ÑÐºÐ° Ð²ÑÐ¾Ð´Ð°
"""

import sys
import time


from core.brain import JarvisBrain


def main():
    """ÐÐ»Ð°Ð²Ð½Ð°Ñ ÑÑÐ½ÐºÑÐ¸Ñ."""
    print("=" * 50)
    print("  JARVIS Ultimate v2.0.0")
    print("  AI Assistant with Learning Capabilities")
    print("=" * 50)
    print()

    # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ
    brain = JarvisBrain()

    try:
        # ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð²ÑÐµÑ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹
        brain.initialize()

        # ÐÐ°Ð¿ÑÑÐº
        brain.start()

        # ÐÐ»Ð°Ð²Ð½ÑÐ¹ ÑÐ¸ÐºÐ»
        print("\nJARVIS Ð³Ð¾ÑÐ¾Ð² Ðº ÑÐ°Ð±Ð¾ÑÐµ. ÐÐ²ÐµÐ´Ð¸ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð¸Ð»Ð¸ 'Ð²ÑÑÐ¾Ð´' Ð´Ð»Ñ Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð¸Ñ.\n")

        while brain.running:
            try:
                # ÐÐ²Ð¾Ð´ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
                command = input("ÐÑ: ").strip()

                if not command:
                    continue

                # ÐÑÑÐ¾Ð´
                if command.lower() in ["Ð²ÑÑÐ¾Ð´", "exit", "quit", "ÑÑÐ¾Ð¿"]:
                    print("ÐÐ°Ð²ÐµÑÑÐµÐ½Ð¸Ðµ ÑÐ°Ð±Ð¾ÑÑ...")
                    break

                # ÐÐ±ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
                result = brain.process_command(command)

                # ÐÑÐ²Ð¾Ð´ ÑÐµÐ·ÑÐ»ÑÑÐ°ÑÐ°
                if result.get("status") == "ok":
                    if "message" in result:
                        print(f"JARVIS: {result['message']}")
                    elif "response" in result:
                        print(f"JARVIS: {result['response']}")
                    else:
                        print(f"JARVIS: ÐÐ¾Ð¼Ð°Ð½Ð´Ð° Ð²ÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð°")
                else:
                    print(f"JARVIS: ÐÑÐ¸Ð±ÐºÐ° - {result.get('message', 'ÐÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð°Ñ Ð¾ÑÐ¸Ð±ÐºÐ°')}")

                # ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾Ð± Ð¾Ð±ÑÑÐµÐ½Ð¸Ð¸
                if "learning_info" in result:
                    learning = result["learning_info"]
                    if learning.get("learning_suggestion"):
                        print(f"\nð¡ {learning['learning_suggestion']}\n")

                print()

            except KeyboardInterrupt:
                print("\n\nÐÑÐµÑÐ²Ð°Ð½Ð¾ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¼")
                break
            except Exception as e:
                print(f"ÐÑÐ¸Ð±ÐºÐ°: {e}")

    except Exception as e:
        print(f"ÐÑÐ¸ÑÐ¸ÑÐµÑÐºÐ°Ñ Ð¾ÑÐ¸Ð±ÐºÐ°: {e}")
        sys.exit(1)

    finally:
        # ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ°
        brain.stop()
        print("\nÐÐ¾ ÑÐ²Ð¸Ð´Ð°Ð½Ð¸Ñ!")


if __name__ == "__main__":
    main()
