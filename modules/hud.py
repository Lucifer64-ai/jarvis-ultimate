"""
JARVIS HUD - ÐÐ¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¸Ð¹ Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ Ð² ÑÑÐ¸Ð»Ðµ Ð¢Ð¾Ð½Ð¸ Ð¡ÑÐ°ÑÐºÐ°
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush, QRadialGradient
import psutil
import threading


class ArcReactorWidget(QWidget):
    """Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½ÑÐ¹ Ð²Ð¸Ð´Ð¶ÐµÑ - Arc Reactor Ñ Ð³Ð¾Ð»Ð¾ÑÐ¾Ð²Ð¾Ð¹ Ð²Ð¾Ð»Ð½Ð¾Ð¹."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.pulse_phase = 0
        self.voice_level = 0.0
        
        # Ð¢Ð°Ð¹Ð¼ÐµÑ Ð°Ð½Ð¸Ð¼Ð°ÑÐ¸Ð¸
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
    
    def _animate(self):
        """ÐÐ½Ð¸Ð¼Ð°ÑÐ¸Ñ Ð¿ÑÐ»ÑÑÐ°ÑÐ¸Ð¸."""
        self.pulse_phase += 0.1
        if self.pulse_phase > 6.28:
            self.pulse_phase = 0
        self.update()
    
    def set_voice_level(self, level: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÑÐ¾Ð²ÐµÐ½Ñ Ð³Ð¾Ð»Ð¾ÑÐ°."""
        self.voice_level = max(0.0, min(1.0, level))
        self.update()
    
    def paintEvent(self, event):
        """ÐÑÑÐ¸ÑÐ¾Ð²ÐºÐ° Arc Reactor."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 80
        
        # ÐÑÐ»ÑÑÐ°ÑÐ¸Ñ
        pulse = (self.pulse_phase.sin() + 1) / 2 if hasattr(self.pulse_phase, 'sin') else 0.5
        pulse_radius = radius + pulse * 10
        
        # ÐÐ½ÐµÑÐ½ÐµÐµ ÑÐ²ÐµÑÐµÐ½Ð¸Ðµ
        gradient = QRadialGradient(center_x, center_y, pulse_radius)
        gradient.setColorAt(0, QColor(0, 200, 255, 100))
        gradient.setColorAt(0.5, QColor(0, 150, 255, 50))
        gradient.setColorAt(1, QColor(0, 100, 255, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - pulse_radius, center_y - pulse_radius, 
                          pulse_radius * 2, pulse_radius * 2)
        
        # ÐÐ½ÑÑÑÐµÐ½Ð½Ð¸Ð¹ ÐºÑÑÐ³
        painter.setPen(QPen(QColor(0, 200, 255, 200), 3))
        painter.setBrush(QBrush(QColor(0, 50, 100, 100)))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # ÐÐ¾Ð»Ð¾ÑÐ¾Ð²Ð°Ñ Ð²Ð¾Ð»Ð½Ð°
        if self.voice_level > 0:
            wave_height = self.voice_level * 30
            painter.setPen(QPen(QColor(0, 255, 255, 200), 2))
            
            for i in range(5):
                offset = i * 10 - 20
                amplitude = wave_height * (1 - abs(offset) / 30)
                painter.drawLine(center_x + offset - 5, center_y - amplitude,
                               center_x + offset + 5, center_y + amplitude)


class SystemPanel(QWidget):
    """ÐÐ°Ð½ÐµÐ»Ñ Ñ ÑÐ¸ÑÑÐµÐ¼Ð½Ð¾Ð¹ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸ÐµÐ¹."""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 20, 40, 150);
                border: 2px solid rgba(0, 200, 255, 100);
                border-radius: 10px;
            }
        """)
        
        # Ð¢ÐµÐ½Ñ
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 200, 255, 100))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # ÐÐ°Ð³Ð¾Ð»Ð¾Ð²Ð¾Ðº
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            color: rgb(0, 200, 255);
            font-size: 14px;
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        layout.addWidget(self.title_label)
        
        # ÐÐ¾Ð½ÑÐµÐ½Ñ
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
    
    def add_stat(self, label: str, value: str = ""):
        """ÐÐ¾Ð±Ð°Ð²Ð¸ÑÑ ÑÑÐ°ÑÐ¸ÑÑÐ¸ÐºÑ."""
        row = QHBoxLayout()
        
        name_label = QLabel(label)
        name_label.setStyleSheet("""
            color: rgb(150, 200, 255);
            font-size: 12px;
            background: transparent;
            border: none;
        """)
        row.addWidget(name_label)
        
        row.addStretch()
        
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            color: rgb(0, 255, 255);
            font-size: 12px;
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        row.addWidget(value_label)
        
        self.content_layout.addLayout(row)
        return value_label


class JarvisHUD(QMainWindow):
    """ÐÐ»Ð°Ð²Ð½Ð¾Ðµ Ð¾ÐºÐ½Ð¾ JARVIS HUD."""
    
    voice_level_signal = pyqtSignal(float)
    
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.logger = brain.logger
        
        # ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð¾ÐºÐ½Ð°
        self.setWindowTitle("JARVIS HUD")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Ð Ð°Ð·Ð¼ÐµÑ Ð¸ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ñ
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½ÑÐ¹ Ð²Ð¸Ð´Ð¶ÐµÑ
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # ÐÐµÑÑÐ½ÑÑ Ð¿Ð°Ð½ÐµÐ»Ñ
        top_layout = QHBoxLayout()
        
        # ÐÐµÐ²Ð°Ñ Ð²ÐµÑÑÐ½ÑÑ - ÐÑÐµÐ¼Ñ Ð¸ Ð´Ð°ÑÐ°
        self.time_panel = SystemPanel("ÐÐ ÐÐÐ¯")
        self.time_label = self.time_panel.add_stat("ÐÑÐµÐ¼Ñ", "--:--")
        self.date_label = self.time_panel.add_stat("ÐÐ°ÑÐ°", "--.--.----")
        top_layout.addWidget(self.time_panel)
        
        top_layout.addStretch()
        
        # ÐÑÐ°Ð²Ð°Ñ Ð²ÐµÑÑÐ½ÑÑ - Ð¡Ð¸ÑÑÐµÐ¼Ð°
        self.system_panel = SystemPanel("Ð¡ÐÐ¡Ð¢ÐÐÐ")
        self.cpu_label = self.system_panel.add_stat("CPU", "0%")
        self.ram_label = self.system_panel.add_stat("RAM", "0%")
        self.disk_label = self.system_panel.add_stat("ÐÐ¸ÑÐº", "0%")
        top_layout.addWidget(self.system_panel)
        
        main_layout.addLayout(top_layout)
        
        # Ð¦ÐµÐ½ÑÑ - Arc Reactor
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        
        self.arc_reactor = ArcReactorWidget()
        center_layout.addWidget(self.arc_reactor)
        
        center_layout.addStretch()
        main_layout.addLayout(center_layout)
        
        # ÐÐ¸Ð¶Ð½ÑÑ Ð¿Ð°Ð½ÐµÐ»Ñ
        bottom_layout = QHBoxLayout()
        
        # ÐÐµÐ²Ð°Ñ Ð½Ð¸Ð¶Ð½ÑÑ - ÐÐ¾Ð¼Ð°Ð½Ð´Ñ
        self.command_panel = SystemPanel("ÐÐÐÐÐÐÐ«")
        self.command_label = self.command_panel.add_stat("ÐÐ¾ÑÐ»ÐµÐ´Ð½ÑÑ", "ÐÐµÑ Ð´Ð°Ð½Ð½ÑÑ")
        bottom_layout.addWidget(self.command_panel)
        
        bottom_layout.addStretch()
        
        # ÐÑÐ°Ð²Ð°Ñ Ð½Ð¸Ð¶Ð½ÑÑ - Ð¡ÐµÑÑ
        self.network_panel = SystemPanel("Ð¡ÐÐ¢Ð¬")
        self.network_label = self.network_panel.add_stat("Ð¡ÑÐ°ÑÑÑ", "ÐÐ¾Ð´ÐºÐ»ÑÑÐµÐ½Ð¾")
        self.speed_label = self.network_panel.add_stat("Ð¡ÐºÐ¾ÑÐ¾ÑÑÑ", "0 MB/s")
        bottom_layout.addWidget(self.network_panel)
        
        main_layout.addLayout(bottom_layout)
        
        # Ð¢Ð°Ð¹Ð¼ÐµÑ Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ñ Ð´Ð°Ð½Ð½ÑÑ
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_data)
        self.update_timer.start(1000)
        
        # ÐÐ¾Ð´ÐºÐ»ÑÑÐµÐ½Ð¸Ðµ ÑÐ¸Ð³Ð½Ð°Ð»Ð° Ð³Ð¾Ð»Ð¾ÑÐ°
        self.voice_level_signal.connect(self.arc_reactor.set_voice_level)
        
        self.logger.info("JARVIS HUD Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½")
    
    def _update_data(self):
        """ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐ¸ÑÑÐµÐ¼Ð½ÑÑ Ð´Ð°Ð½Ð½ÑÑ."""
        from datetime import datetime
        
        # ÐÑÐµÐ¼Ñ Ð¸ Ð´Ð°ÑÐ°
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))
        self.date_label.setText(now.strftime("%d.%m.%Y"))
        
        # Ð¡Ð¸ÑÑÐµÐ¼Ð°
        self.cpu_label.setText(f"{psutil.cpu_percent()}%")
        self.ram_label.setText(f"{psutil.virtual_memory().percent}%")
        self.disk_label.setText(f"{psutil.disk_usage('/').percent}%")
        
        # Ð¡ÐµÑÑ
        try:
            net_io = psutil.net_io_counters()
            speed_mb = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024
            self.speed_label.setText(f"{speed_mb:.1f} MB/s")
        except:
            self.speed_label.setText("N/A")
    
    def update_command(self, command: str):
        """ÐÐ±Ð½Ð¾Ð²Ð¸ÑÑ Ð¿Ð¾ÑÐ»ÐµÐ´Ð½ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ."""
        self.command_label.setText(command[:30] + "..." if len(command) > 30 else command)
    
    def set_voice_level(self, level: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÑÐ¾Ð²ÐµÐ½Ñ Ð³Ð¾Ð»Ð¾ÑÐ°."""
        self.voice_level_signal.emit(level)
    
    def show_hud(self):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ HUD."""
        self.show()
        self.logger.info("JARVIS HUD Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½")
    
    def hide_hud(self):
        """Ð¡ÐºÑÑÑÑ HUD."""
        self.hide()
        self.logger.info("JARVIS HUD ÑÐºÑÑÑ")
    
    def toggle_hud(self):
        """ÐÐµÑÐµÐºÐ»ÑÑÐ¸ÑÑ Ð²Ð¸Ð´Ð¸Ð¼Ð¾ÑÑÑ HUD."""
        if self.isVisible():
            self.hide_hud()
        else:
            self.show_hud()
