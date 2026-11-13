"""
HUD-ÃÂ¸ÃÂ½ÃÃÂµÃÃÃÂµÃÂ¹Ã JARVIS ÃÂ² ÃÃÃÂ¸ÃÂ»ÃÂµ Iron Man
"""

import tkinter as tk
from tkinter import Canvas
import threading
import psutil
from datetime import datetime


class HUDOverlay:
    """ÃÃÂ¾ÃÂ»ÃÂ¾ÃÂ³ÃÃÂ°ÃÃÂ¸ÃÃÂµÃÃÂºÃÂ¸ÃÂ¹ HUD-ÃÂ¾ÃÂ²ÃÂµÃÃÂ»ÃÂµÃÂ¹."""

    def __init__(self, brain):
        self.brain = brain
        self.root = None
        self.canvas = None
        self.running = False
        self.config = brain.config.get("hud", {})

    def start(self):
        """ÃÃÂ°ÃÂ¿ÃÃÃÂº HUD ÃÂ² ÃÂ¾ÃÃÂ´ÃÂµÃÂ»ÃÃÂ½ÃÂ¾ÃÂ¼ ÃÂ¿ÃÂ¾ÃÃÂ¾ÃÂºÃÂµ."""
        if not self.config.get("enabled", True):
            return
        
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÃÃÃÂ½ÃÂ¾ÃÂ²ÃÂ½ÃÂ¾ÃÂ¹ ÃÃÂ¸ÃÂºÃÂ» HUD."""
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.7)
        self.root.configure(bg='black')
        
        # ÃÂ ÃÂ°ÃÂ·ÃÂ¼ÃÂµÃ ÃÂ¸ ÃÂ¿ÃÂ¾ÃÂ·ÃÂ¸ÃÃÂ¸Ã
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
        
        # Canvas ÃÂ´ÃÂ»Ã ÃÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸Ã
        self.canvas = Canvas(self.root, width=width, height=height, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # ÃÂ ÃÂ°ÃÂ¼ÃÂºÃÂ°
        self.canvas.create_rectangle(5, 5, width-5, height-5, outline='#00d4ff', width=2)
        
        # ÃÃÂ°ÃÂ³ÃÂ¾ÃÂ»ÃÂ¾ÃÂ²ÃÂ¾ÃÂº
        self.canvas.create_text(width//2, 25, text="J.A.R.V.I.S.", fill='#00d4ff', font=('Consolas', 16, 'bold'))
        
        self.running = True
        self._update()
        self.root.mainloop()

    def _update(self):
        """ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ´ÃÂ°ÃÂ½ÃÂ½ÃÃ HUD."""
        if not self.running:
            return
        
        try:
            # ÃÃÃÂ¸ÃÃÃÂºÃÂ° ÃÃÃÂ°ÃÃÃ ÃÂ´ÃÂ°ÃÂ½ÃÂ½ÃÃ
            self.canvas.delete("data")
            
            # ÃÃÃÂµÃÂ¼Ã
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
            
            # ÃÂ¡ÃÃÂ°ÃÃÃ
            self.canvas.create_text(200, 250, text="SYSTEM ONLINE", fill='#00d4ff', font=('Consolas', 10), tags="data")
            
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ¾ÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸Ã HUD: {e}")
        
        # ÃÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÂ°ÃÂ¶ÃÂ´ÃÃÂµ 2 ÃÃÂµÃÂºÃÃÂ½ÃÂ´Ã
        self.root.after(2000, self._update)

    def stop(self):
        """ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° HUD."""
        self.running = False
        if self.root:
            self.root.quit()

    def show_message(self, message: str, duration: int = 3000):
        """ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ ÃÂ²ÃÃÂµÃÂ¼ÃÂµÃÂ½ÃÂ½ÃÂ¾ÃÂµ ÃÃÂ¾ÃÂ¾ÃÂ±ÃÃÂµÃÂ½ÃÂ¸ÃÂµ."""
        if not self.canvas:
            return
        
        text_id = self.canvas.create_text(
            200, 200, text=message, fill='#ffffff', font=('Consolas', 12)
        )
        self.root.after(duration, lambda: self.canvas.delete(text_id))
