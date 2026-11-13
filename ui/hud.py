"""
HUD-ÃÃÂ¸ÃÃÂ½ÃÃÃÂµÃÃÃÃÂµÃÃÂ¹Ã JARVIS ÃÃÂ² ÃÃÃÃÂ¸ÃÃÂ»ÃÃÂµ Iron Man
"""

import tkinter as tk
from tkinter import Canvas
import threading
import psutil
from datetime import datetime


class HUDOverlay:
    """ÃÃÃÂ¾ÃÃÂ»ÃÃÂ¾ÃÃÂ³ÃÃÃÂ°ÃÃÃÂ¸ÃÃÃÂµÃÃÃÂºÃÃÂ¸ÃÃÂ¹ HUD-ÃÃÂ¾ÃÃÂ²ÃÃÂµÃÃÃÂ»ÃÃÂµÃÃÂ¹."""

    def __init__(self, brain):
        self.brain = brain
        self.root = None
        self.canvas = None
        self.running = False
        self.config = brain.config.get("hud", {})

    def start(self):
        """ÃÃÃÂ°ÃÃÂ¿ÃÃÃÃÂº HUD ÃÃÂ² ÃÃÂ¾ÃÃÃÂ´ÃÃÂµÃÃÂ»ÃÃÃÂ½ÃÃÂ¾ÃÃÂ¼ ÃÃÂ¿ÃÃÂ¾ÃÃÃÂ¾ÃÃÂºÃÃÂµ."""
        if not self.config.get("enabled", True):
            return
        
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """ÃÃÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ½ÃÃÂ¾ÃÃÂ¹ ÃÃÃÂ¸ÃÃÂºÃÃÂ» HUD."""
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.7)
        self.root.configure(bg='black')
        
        # ÃÃÂ ÃÃÂ°ÃÃÂ·ÃÃÂ¼ÃÃÂµÃ ÃÃÂ¸ ÃÃÂ¿ÃÃÂ¾ÃÃÂ·ÃÃÂ¸ÃÃÃÂ¸Ã
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
        
        # Canvas ÃÃÂ´ÃÃÂ»Ã ÃÃÃÂ¸ÃÃÃÂ¾ÃÃÂ²ÃÃÂ°ÃÃÂ½ÃÃÂ¸Ã
        self.canvas = Canvas(self.root, width=width, height=height, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # ÃÃÂ ÃÃÂ°ÃÃÂ¼ÃÃÂºÃÃÂ°
        self.canvas.create_rectangle(5, 5, width-5, height-5, outline='#00d4ff', width=2)
        
        # ÃÃÃÂ°ÃÃÂ³ÃÃÂ¾ÃÃÂ»ÃÃÂ¾ÃÃÂ²ÃÃÂ¾ÃÃÂº
        self.canvas.create_text(width//2, 25, text="J.A.R.V.I.S.", fill='#00d4ff', font=('Consolas', 16, 'bold'))
        
        self.running = True
        self._update()
        self.root.mainloop()

    def _update(self):
        """ÃÃÃÂ±ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ´ÃÃÂ°ÃÃÂ½ÃÃÂ½ÃÃ HUD."""
        if not self.running:
            return
        
        try:
            # ÃÃÃÃÂ¸ÃÃÃÃÂºÃÃÂ° ÃÃÃÃÂ°ÃÃÃ ÃÃÂ´ÃÃÂ°ÃÃÂ½ÃÃÂ½ÃÃ
            self.canvas.delete("data")
            
            # ÃÃÃÃÂµÃÃÂ¼Ã
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
            
            # ÃÃÂ¡ÃÃÃÂ°ÃÃÃ
            self.canvas.create_text(200, 250, text="SYSTEM ONLINE", fill='#00d4ff', font=('Consolas', 10), tags="data")
            
        except Exception as e:
            self.brain.logger.error(f"ÃÃÃÃÂ¸ÃÃÂ±ÃÃÂºÃÃÂ° ÃÃÂ¾ÃÃÂ±ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸Ã HUD: {e}")
        
        # ÃÃÃÂ±ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂ»ÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂºÃÃÂ°ÃÃÂ¶ÃÃÂ´ÃÃÃÂµ 2 ÃÃÃÂµÃÃÂºÃÃÃÂ½ÃÃÂ´Ã
        self.root.after(2000, self._update)

    def stop(self):
        """ÃÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂºÃÃÂ° HUD."""
        self.running = False
        if self.root:
            self.root.quit()

    def show_message(self, message: str, duration: int = 3000):
        """ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ ÃÃÂ²ÃÃÃÂµÃÃÂ¼ÃÃÂµÃÃÂ½ÃÃÂ½ÃÃÂ¾ÃÃÂµ ÃÃÃÂ¾ÃÃÂ¾ÃÃÂ±ÃÃÃÂµÃÃÂ½ÃÃÂ¸ÃÃÂµ."""
        if not self.canvas:
            return
        
        text_id = self.canvas.create_text(
            200, 200, text=message, fill='#ffffff', font=('Consolas', 12)
        )
        self.root.after(duration, lambda: self.canvas.delete(text_id))
