# 🤖 JARVIS Ultimate

**Продвинутый AI-ассистент с полным управлением ПК, голосовым интерфейсом, HUD-интерфейсом, ML-распознаванием, ChatGPT интеграцией, Home Assistant и мобильным приложением.**

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)

---

## 📋 Описание

JARVIS Ultimate — это полнофункциональный AI-ассистент, вдохновленный JARVIS из Iron Man. Система объединяет:

- 🎤 **Голосовое управление** — распознавание команд на русском языке
- 🖥️ **Полное управление ПК** — системные операции, процессы, файлы, реестр
- 🎨 **HUD-интерфейс** — голографический оверлей в стиле Iron Man
- 🧠 **AI и ML** — ChatGPT интеграция, ML-классификация команд
- 🏠 **Умный дом** — интеграция с Home Assistant
- 📱 **Мобильное приложение** — управление через смартфон
- ⚡ **Автоматизация** — планировщик задач, макросы, триггеры
- 🔌 **Плагины** — расширяемая архитектура

---

## 🚀 Возможности

### Системные операции
- Выключение, перезагрузка, блокировка экрана
- Управление процессами (просмотр, завершение)
- Работа с файлами (создание, копирование, удаление в корзину)
- Управление окнами (свернуть все, закрыть по заголовку)
- Мониторинг оборудования (CPU, RAM, диски, батарея)
- Сетевые операции (IP, тест скорости)

### Голосовой интерфейс
- Распознавание речи на русском языке
- Wake word "Джарвис"
- Синтез речи с выбором голоса
- Обработка голосовых команд

### AI модули
- **ChatGPT интеграция** — умные ответы, анализ интентов, генерация кода
- **ML-движок** — классификация команд через SVM
- **Контекст** — управление историей разговора
- **Улучшение речи** — коррекция ошибок распознавания

### Умный дом (Home Assistant)
- Управление освещением (вкл/выкл, яркость, цвет)
- Управление климатом (температура, режимы)
- Управление медиа (воспроизведение, громкость)
- Управление замками
- Сцены и автоматизации
- Мониторинг датчиков (температура, влажность, движение)

### Мобильное приложение
- **React Native** (Expo) для iOS и Android
- Авторизация через API
- Управление устройствами умного дома
- Отправка голосовых команд
- Просмотр статуса системы
- Real-time обновления через WebSocket

### Автоматизация
- **Планировщик задач** — выполнение команд по расписанию
- **Макросы** — последовательности команд
- **Триггеры** — автоматические действия по условиям

---

## 📦 Установка

### Требования
- Windows 10/11 (64-bit)
- Python 3.11+
- Микрофон (для голосового управления)
- Home Assistant (опционально, для умного дома)
- OpenAI API ключ (опционально, для ChatGPT)

### Быстрая установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Lucifer64-ai/jarvis-ultimate.git
cd jarvis-ultimate
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте конфигурацию:**
```bash
copy .env.example .env
# Отредактируйте .env файл
```

5. **Запустите JARVIS:**
```bash
python main.py
```

### Сборка EXE

**Windows (BAT):**
```bash
cd build
build.bat
```

**Windows (PowerShell):**
```powershell
cd build
.\build.ps1
```

Результат: `dist/JARVIS/JARVIS.exe`

### Создание установщика

