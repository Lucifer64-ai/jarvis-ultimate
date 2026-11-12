"""
Holographic HUD Interface - Виртуальное тело JARVIS
Голографический интерфейс поверх рабочего стола в стиле Iron Man
"""

import sys
import time
import math
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Dict, Optional
from PyQt5.QtWidgets import QApplication, QWidget, QPainter, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QFont, QRadialGradient
import psutil


class HolographicHUD(QWidget):
    """Голографический HUD интерфейс JARVIS."""

    def __init__(self, brain=None):
        super().__init__()
        self.brain = brain
        self.setWindowTitle("JARVIS HUD")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

        self.color_primary = QColor(0, 200, 255, 200)
        self.color_secondary = QColor(0, 150, 255, 150)
        self.color_accent = QColor(255, 150, 0, 200)
        self.color_text = QColor(200, 230, 255, 255)
        self.animation_time = 0
        self.pulse_phase = 0
        self.cpu_usage = 0
        self.ram_usage = 0
        self.network_speed = 0
        self.status = "READY"
        self.voice_active = False

        # psutil counters run off the Qt GUI thread; only one poll can be active.
        self._metrics_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="jarvis-hud")
        self._metrics_future: Optional[Future] = None
        self._last_net = None
        self._last_net_time = None
        self._metrics_timer = QTimer(self)
        self._metrics_timer.timeout.connect(self.update_data)
        self._metrics_timer.start(1000)
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self.animate)
        self._animation_timer.start(66)  # ~15 FPS, достаточных для плавной анимации.
        self._metrics_future = self._metrics_executor.submit(self._read_metrics)
        self.show()

    def _read_metrics(self):
        """Снять метрики системы в worker-потоке."""
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        counters = psutil.net_io_counters()
        now = time.monotonic()
        total_bytes = counters.bytes_sent + counters.bytes_recv
        return cpu, ram, total_bytes, now

    def update_data(self):
        """Получить завершённый опрос и запустить следующий без блокировки UI."""
        future = self._metrics_future
        if future is not None and future.done():
            try:
                cpu, ram, total_bytes, now = future.result()
                self.cpu_usage = cpu
                self.ram_usage = ram
                if self._last_net is not None and self._last_net_time is not None and now > self._last_net_time:
                    self.network_speed = max(0, total_bytes - self._last_net) / (now - self._last_net_time) / (1024 * 1024)
                self._last_net, self._last_net_time = total_bytes, now
                self.update()
            except Exception as exc:
                if self.brain:
                    self.brain.logger.debug("Не удалось обновить HUD метрики: %s", exc)
            self._metrics_future = None
        if self._metrics_future is None:
            self._metrics_future = self._metrics_executor.submit(self._read_metrics)

    def animate(self):
        self.animation_time += 0.066
        self.pulse_phase = (self.pulse_phase + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width, height = self.width(), self.height()
        center_x, center_y = width // 2, height // 2
        self.draw_arc_reactor(painter, center_x, center_y, 150)
        self.draw_system_panels(painter, width, height)
        if self.voice_active:
            self.draw_voice_wave(painter, center_x, center_y + 200)
        self.draw_status(painter, center_x, height - 100)

    def draw_arc_reactor(self, painter: QPainter, x: int, y: int, radius: int):
        pulse = math.sin(self.animation_time * 2) * 0.2 + 0.8
        gradient = QRadialGradient(x, y, radius * 1.5)
        gradient.setColorAt(0, QColor(0, 200, 255, int(100 * pulse)))
        gradient.setColorAt(0.5, QColor(0, 150, 255, int(50 * pulse)))
        gradient.setColorAt(1, QColor(0, 100, 255, 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(x, y), radius * 1.5, radius * 1.5)
        pen = QPen(self.color_primary)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(x, y), radius, radius)
        pen.setColor(self.color_secondary)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(x, y), radius * 0.7, radius * 0.7)
        painter.setBrush(QBrush(self.color_accent))
        painter.setPen(Qt.NoPen)
        for i in range(8):
            angle = math.radians((self.animation_time * 50 + i * 45) % 360)
            px = x + math.cos(angle) * radius * 0.85
            py = y + math.sin(angle) * radius * 0.85
            painter.drawEllipse(QPointF(px, py), 5, 5)
        painter.setPen(QPen(self.color_text))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(QRectF(x - 50, y - 30, 100, 60), Qt.AlignCenter, f"{int(self.cpu_usage)}%")

    def draw_system_panels(self, painter: QPainter, width: int, height: int):
        self.draw_panel(painter, 50, 50, 300, 150, "TIME", [time.strftime("%H:%M:%S"), time.strftime("%d.%m.%Y")])
        self.draw_panel(painter, width - 350, 50, 300, 150, "MEMORY", [f"RAM: {self.ram_usage}%", f"CPU: {self.cpu_usage}%"])
        self.draw_panel(painter, 50, height - 200, 300, 150, "NETWORK", [f"Speed: {self.network_speed:.1f} MB/s", "Status: ONLINE"])
        self.draw_panel(painter, width - 350, height - 200, 300, 150, "SYSTEM", ["JARVIS v2.0", "All systems nominal"])

    def draw_panel(self, painter: QPainter, x: int, y: int, w: int, h: int, title: str, data: list):
        painter.setPen(QPen(self.color_primary, 2))
        painter.setBrush(QBrush(QColor(0, 20, 40, 100)))
        painter.drawRoundedRect(x, y, w, h, 10, 10)
        painter.setPen(QPen(self.color_accent))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(x + 10, y + 25, title)
        painter.setPen(QPen(self.color_text))
        painter.setFont(QFont("Arial", 14))
        for i, text in enumerate(data):
            painter.drawText(x + 10, y + 50 + i * 30, text)

    def draw_voice_wave(self, painter: QPainter, x: int, y: int):
        painter.setPen(QPen(self.color_primary, 3))
        previous = None
        for i in range(100):
            point = QPointF(x - 200 + i * 4, y + math.sin(self.animation_time * 5 + i * 0.2) * 30)
            if previous is not None:
                painter.drawLine(previous, point)
            previous = point

    def draw_status(self, painter: QPainter, x: int, y: int):
        painter.setPen(QPen(self.color_text))
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(QRectF(x - 100, y, 200, 40), Qt.AlignCenter, self.status)

    def set_status(self, status: str):
        if self.status != status:
            self.status = status
            self.update()

    def set_voice_active(self, active: bool):
        if self.voice_active != active:
            self.voice_active = active
            self.update()

    def closeEvent(self, event):
        self._metrics_timer.stop()
        self._animation_timer.stop()
        self._metrics_executor.shutdown(wait=False, cancel_futures=True)
        super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hud = HolographicHUD()
    sys.exit(app.exec_())
