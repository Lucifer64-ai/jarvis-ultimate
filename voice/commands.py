"""
Обработчик голосовых команд JARVIS
"""

from typing import Dict, Optional
import re


class CommandHandler:
    """Обработка голосовых команд."""

    def __init__(self, brain):
        self.brain = brain
        self.commands = self._register_commands()

    def _register_commands(self) -> Dict:
        """Регистрация команд."""
        return {
            # Системные команды
            r"выключи (компьютер|пк)": ("system", "shutdown"),
            r"перезагрузи (компьютер|пк)": ("system", "restart"),
            r"отмени выключение": ("system", "cancel_shutdown"),
            r"заблокируй (экран|компьютер)": ("system", "lock_screen"),
            r"спящий режим": ("system", "sleep"),
            
            # Информация
            r"который час|время|сколько времени": ("info", "time"),
            r"какая (дата|сегодня)": ("info", "date"),
            r"какая погода": ("info", "weather"),
            r"статус системы": ("info", "system_status"),
            r"загрузка процессора": ("info", "cpu_usage"),
            r"состояние батареи": ("info", "battery"),
            
            # Приложения
            r"открой (блокнот|notepad)": ("app", "open_notepad"),
            r"открой калькулятор": ("app", "open_calculator"),
            r"открой youtube": ("app", "open_youtube"),
            r"открой github": ("app", "open_github"),
            
            # Управление
            r"громкость (\d+)": ("control", "set_volume"),
            r"без звука|mute": ("control", "mute"),
            r"яркость (\d+)": ("control", "set_brightness"),
            r"сверни все окна": ("control", "minimize_all"),
            r"покажи рабочий стол": ("control", "show_desktop"),
            
            # Сеть
            r"тест скорости|скорость интернета": ("network", "speed_test"),
            r"какой (ip|айпи) адрес": ("network", "get_ip"),
        }

    def parse_command(self, text: str) -> Optional[Dict]:
        """Разбор команды."""
        text_lower = text.lower().strip()
        
        for pattern, (category, action) in self.commands.items():
            match = re.match(pattern, text_lower)
            if match:
                result = {
                    "category": category,
                    "action": action,
                    "original": text
                }
                
                # Извлечение параметров
                if match.groups():
                    result["params"] = match.groups()
                
                return result
        
        return None

    def execute(self, text: str) -> Dict:
        """Выполнение команды."""
        command = self.parse_command(text)
        
        if not command:
            return {"status": "error", "message": "Команда не распознана"}
        
        category = command["category"]
        action = command["action"]
        
        try:
            # Маршрутизация к соответствующему модулю
            if category == "system":
                module = self.brain.modules.get("system")
                if module and hasattr(module, action):
                    return getattr(module, action)()
            
            elif category == "info":
                return self._handle_info(action)
            
            elif category == "app":
                return self._handle_app(action)
            
            elif category == "control":
                return self._handle_control(action, command.get("params"))
            
            elif category == "network":
                module = self.brain.modules.get("network")
                if module and hasattr(module, action):
                    return getattr(module, action)()
            
            return {"status": "error", "message": "Действие не реализовано"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _handle_info(self, action: str) -> Dict:
        """Обработка информационных команд."""
        from datetime import datetime
        
        if action == "time":
            now = datetime.now()
            return {"status": "ok", "message": f"Сейчас {now.strftime('%H:%M')}"}
        
        elif action == "date":
            now = datetime.now()
            return {"status": "ok", "message": f"Сегодня {now.strftime('%d %B %Y')}"}
        
        elif action == "system_status":
            hardware = self.brain.modules.get("hardware")
            if hardware:
                report = hardware.get_full_report()
                return {"status": "ok", "data": report}
        
        elif action == "cpu_usage":
            hardware = self.brain.modules.get("hardware")
            if hardware:
                cpu_info = hardware.get_cpu_info()
                return {"status": "ok", "message": f"Загрузка процессора {cpu_info['usage']}%"}
        
        elif action == "battery":
            power = self.brain.modules.get("power")
            if power:
                battery = power.get_battery_info()
                if battery.get("available"):
                    return {"status": "ok", "message": f"Заряд батареи {battery['percent']}%"}
                else:
                    return {"status": "ok", "message": "Батарея не обнаружена"}
        
        return {"status": "error", "message": "Информация недоступна"}

    def _handle_app(self, action: str) -> Dict:
        """Обработка команд открытия приложений."""
        import subprocess
        
        apps = {
            "open_notepad": "notepad",
            "open_calculator": "calc",
            "open_youtube": "https://youtube.com",
            "open_github": "https://github.com"
        }
        
        if action in apps:
            target = apps[action]
            try:
                if target.startswith("http"):
                    subprocess.Popen(["start", target], shell=True)
                else:
                    subprocess.Popen([target])
                return {"status": "ok", "message": f"Открываю {action.replace('open_', '')}"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        return {"status": "error", "message": "Приложение не найдено"}

    def _handle_control(self, action: str, params: tuple = None) -> Dict:
        """Обработка команд управления."""
        import pyautogui
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
        
        if action == "set_volume" and params:
            try:
                volume_level = int(params[0]) / 100
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                volume.SetMasterVolumeLevelScalar(volume_level, None)
                return {"status": "ok", "message": f"Громкость установлена на {params[0]}%"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        elif action == "mute":
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                current = volume.GetMute()
                volume.SetMute(not current, None)
                return {"status": "ok", "message": "Звук переключен"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        elif action == "minimize_all":
            windows = self.brain.modules.get("windows")
            if windows:
                return windows.minimize_all()
        
        elif action == "show_desktop":
            windows = self.brain.modules.get("windows")
            if windows:
                return windows.show_desktop()
        
        return {"status": "error", "message": "Команда не реализована"}