1. Установите [Inno Setup](https://jrsoftware.org/isdl.php)
2. Запустите:
```bash
iscc installer\jarvis_installer.iss
```

Результат: `installer/output/JARVIS_Ultimate_Setup.exe`

---

## ⚙️ Конфигурация

### .env файл

```env
# OpenAI API (опционально)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7

# Home Assistant (опционально)
HOME_ASSISTANT_URL=http://192.168.1.100:8123
HOME_ASSISTANT_TOKEN=your-token-here

# Mobile API Server
MOBILE_API_HOST=0.0.0.0
MOBILE_API_PORT=8080
MOBILE_API_SECRET=your-secret-key

# WebSocket Server
WEBSOCKET_PORT=8765

# Logging
LOG_LEVEL=INFO
LOG_FILE=jarvis.log
```

### config.json

```json
{
  "name": "JARVIS",
  "version": "2.0.0",
  "language": "ru",
  "voice": {
    "rate": 180,
    "wake_word": "джарвис",
    "volume": 1.0
  },
  "hud": {
    "enabled": true,
    "position": "top-right"
  },
  "startup": {
    "greeting": true,
    "sound": true
  }
}
```

---

## 🎮 Использование

### Голосовые команды

**Системные:**
- "Джарвис, выключи компьютер"
- "Джарвис, перезагрузи ПК"
- "Джарвис, заблокируй экран"
- "Джарвис, спящий режим"

**Информация:**
- "Джарвис, который час?"
- "Джарвис, какая погода?"
- "Джарвис, статус системы"
- "Джарвис, состояние батареи"

**Приложения:**
- "Джарвис, открой блокнот"
- "Джарвис, открой YouTube"
- "Джарвис, открой GitHub"

**Управление:**
- "Джарвис, громкость 50"
- "Джарвис, без звука"
- "Джарвис, сверни все окна"

**Сеть:**
- "Джарвис, тест скорости"
- "Джарвис, какой IP адрес?"

**Умный дом:**
- "Джарвис, включи свет"
- "Джарвис, выключи свет"
- "Джарвис, установи температуру 22 градуса"

### Мобильное приложение

1. Установите приложение на смартфон:
```bash
cd mobile-app
npm install
expo start
```

2. Отсканируйте QR-код в Expo Go

3. Войдите с учетными данными JARVIS

4. Управляйте системой удаленно!

---

## 🏗️ Архитектура

```
jarvis-ultimate/
├── core/                    # Ядро системы
│   ├── config.py           # Конфигурация
│   ├── brain.py            # Главный контроллер
│   ├── event_bus.py        # Шина событий
│   └── plugin_manager.py   # Менеджер плагинов
│
├── modules/                 # Системные модули
│   ├── system.py           # Системные операции
│   ├── processes.py        # Управление процессами
│   ├── files.py            # Работа с файлами
│   ├── windows.py          # Управление окнами
│   ├── network.py          # Сетевые операции
│   ├── registry.py         # Реестр Windows
│   ├── power.py            # Питание
│   └── hardware.py         # Оборудование
│
├── voice/                   # Голосовой интерфейс
│   ├── listener.py         # Распознавание речи
│   ├── speaker.py          # Синтез речи
│   └── commands.py         # Обработчик команд
│
├── ui/                      # Интерфейс
│   ├── hud.py              # HUD-оверлей
│   ├── tray.py             # Трей-иконка
│   └── notifications.py    # Уведомления
│
├── ai/                      # AI модули
│   ├── ml_engine.py        # ML-классификация
│   ├── chatgpt.py          # ChatGPT интеграция
│   ├── context_manager.py  # Управление контекстом
│   └── voice_enhancer.py   # Улучшение речи
│
├── smart_home/              # Умный дом
│   ├── home_assistant.py   # Home Assistant API
│   ├── devices.py          # Управление устройствами
│   ├── scenes.py           # Сцены
│   └── sensors.py          # Датчики
│
├── mobile/                  # Мобильное API
│   ├── server.py           # HTTP сервер
│   ├── websocket.py        # WebSocket
│   └── auth.py             # Аутентификация
│
├── mobile-app/              # React Native приложение
│   ├── App.js              # Главный компонент
│   ├── src/screens/        # Экраны
│   └── src/services/       # Сервисы
│
├── automation/              # Автоматизация
│   ├── scheduler.py        # Планировщик
│   ├── macros.py           # Макросы
│   └── triggers.py         # Триггеры
│
├── build/                   # Сборка
│   ├── jarvis.spec         # PyInstaller конфиг
│   ├── build.bat           # Скрипт сборки
│   └── build.ps1           # PowerShell скрипт
│
├── installer/               # Установщик
│   └── jarvis_installer.iss # Inno Setup скрипт
│
├── .github/workflows/       # CI/CD
│   └── build-exe.yml       # GitHub Actions
│
├── main.py                  # Точка входа
├── config.json              # Конфигурация
├── .env.example             # Пример .env
├── requirements.txt         # Зависимости
└── README.md                # Документация
```

---

## 🔧 Разработка

### Добавление нового модуля

1. Создайте файл в `modules/`:
```python
class MyModule:
    def __init__(self, brain):
        self.brain = brain
    
    def my_action(self):
        return {"status": "ok", "message": "Done!"}
```

2. Зарегистрируйте в `core/brain.py`:
```python
self.modules["my_module"] = MyModule(self)
```

3. Добавьте команду в `voice/commands.py`:
```python
r"моя команда": ("my_module", "my_action"),
```

### Создание плагина

1. Создайте папку `plugins/my_plugin/`
2. Добавьте `plugin.py`:
```python
def setup(brain):
    class MyPlugin:
        def __init__(self):
            self.brain = brain
        
        def shutdown(self):
            pass
    
    return MyPlugin()
```

3. Плагин автоматически загрузится при запуске

---

## 🚀 CI/CD

### GitHub Actions

Автоматическая сборка EXE при push в main:

```yaml
name: Build JARVIS EXE

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
```

**Артефакты:**
- `JARVIS-EXE` — готовый EXE файл
- `JARVIS_Ultimate_Setup.exe` — установщик (при создании тега)

### Создание релиза

```bash
git tag v2.0.0
git push origin v2.0.0
```

GitHub Actions автоматически:
1. Соберет EXE
2. Создаст установщик
3. Опубликует релиз

---

## 🐛 Troubleshooting

### Ошибка: "Python не установлен"
Установите Python 3.11+ с [python.org](https://python.org)

### Ошибка: "Микрофон не найден"
Проверьте подключение микрофона и разрешения в Windows

### Ошибка: "OpenAI API не настроен"
Добавьте `OPENAI_API_KEY` в `.env` файл (опционально)

### Ошибка: "Home Assistant не подключен"
Проверьте `HOME_ASSISTANT_URL` и `HOME_ASSISTANT_TOKEN` в `.env`

### HUD не отображается
Проверьте `hud.enabled` в `config.json`

---

## 📝 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

---

## 🤝 Вклад

Pull requests приветствуются! Для крупных изменений сначала откройте issue для обсуждения.

---

## 📞 Поддержка

- **Issues:** [GitHub Issues](https://github.com/Lucifer64-ai/jarvis-ultimate/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Lucifer64-ai/jarvis-ultimate/discussions)

---

## 🙏 Благодарности

- [OpenAI](https://openai.com/) — ChatGPT API
- [Home Assistant](https://www.home-assistant.io/) — Умный дом
- [PyInstaller](https://pyinstaller.org/) — Сборка EXE
- [Inno Setup](https://jrsoftware.org/isdl.php) — Установщик

---

## 📊 Статистика

![GitHub stars](https://img.shields.io/github/stars/Lucifer64-ai/jarvis-ultimate?style=social)
![GitHub forks](https://img.shields.io/github/forks/Lucifer64-ai/jarvis-ultimate?style=social)
![GitHub issues](https://img.shields.io/github/issues/Lucifer64-ai/jarvis-ultimate)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Lucifer64-ai/jarvis-ultimate)

---

**Создано с ❤️ для энтузиастов AI и автоматизации**

*"I am JARVIS, your personal AI assistant."*
