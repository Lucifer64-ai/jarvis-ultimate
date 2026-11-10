"""
Holographic HUD Interface - Виртуальное тело JARVIS
Голографический интерфейс поверх рабочего стола в стиле Iron Man
"""

import sys
import time
import math
from typing import Dict, Optional
from PyQt5.QtWidgets import QApplication, QWidget, QPainter, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QFont, QRadialGradient, QLinearGradient
import psutil


class HolographicHUD(QWidget):
    """Голографический HUD интерфейс JARVIS."""

    def __init__(self, brain=None):
        super().__init__()
        self.brain = brain
        
        # Настройки окна
        self.setWindowTitle("JARVIS HUD")
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # Без рамки
            Qt.WindowStaysOnTopHint |  # Поверх всех окон
            Qt.Tool  # Не показывать в панели задач
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # Прозрачный фон
        
        # Получаем размер экрана
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        
        # Цвета (стиль Iron Man)
        self.color_primary = QColor(0, 200, 255, 200)  # Циановый
        self.color_secondary = QColor(0, 150, 255, 150)  # Синий
        self.color_accent = QColor(255, 150, 0, 200)  # Оранжевый
        self.color_text = QColor(200, 230, 255, 255)  # Светло-голубой
        
        # Анимация
        self.animation_time = 0
        self.pulse_phase = 0
        
        # Системные данные
        self.cpu_usage = 0
        self.ram_usage = 0
        self.network_speed = 0
        
        # Таймер обновления
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Обновление каждую секунду
        
        # Таймер анимации
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(50)  # 20 FPS
        
        # Статус
        self.status = "READY"
        self.voice_active = False
        
        self.show()

    def update_data(self):
        """Обновление системных данных."""
        try:
            self.cpu_usage = psutil.cpu_percent(interval=0)
            self.ram_usage = psutil.virtual_memory().percent
            
            # Сетевая активность (упрощенно)
            net_io = psutil.net_io_counters()
            self.network_speed = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024  # MB
        except:
            pass

    def animate(self):
        """Анимация HUD элементов."""
        self.animation_time += 0.05
        self.pulse_phase = (self.pulse_phase + 1) % 360
        self.update()

    def paintEvent(self, event):
        """Отрисовка HUD."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        
        # Центральный круг (Arc Reactor)
        self.draw_arc_reactor(painter, center_x, center_y, 150)
        
        # Системные панели
        self.draw_system_panels(painter, width, height)
        
        # Голосовая волна
        if self.voice_active:
            self.draw_voice_wave(painter, center_x, center_y + 200)
        
        # Статус
        self.draw_status(painter, center_x, height - 100)

    def draw_arc_reactor(self, painter: QPainter, x: int, y: int, radius: int):
        """Отрисовка центрального элемента - Arc Reactor."""
        # Пульсация
        pulse = math.sin(self.animation_time * 2) * 0.2 + 0.8
        
        # Внешнее свечение
        gradient = QRadialGradient(x, y, radius * 1.5)
        gradient.setColorAt(0, QColor(0, 200, 255, int(100 * pulse)))
        gradient.setColorAt(0.5, QColor(0, 150, 255, int(50 * pulse)))
        gradient.setColorAt(1, QColor(0, 100, 255, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(x, y), radius * 1.5, radius * 1.5)
        
        # Основное кольцо
        pen = QPen(self.color_primary)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(x, y), radius, radius)
        
        # Внутреннее кольцо
        pen.setColor(self.color_secondary)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(x, y), radius * 0.7, radius * 0.7)
        
        # Вращающиеся элементы
        for i in range(8):
            angle = (self.animation_time * 50 + i * 45) % 360
            rad = math.radians(angle)
            px = x + math.cos(rad) * radius * 0.85
            py = y + math.sin(rad) * radius * 0.85
            
            painter.setBrush(QBrush(self.color_accent))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(px, py), 5, 5)
        
        # Центральный текст (CPU)
        painter.setPen(QPen(self.color_text))
        font = QFont("Arial", 24, QFont.Bold)
        painter.setFont(font)
        painter.drawText(
            QRectF(x - 50, y - 30, 100, 60),
            Qt.AlignCenter,
            f"{int(self.cpu_usage)}%"
        )

    def draw_system_panels(self, painter: QPainter, width: int, height: int):
        """Отрисовка системных панелей."""
        # Левая верхняя панель - Время
        self.draw_panel(
            painter,
            50, 50, 300, 150,
            "TIME",
            [time.strftime("%H:%M:%S"), time.strftime("%d.%m.%Y")]
        )
        
        # Правая верхняя панель - RAM
        self.draw_panel(
            painter,
            width - 350, 50, 300, 150,
            "MEMORY",
            [f"RAM: {self.ram_usage}%", f"CPU: {self.cpu_usage}%"]
        )
        
        # Левая нижняя панель - Сеть
        self.draw_panel(
            painter,
            50, height - 200, 300, 150,
            "NETWORK",
            [f"Speed: {self.network_speed:.1f} MB/s", "Status: ONLINE"]
        )
        
        # Правая нижняя панель - Статус
        self.draw_panel(
            painter,
            width - 350, height - 200, 300, 150,
            "SYSTEM",
            ["JARVIS v2.0", "All systems nominal"]
        )

    def draw_panel(self, painter: QPainter, x: int, y: int, w: int, h: int, title: str, data: list):
        """Отрисовка панели."""
        # Фон панели
        painter.setPen(QPen(self.color_primary, 2))
        painter.setBrush(QBrush(QColor(0, 20, 40, 100)))
        painter.drawRoundedRect(x, y, w, h, 10, 10)
        
        # Заголовок
        painter.setPen(QPen(self.color_accent))
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(x + 10, y + 25, title)
        
        # Данные
        painter.setPen(QPen(self.color_text))
        font = QFont("Arial", 14)
        painter.setFont(font)
        
        for i, text in enumerate(data):
            painter.drawText(x + 10, y + 50 + i * 30, text)

    def draw_voice_wave(self, painter: QPainter, x: int, y: int):
        """Отрисовка голосовой волны."""
        pen = QPen(self.color_primary)
        pen.setWidth(3)
        painter.setPen(pen)
        
        # Синусоидальная волна
        points = []
        for i in range(100):
            px = x - 200 + i * 4
            py = y + math.sin(self.animation_time * 5 + i * 0.2) * 30
            points.append(QPointF(px, py))
        
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

    def draw_status(self, painter: QPainter, x: int, y: int):
        """Отрисовка статуса."""
        painter.setPen(QPen(self.color_text))
        font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(font)
        painter.drawText(
            QRectF(x - 100, y, 200, 40),
            Qt.AlignCenter,
            self.status
        )

    def set_status(self, status: str):
        """Установка статуса."""
        self.status = status
        self.update()

    def set_voice_active(self, active: bool):
        """Активация/деактивация голосовой волны."""
        self.voice_active = active
        self.update()

    def mousePressEvent(self, event):
        """Закрытие по клику (для тестирования)."""
        if event.button() == Qt.RightButton:
            self.close()


# Тестовый запуск
if __name__ == "__main__":
    app = QApplication(sys.argv)
    hud = HolographicHUD()
    sys.exit(app.exec_())
