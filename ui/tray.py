"""
Ð¢ÑÐµÐ¹-Ð¸ÐºÐ¾Ð½ÐºÐ° JARVIS
"""

import pystray
from PIL import Image, ImageDraw
import threading


class TrayIcon:
    """ÐÐºÐ¾Ð½ÐºÐ° Ð² ÑÐ¸ÑÑÐµÐ¼Ð½Ð¾Ð¼ ÑÑÐµÐµ."""

    def __init__(self, brain):
        self.brain = brain
        self.icon = None
        self._create_icon()

    def _create_icon(self):
        """Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð¸ÐºÐ¾Ð½ÐºÐ¸."""
        # Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð¿ÑÐ¾ÑÑÐ¾Ð¹ Ð¸ÐºÐ¾Ð½ÐºÐ¸ JARVIS
        image = Image.new('RGB', (64, 64), color='#0f0f1e')
        dc = ImageDraw.Draw(image)
        
        # ÐÑÑÐ³
        dc.ellipse([8, 8, 56, 56], outline='#00d4ff', width=3)
        
        # ÐÑÐºÐ²Ð° J
        dc.text((24, 18), "J", fill='#00d4ff')
        
        self.image = image

    def start(self):
        """ÐÐ°Ð¿ÑÑÐº Ð¸ÐºÐ¾Ð½ÐºÐ¸ Ð² ÑÑÐµÐµ."""
        menu = pystray.Menu(
            pystray.MenuItem("ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ HUD", self._show_hud),
            pystray.MenuItem("Ð¡ÐºÑÑÑÑ HUD", self._hide_hud),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Ð¡ÑÐ°ÑÑÑ", self._show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("ÐÑÑÐ¾Ð´", self._quit)
        )
        
        self.icon = pystray.Icon("jarvis", self.image, "JARVIS", menu)
        
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()

    def _show_hud(self, icon, item):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ HUD."""
        if hasattr(self.brain, 'hud'):
            self.brain.hud.start()

    def _hide_hud(self, icon, item):
        """Ð¡ÐºÑÑÑÑ HUD."""
        if hasattr(self.brain, 'hud'):
            self.brain.hud.stop()

    def _show_status(self, icon, item):
        """ÐÐ¾ÐºÐ°Ð·Ð°ÑÑ ÑÑÐ°ÑÑÑ."""
        status = self.brain.get_status()
        self.brain.logger.info(f"Ð¡ÑÐ°ÑÑÑ: {status}")

    def _quit(self, icon, item):
        """ÐÑÑÐ¾Ð´ Ð¸Ð· Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        self.brain.stop()
        icon.stop()

    def stop(self):
        """ÐÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¸ÐºÐ¾Ð½ÐºÐ¸."""
        if self.icon:
            self.icon.stop()
