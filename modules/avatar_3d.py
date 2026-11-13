"""
3D Avatar Module - ÐÐ¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¸Ð¹ Ð°Ð²Ð°ÑÐ°Ñ JARVIS
Ð ÐµÐ°Ð³Ð¸ÑÑÐµÑ Ð½Ð° Ð³Ð¾Ð»Ð¾Ñ Ð¸ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ
"""

import sys
import math
import time
import threading
from typing import Optional, Dict
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QLinearGradient


class HolographicAvatar(QWidget):
    """ÐÐ¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¸Ð¹ 3D Ð°Ð²Ð°ÑÐ°Ñ JARVIS."""

    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.logger = brain.logger
        
        # Ð¡Ð¾ÑÑÐ¾ÑÐ½Ð¸Ðµ Ð°Ð²Ð°ÑÐ°ÑÐ°
        self.state = "idle"  # idle, listening, speaking, thinking, processing
        self.voice_level = 0.0
        self.rotation_angle = 0.0
        self.pulse_phase = 0.0
        self.energy_level = 0.5
        
        # ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð¾ÑÐ¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ
        self.width = 400
        self.height = 400
        self.position_x = 100
        self.position_y = 100
        
        # ÐÐ½Ð¸Ð¼Ð°ÑÐ¸Ñ
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)  # ~60 FPS
        
        # ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° Ð¾ÐºÐ½Ð°
        self.setup_window()
        
        self.logger.info("â 3D Ð°Ð²Ð°ÑÐ°Ñ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½")

    def setup_window(self):
        """ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° Ð¿ÑÐ¾Ð·ÑÐ°ÑÐ½Ð¾Ð³Ð¾ Ð¾ÐºÐ½Ð°."""
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.setGeometry(self.position_x, self.position_y, self.width, self.height)
        
        # ÐÑÐ¾Ð·ÑÐ°ÑÐ½Ð¾ÑÑÑ
        self.setWindowOpacity(0.85)

    def paintEvent(self, event):
        """ÐÑÑÐ¸ÑÐ¾Ð²ÐºÐ° Ð³Ð¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¾Ð³Ð¾ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Ð¦ÐµÐ½ÑÑ Ð°Ð²Ð°ÑÐ°ÑÐ°
        center_x = self.width // 2
        center_y = self.height // 2
        
        # === ÐÐ¡ÐÐÐÐÐÐ ÐÐÐ ÐÐ£Ð¡ (Arc Reactor ÑÑÐ¸Ð»Ñ) ===
        
        # ÐÐ½ÐµÑÐ½ÐµÐµ ÐºÐ¾Ð»ÑÑÐ¾
        outer_radius = 150
        self.draw_ring(painter, center_x, center_y, outer_radius, 20, 
                      QColor(0, 200, 255, 100), self.rotation_angle)
        
        # Ð¡ÑÐµÐ´Ð½ÐµÐµ ÐºÐ¾Ð»ÑÑÐ¾
        middle_radius = 120
        self.draw_ring(painter, center_x, center_y, middle_radius, 15,
                      QColor(0, 255, 255, 150), -self.rotation_angle * 1.5)
        
        # ÐÐ½ÑÑÑÐµÐ½Ð½ÐµÐµ ÐºÐ¾Ð»ÑÑÐ¾
        inner_radius = 90
        self.draw_ring(painter, center_x, center_y, inner_radius, 10,
                      QColor(100, 255, 255, 200), self.rotation_angle * 2)
        
        # === Ð¯ÐÐ Ð (Ð¿ÑÐ»ÑÑÐ¸ÑÑÑÑÐ¸Ð¹ ÑÐµÐ½ÑÑ) ===
        
        # ÐÑÐ»ÑÑÐ°ÑÐ¸Ñ ÑÐ´ÑÐ°
        pulse_size = 60 + math.sin(self.pulse_phase) * 10
        
        # ÐÑÐ°Ð´Ð¸ÐµÐ½Ñ ÑÐ´ÑÐ°
        gradient = QRadialGradient(center_x, center_y, pulse_size)
        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(0.3, QColor(100, 255, 255, 200))
        gradient.setColorAt(0.7, QColor(0, 200, 255, 150))
        gradient.setColorAt(1, QColor(0, 100, 200, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - pulse_size, center_y - pulse_size,
                           pulse_size * 2, pulse_size * 2)
        
        # === Ð­ÐÐÐ ÐÐÐ¢ÐÐ§ÐÐ¡ÐÐÐ ÐÐÐÐÐ ===
        
        self.draw_energy_lines(painter, center_x, center_y, inner_radius, outer_radius)
        
        # === ÐÐÐÐÐÐÐ¢ÐÐ  ÐÐÐÐÐ¡Ð ===
        
        if self.voice_level > 0.1:
            self.draw_voice_indicator(painter, center_x, center_y, outer_radius + 30)
        
        # === Ð¢ÐÐÐ¡Ð¢ Ð¡ÐÐ¡Ð¢ÐÐ¯ÐÐÐ¯ ===
        
        self.draw_state_text(painter, center_x, self.height - 50)
        
        painter.end()

    def draw_ring(self, painter: QPainter, cx: int, cy: int, radius: int, 
                  thickness: int, color: QColor, rotation: float):
        """ÐÑÑÐ¸ÑÐ¾Ð²ÐºÐ° Ð²ÑÐ°ÑÐ°ÑÑÐµÐ³Ð¾ÑÑ ÐºÐ¾Ð»ÑÑÐ°."""
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(rotation)
        
        # Ð¡ÐµÐ³Ð¼ÐµÐ½ÑÑ ÐºÐ¾Ð»ÑÑÐ°
        segments = 12
        for i in range(segments):
            angle = i * (360 / segments)
            painter.save()
            painter.rotate(angle)
            
            # ÐÑÐ°Ð´Ð¸ÐµÐ½Ñ ÑÐµÐ³Ð¼ÐµÐ½ÑÐ°
            gradient = QLinearGradient(0, -radius, 0, -radius + thickness)
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            
            # Ð Ð¸ÑÑÐµÐ¼ ÑÐµÐ³Ð¼ÐµÐ½Ñ
            painter.drawRoundedRect(-thickness // 2, -radius, thickness, thickness, 3, 3)
            
            painter.restore()
        
        painter.restore()

    def draw_energy_lines(self, painter: QPainter, cx: int, cy: int, 
                          inner_r: int, outer_r: int):
        """ÐÑÑÐ¸ÑÐ¾Ð²ÐºÐ° ÑÐ½ÐµÑÐ³ÐµÑÐ¸ÑÐµÑÐºÐ¸Ñ Ð»Ð¸Ð½Ð¸Ð¹."""
        lines = 8
        for i in range(lines):
            angle = i * (360 / lines) + self.rotation_angle * 3
            rad = math.radians(angle)
            
            x1 = cx + math.cos(rad) * inner_r
            y1 = cy + math.sin(rad) * inner_r
            x2 = cx + math.cos(rad) * outer_r
            y2 = cy + math.sin(rad) * outer_r
            
            # ÐÑÐ°Ð´Ð¸ÐµÐ½Ñ Ð»Ð¸Ð½Ð¸Ð¸
            gradient = QLinearGradient(x1, y1, x2, y2)
            gradient.setColorAt(0, QColor(0, 255, 255, 200))
            gradient.setColorAt(1, QColor(0, 255, 255, 0))
            
            pen = QPen(QBrush(gradient), 2)
            painter.setPen(pen)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_voice_indicator(self, painter: QPainter, cx: int, cy: int, radius: int):
        """ÐÑÑÐ¸ÑÐ¾Ð²ÐºÐ° Ð¸Ð½Ð´Ð¸ÐºÐ°ÑÐ¾ÑÐ° Ð³Ð¾Ð»Ð¾ÑÐ°."""
        # ÐÐ¾Ð»Ð½Ñ Ð³Ð¾Ð»Ð¾ÑÐ°
        waves = 3
        for i in range(waves):
            wave_radius = radius + i * 15
            alpha = int(200 * (1 - i / waves) * self.voice_level)
            
            pen = QPen(QColor(0, 255, 255, alpha))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            painter.drawEllipse(cx - wave_radius, cy - wave_radius,
                               wave_radius * 2, wave_radius * 2)

    def draw_state_text(self, painter: QPainter, x: int, y: int):
        """ÐÑÑÐ¸ÑÐ¾Ð²ÐºÐ° ÑÐµÐºÑÑÐ° ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ñ."""
        state_texts = {
            "idle": "ÐÐÐ¢ÐÐ",
            "listening": "Ð¡ÐÐ£Ð¨ÐÐ®...",
            "speaking": "ÐÐÐÐÐ Ð®...",
            "thinking": "ÐÐ£ÐÐÐ®...",
            "processing": "ÐÐÐ ÐÐÐÐ¢ÐÐ..."
        }
        
        text = state_texts.get(self.state, "ÐÐÐ¢ÐÐ")
        
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        
        # Ð¢ÐµÐ½Ñ ÑÐµÐºÑÑÐ°
        painter.setPen(QColor(0, 0, 0, 150))
        painter.drawText(x + 1, y + 1, text)
        
        # ÐÑÐ½Ð¾Ð²Ð½Ð¾Ð¹ ÑÐµÐºÑÑ
        painter.setPen(QColor(0, 255, 255, 255))
        painter.drawText(x, y, text)

    def update_animation(self):
        """ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ Ð°Ð½Ð¸Ð¼Ð°ÑÐ¸Ð¸."""
        # ÐÑÐ°ÑÐµÐ½Ð¸Ðµ
        self.rotation_angle += 1.0
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        
        # ÐÑÐ»ÑÑÐ°ÑÐ¸Ñ
        self.pulse_phase += 0.1
        if self.pulse_phase >= 2 * math.pi:
            self.pulse_phase = 0
        
        # ÐÐ°ÑÑÑÐ°Ð½Ð¸Ðµ Ð³Ð¾Ð»Ð¾ÑÐ°
        if self.voice_level > 0:
            self.voice_level -= 0.05
            if self.voice_level < 0:
                self.voice_level = 0
        
        # ÐÐµÑÐµÑÐ¸ÑÐ¾Ð²ÐºÐ°
        self.update()

    # === ÐÐ£ÐÐÐÐ§ÐÐ«Ð ÐÐÐ¢ÐÐÐ« ===

    def set_state(self, state: str):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ñ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        if state in ["idle", "listening", "speaking", "thinking", "processing"]:
            self.state = state
            self.logger.debug(f"ÐÐ²Ð°ÑÐ°Ñ: ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ -> {state}")

    def set_voice_level(self, level: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÑÑÐ¾Ð²Ð½Ñ Ð³Ð¾Ð»Ð¾ÑÐ° (0.0 - 1.0)."""
        self.voice_level = max(0.0, min(1.0, level))

    def set_energy_level(self, level: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° ÑÑÐ¾Ð²Ð½Ñ ÑÐ½ÐµÑÐ³Ð¸Ð¸ (0.0 - 1.0)."""
        self.energy_level = max(0.0, min(1.0, level))

    def show_avatar(self):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ Ð°Ð²Ð°ÑÐ°Ñ."""
        self.show()
        self.logger.info("ÐÐ²Ð°ÑÐ°Ñ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½")

    def hide_avatar(self):
        """Ð¡ÐºÑÑÑÑ Ð°Ð²Ð°ÑÐ°Ñ."""
        self.hide()
        self.logger.info("ÐÐ²Ð°ÑÐ°Ñ ÑÐºÑÑÑ")

    def move_to_position(self, x: int, y: int):
        """ÐÐµÑÐµÐ¼ÐµÑÐµÐ½Ð¸Ðµ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        self.position_x = x
        self.position_y = y
        self.move(x, y)

    def resize_avatar(self, width: int, height: int):
        """ÐÐ·Ð¼ÐµÐ½ÐµÐ½Ð¸Ðµ ÑÐ°Ð·Ð¼ÐµÑÐ° Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        self.width = width
        self.height = height
        self.setFixedSize(width, height)


class AvatarManager:
    """ÐÐµÐ½ÐµÐ´Ð¶ÐµÑ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ñ 3D Ð°Ð²Ð°ÑÐ°ÑÐ¾Ð¼."""

    def __init__(self, brain):
        self.brain = brain
        self.logger = brain.logger
        self.avatar: Optional[HolographicAvatar] = None
        self.app: Optional[QApplication] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False

    def initialize(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð°Ð²Ð°ÑÐ°ÑÐ° Ð² Ð¾ÑÐ´ÐµÐ»ÑÐ½Ð¾Ð¼ Ð¿Ð¾ÑÐ¾ÐºÐµ."""
        if self.running:
            self.logger.warning("ÐÐ²Ð°ÑÐ°Ñ ÑÐ¶Ðµ Ð·Ð°Ð¿ÑÑÐµÐ½")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_avatar_thread, daemon=True)
        self.thread.start()
        
        # ÐÐ¶Ð¸Ð´Ð°Ð½Ð¸Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸
        time.sleep(0.5)
        
        self.logger.info("â ÐÐµÐ½ÐµÐ´Ð¶ÐµÑ Ð°Ð²Ð°ÑÐ°ÑÐ° Ð·Ð°Ð¿ÑÑÐµÐ½")

    def _run_avatar_thread(self):
        """ÐÐ¾ÑÐ¾Ðº Ð´Ð»Ñ Ð·Ð°Ð¿ÑÑÐºÐ° Qt Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        try:
            self.app = QApplication(sys.argv)
            self.avatar = HolographicAvatar(self.brain)
            self.app.exec_()
        except Exception as e:
            self.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð² Ð¿Ð¾ÑÐ¾ÐºÐµ Ð°Ð²Ð°ÑÐ°ÑÐ°: {e}")
        finally:
            self.running = False

    def show(self):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ Ð°Ð²Ð°ÑÐ°Ñ."""
        if self.avatar:
            self.avatar.show_avatar()
            return {"status": "ok", "message": "ÐÐ²Ð°ÑÐ°Ñ Ð¿Ð¾ÐºÐ°Ð·Ð°Ð½"}
        return {"status": "error", "message": "ÐÐ²Ð°ÑÐ°Ñ Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}

    def hide(self):
        """Ð¡ÐºÑÑÑÑ Ð°Ð²Ð°ÑÐ°Ñ."""
        if self.avatar:
            self.avatar.hide_avatar()
            return {"status": "ok", "message": "ÐÐ²Ð°ÑÐ°Ñ ÑÐºÑÑÑ"}
        return {"status": "error", "message": "ÐÐ²Ð°ÑÐ°Ñ Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}

    def set_state(self, state: str):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        if self.avatar:
            self.avatar.set_state(state)

    def set_voice_level(self, level: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ ÑÑÐ¾Ð²ÐµÐ½Ñ Ð³Ð¾Ð»Ð¾ÑÐ°."""
        if self.avatar:
            self.avatar.set_voice_level(level)

    def move(self, x: int, y: int):
        """ÐÐµÑÐµÐ¼ÐµÑÑÐ¸ÑÑ Ð°Ð²Ð°ÑÐ°Ñ."""
        if self.avatar:
            self.avatar.move_to_position(x, y)
            return {"status": "ok", "message": f"ÐÐ²Ð°ÑÐ°Ñ Ð¿ÐµÑÐµÐ¼ÐµÑÑÐ½ Ð² ({x}, {y})"}
        return {"status": "error", "message": "ÐÐ²Ð°ÑÐ°Ñ Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}

    def resize(self, width: int, height: int):
        """ÐÐ·Ð¼ÐµÐ½Ð¸ÑÑ ÑÐ°Ð·Ð¼ÐµÑ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        if self.avatar:
            self.avatar.resize_avatar(width, height)
            return {"status": "ok", "message": f"Ð Ð°Ð·Ð¼ÐµÑ Ð¸Ð·Ð¼ÐµÐ½ÑÐ½ Ð½Ð° {width}x{height}"}
        return {"status": "error", "message": "ÐÐ²Ð°ÑÐ°Ñ Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}

    def get_status(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÑÐ°ÑÑÑ Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        if self.avatar:
            return {
                "status": "ok",
                "running": self.running,
                "state": self.avatar.state,
                "voice_level": self.avatar.voice_level,
                "energy_level": self.avatar.energy_level,
                "position": (self.avatar.position_x, self.avatar.position_y),
                "size": (self.avatar.width, self.avatar.height)
            }
        return {"status": "error", "message": "ÐÐ²Ð°ÑÐ°Ñ Ð½Ðµ Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½"}

    def stop(self):
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð°Ð²Ð°ÑÐ°ÑÐ°."""
        if self.app:
            self.app.quit()
        self.running = False
        self.logger.info("ÐÐ²Ð°ÑÐ°Ñ Ð¾ÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½")
