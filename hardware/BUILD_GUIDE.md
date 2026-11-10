# JARVIS Physical Body - Сборка аппаратной части

## 🤖 Что это?

Полноценное физическое тело JARVIS как у Тони Старка:
- Голографический дисплей
- Движущаяся "голова" на сервоприводах
- LED индикаторы состояния
- Датчики присутствия и окружающей среды

---

## 📋 Необходимые компоненты

### 1. Вычислительный блок
- **Raspberry Pi 4** (4GB или 8GB RAM) - мозг JARVIS
- **MicroSD карта** 64GB+ (для ОС)
- **Блок питания** 5V 3A (USB-C)

### 2. Дисплей
- **Голографический проектор** (опционально, дорого)
- ИЛИ **Прозрачный OLED дисплей** (средний бюджет)
- ИЛИ **Обычный монитор + полупрозрачное зеркало** (бюджетно)

### 3. Движение (сервоприводы)
- **2x Сервопривода** MG996R (для pan/tilt)
- **Кронштейн** для крепления сервоприводов
- **PCA9685** - плата управления сервоприводами (I2C)

### 4. LED индикаторы
- **RGB LED strip** (WS2812B) - 1 метр
- **Arduino Nano** (для управления LED)
- ИЛИ **GPIO Raspberry Pi** напрямую (если LED мало)

### 5. Датчики
- **PIR Motion Sensor** (HC-SR501) - обнаружение движения
- **Ultrasonic Sensor** (HC-SR04) - расстояние до человека
- **DHT22** - температура и влажность
- **Light Sensor** (BH1750) - освещенность

### 6. Звук
- **Микрофон** USB или I2S (ReSpeaker)
- **Динамики** 3.5mm или USB
- ИЛИ **ReSpeaker 4-Mic Array** (для направленного звука)

### 7. Камера (опционально)
- **Raspberry Pi Camera Module** - для распознавания лиц
- ИЛИ **USB веб-камера**

### 8. Корпус
- **3D печатанный корпус** (файлы в `/hardware/case/`)
- ИЛИ **акриловый корпус** ручной сборки

---

## 🔌 Подключение

### Raspberry Pi GPIO

```
Сервоприводы (PCA9685):
- VCC → 5V
- GND → GND
- SDA → GPIO 2 (SDA)
- SCL → GPIO 3 (SCL)

LED Strip (WS2812B):
- VCC → 5V (внешний блок питания!)
- GND → GND
- DIN → GPIO 18

Датчики:
- PIR Motion → GPIO 22
- Ultrasonic Trig → GPIO 23
- Ultrasonic Echo → GPIO 24
- DHT22 Data → GPIO 17
- Light Sensor (I2C) → SDA/SCL

Микрофон:
- USB микрофон → USB порт
- ИЛИ I2S микрофон → I2S пины
```

---

## 💻 Установка ПО

### 1. Установка Raspberry Pi OS

```bash
# Скачай Raspberry Pi Imager
# Установи Raspberry Pi OS (64-bit)
# Включи SSH и Wi-Fi
```

### 2. Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Python и pip
sudo apt install python3-pip python3-venv -y

# GPIO библиотеки
sudo apt install python3-rpi.gpio -y

# Клонирование репозитория
git clone https://github.com/Lucifer64-ai/jarvis-ultimate.git
cd jarvis-ultimate

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
pip install RPi.GPIO adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit
pip install adafruit-circuitpython-dht adafruit-circuitpython-bh1750
pip install adafruit-circuitpython-neopixel
```

### 3. Настройка конфигурации

Отредактируй `config.json`:

```json
{
  "hardware": {
    "enabled": true,
    "display_type": "projector",
    "display_resolution": "1920x1080",
    "servo_pan_pin": 17,
    "servo_tilt_pin": 27,
    "led_pins": [18, 23, 24],
    "motion_sensor_pin": 22,
    "ultrasonic_trig_pin": 23,
    "ultrasonic_echo_pin": 24,
    "dht_pin": 17
  }
}
```

### 4. Запуск JARVIS

```bash
python main.py
```

---

## 🎮 Использование

### Голосовые команды

**Активация:**
- "Джарвис, включись" - активация hardware
- "Джарвис, выключись" - деактивация

**Движение:**
- "Джарвис, посмотри налево"
- "Джарвис, посмотри направо"
- "Джарвис, смотри на меня"

**LED:**
- "Джарвис, радуга" - радужная анимация
- "Джарвис, дыхание" - плавная пульсация

**Датчики:**
- "Джарвис, температура" - показать температуру
- "Джарвис, кто-нибудь есть?" - проверка присутствия
- "Джарвис, статус среды" - все показания датчиков

---

## 🏗️ Сборка корпуса

### Вариант 1: 3D печать

Файлы для 3D печати находятся в `/hardware/case/`:
- `head.stl` - голова JARVIS
- `base.stl` - основание
- `mount.stl` - крепление для Raspberry Pi

**Материал:** PLA или PETG
**Цвет:** Серебристый или белый

### Вариант 2: Акриловый корпус

Используй лазерную резку акрила по чертежам из `/hardware/case/dxf/`.

---

## 🔧 Troubleshooting

### Сервоприводы не двигаются
- Проверь подключение PCA9685 (I2C)
- Убедись, что питание 5V подается на PCA9685
- Проверь адреса I2C: `sudo i2cdetect -y 1`

### LED не светятся
- Проверь подключение DIN к GPIO 18
- Убедись, что используется внешний блок питания для LED strip
- Проверь количество LED в коде

### Датчики не работают
- PIR: проверь подключение к GPIO 22
- Ultrasonic: проверь Trig (GPIO 23) и Echo (GPIO 24)
- DHT22: проверь подключение Data к GPIO 17

### Микрофон не слышит
- Проверь `arecord -l` - список микрофонов
- Настрой default microphone в `/etc/asound.conf`

---

## 💰 Бюджет

### Минимальный (бюджетный) - ~$150
- Raspberry Pi 4 (4GB) - $55
- Обычный монитор (б/у) - $30
- 2x сервопривода - $15
- LED strip - $10
- Датчики - $20
- Микрофон + динамики - $20

### Средний - ~$300
- Raspberry Pi 4 (8GB) - $75
- Прозрачный OLED дисплей - $100
- PCA9685 + сервоприводы - $30
- ReSpeaker 2-Mic - $25
- Все датчики - $30
- 3D печатанный корпус - $40

### Премиум (как у Тони Старка) - ~$1000+
- Голографический проектор - $500+
- Raspberry Pi Cluster - $200
- ReSpeaker 4-Mic Array - $100
- Премиум сервоприводы - $100
- Кастомный корпус - $100+

---

## 🚀 Следующие шаги

1. **Закажи компоненты** с AliExpress/Amazon
2. **Собери hardware** по схеме подключения
3. **Напечатай корпус** (опционально)
4. **Установи ПО** на Raspberry Pi
5. **Настрой конфигурацию**
6. **Запусти JARVIS** и наслаждайся!

---

## 📞 Поддержка

Если возникли вопросы:
- GitHub Issues: https://github.com/Lucifer64-ai/jarvis-ultimate/issues
- Документация: https://github.com/Lucifer64-ai/jarvis-ultimate/wiki

---

**Создано для тех, кто хочет настоящего JARVIS, а не просто программу на рабочем столе.**

*"Sometimes you gotta run before you can walk." - Tony Stark*
