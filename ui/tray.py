"""
ÃÂ¢ÃÃÂµÃÂ¹-ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ° JARVIS
"""

import pystray
from PIL import Image, ImageDraw
import threading


class TrayIcon:
    """ÃÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ° ÃÂ² ÃÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ½ÃÂ¾ÃÂ¼ ÃÃÃÂµÃÂµ."""

    def __init__(self, brain):
        self.brain = brain
        self.icon = None
        self._create_icon()

    def _create_icon(self):
        """ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ¸."""
        # ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÃÂ¾ÃÃÃÂ¾ÃÂ¹ ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ¸ JARVIS
        image = Image.new('RGB', (64, 64), color='#0f0f1e')
        dc = ImageDraw.Draw(image)
        
        # ÃÃÃÃÂ³
        dc.ellipse([8, 8, 56, 56], outline='#00d4ff', width=3)
        
        # ÃÃÃÂºÃÂ²ÃÂ° J
        dc.text((24, 18), "J", fill='#00d4ff')
        
        self.image = image

    def start(self):
        """ÃÃÂ°ÃÂ¿ÃÃÃÂº ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ¸ ÃÂ² ÃÃÃÂµÃÂµ."""
        menu = pystray.Menu(
            pystray.MenuItem("ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ HUD", self._show_hud),
            pystray.MenuItem("ÃÂ¡ÃÂºÃÃÃÃ HUD", self._hide_hud),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("ÃÂ¡ÃÃÂ°ÃÃÃ", self._show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("ÃÃÃÃÂ¾ÃÂ´", self._quit)
        )
        
        self.icon = pystray.Icon("jarvis", self.image, "JARVIS", menu)
        
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()

    def _show_hud(self, icon, item):
        """ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ HUD."""
        if hasattr(self.brain, 'hud'):
            self.brain.hud.start()

    def _hide_hud(self, icon, item):
        """ÃÂ¡ÃÂºÃÃÃÃ HUD."""
        if hasattr(self.brain, 'hud'):
            self.brain.hud.stop()

    def _show_status(self, icon, item):
        """ÃÃÂ¾ÃÂºÃÂ°ÃÂ·ÃÂ°ÃÃ ÃÃÃÂ°ÃÃÃ."""
        status = self.brain.get_status()
        self.brain.logger.info(f"ÃÂ¡ÃÃÂ°ÃÃÃ: {status}")

    def _quit(self, icon, item):
        """ÃÃÃÃÂ¾ÃÂ´ ÃÂ¸ÃÂ· ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã."""
        self.brain.stop()
        icon.stop()

    def stop(self):
        """ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ¸ÃÂºÃÂ¾ÃÂ½ÃÂºÃÂ¸."""
        if self.icon:
            self.icon.stop()
