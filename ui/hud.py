"""
HUD-Ð¸Ð½ÑÐµÑÑÐµÐ¹Ñ JARVIS Ð² ÑÑÐ¸Ð»Ðµ Iron Man
"""

import tkinter as tk
from tkinter import Canvas
import threading
import psutil
from datetime import datetime


class HUDOverlay:
    """ÐÐ¾Ð»Ð¾Ð³ÑÐ°ÑÐ¸ÑÐµÑÐºÐ¸Ð¹ HUD-Ð¾Ð²ÐµÑÐ»ÐµÐ¹."""

    def __init__(self, brain):
        self.brain = brain
        self.root = None
        self.canvas = None
        self.running = False
        self.config = brain.config.get("hud", {})

    def start(self):
        """ÐÐ°Ð¿ÑÑÐº HUD Ð² Ð¾ÑÐ´ÐµÐ»ÑÐ½Ð¾Ð¼ Ð¿Ð¾ÑÐ¾ÐºÐµ."""
        if not self.config.get("enabled", True):
            return
        
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÐÑÐ½Ð¾Ð²Ð½Ð¾Ð¹ ÑÐ¸ÐºÐ» HUD."""
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.7)
        self.root.configure(bg='black')
        
        # Ð Ð°Ð·Ð¼ÐµÑ Ð¸ Ð¿Ð¾Ð·Ð¸ÑÐ¸Ñ
        width, height = 400, 300
        screen_width = self.root.winfo_screenwidth()
        
        position = self.config.get("position", "top-right")
        if position == "top-right":
            x = screen_width - width - 20
            y = 20
        else:
            x = 20
            y = 20
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Canvas Ð´Ð»Ñ ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ñ
        self.canvas = Canvas(self.root, width=width, height=height, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Ð Ð°Ð¼ÐºÐ°
        self.canvas.create_rectangle(5, 5, width-5, height-5, outline='#00d4ff', width=2)
        
        # ÐÐ°Ð³Ð¾Ð»Ð¾Ð²Ð¾Ðº
        self.canvas.create_text(width//2, 25, text="J.A.R.V.I.S.", fill='#00d4ff', font=('Consolas', 16, 'bold'))
        
        self.running = True
        self._update()
        self.root.mainloop()

    def _update(self):
        """ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ Ð´Ð°Ð½Ð½ÑÑ HUD."""
        if not self.running:
            return
        
        try:
            # ÐÑÐ¸ÑÑÐºÐ° ÑÑÐ°ÑÑÑ Ð´Ð°Ð½Ð½ÑÑ
            self.canvas.delete("data")
            
            # ÐÑÐµÐ¼Ñ
            now = datetime.now().strftime("%H:%M:%S")
            self.canvas.create_text(200, 60, text=now, fill='#00d4ff', font=('Consolas', 14), tags="data")
            
            # CPU
            cpu = psutil.cpu_percent()
            self.canvas.create_text(50, 100, text=f"CPU: {cpu}%", fill='#00ff88', font=('Consolas', 11), anchor='w', tags="data")
            
            # RAM
            ram = psutil.virtual_memory().percent
            self.canvas.create_text(50, 130, text=f"RAM: {ram}%", fill='#00ff88', font=('Consolas', 11), anchor='w', tags="data")
            
            # Battery
            battery = psutil.sensors_battery()
            if battery:
                self.canvas.create_text(50, 160, text=f"BAT: {battery.percent}%", fill='#ffaa00', font=('Consolas', 11), anchor='w', tags="data")
            
            # Ð¡ÑÐ°ÑÑÑ
            self.canvas.create_text(200, 250, text="SYSTEM ONLINE", fill='#00d4ff', font=('Consolas', 10), tags="data")
            
        except Exception as e:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ñ HUD: {e}")
        
        # ÐÐ±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ÐºÐ°Ð¶Ð´ÑÐµ 2 ÑÐµÐºÑÐ½Ð´Ñ
        self.root.after(2000, self._update)

    def stop(self):
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° HUD."""
        self.running = False
        if self.root:
            self.root.quit()

    def show_message(self, message: str, duration: int = 3000):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ Ð²ÑÐµÐ¼ÐµÐ½Ð½Ð¾Ðµ ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ."""
        if not self.canvas:
            return
        
        text_id = self.canvas.create_text(
            200, 200, text=message, fill='#ffffff', font=('Consolas', 12)
        )
        self.root.after(duration, lambda: self.canvas.delete(text_id))
