"""
ÃÃÂ¢ÃÃÃÂµÃÃÂ¹-ÃÃÂ¸ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÂºÃÃÂ° JARVIS
"""

import pystray
from PIL import Image, ImageDraw
import threading


class TrayIcon:
    """ÃÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÂºÃÃÂ° ÃÃÂ² ÃÃÃÂ¸ÃÃÃÃÂµÃÃÂ¼ÃÃÂ½ÃÃÂ¾ÃÃÂ¼ ÃÃÃÃÂµÃÃÂµ."""

    def __init__(self, brain):
        self.brain = brain
        self.icon = None
        self._create_icon()

    def _create_icon(self):
        """ÃÃÂ¡ÃÃÂ¾ÃÃÂ·ÃÃÂ´ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ¸ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÂºÃÃÂ¸."""
        # ÃÃÂ¡ÃÃÂ¾ÃÃÂ·ÃÃÂ´ÃÃÂ°ÃÃÂ½ÃÃÂ¸ÃÃÂµ ÃÃÂ¿ÃÃÃÂ¾ÃÃÃÃÂ¾ÃÃÂ¹ ÃÃÂ¸ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÂºÃÃÂ¸ JARVIS
        image = Image.new('RGB', (64, 64), color='#0f0f1e')
        dc = ImageDraw.Draw(image)
        
        # ÃÃÃÃÃÂ³
        dc.ellipse([8, 8, 56, 56], outline='#00d4ff', width=3)
        
        # ÃÃÃÃÂºÃÃÂ²ÃÃÂ° J
        dc.text((24, 18), "J", fill='#00d4ff')
        
        self.image = image

    def start(self):
        """ÃÃÃÂ°ÃÃÂ¿ÃÃÃÃÂº ÃÃÂ¸ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÂºÃÃÂ¸ ÃÃÂ² ÃÃÃÃÂµÃÃÂµ."""
        menu = pystray.Menu(
            pystray.MenuItem("ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ HUD", self._show_hud),
            pystray.MenuItem("ÃÃÂ¡ÃÃÂºÃÃÃÃ HUD", self._hide_hud),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("ÃÃÂ¡ÃÃÃÂ°ÃÃÃ", self._show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("ÃÃÃÃÃÂ¾ÃÃÂ´", self._quit)
        )
        
        self.icon = pystray.Icon("jarvis", self.image, "JARVIS", menu)
        
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()

    def _show_hud(self, icon, item):
        """ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ HUD."""
        if hasattr(self.brain, 'hud'):
            self.brain.hud.start()

    def _hide_hud(self, icon, item):
        """ÃÃÂ¡ÃÃÂºÃÃÃÃ HUD."""
        if hasattr(self.brain, 'hud'):
            self.brain.hud.stop()

    def _show_status(self, icon, item):
        """ÃÃÃÂ¾ÃÃÂºÃÃÂ°ÃÃÂ·ÃÃÂ°ÃÃ ÃÃÃÃÂ°ÃÃÃ."""
        status = self.brain.get_status()
        self.brain.logger.info(f"ÃÃÂ¡ÃÃÃÂ°ÃÃÃ: {status}")

    def _quit(self, icon, item):
        """ÃÃÃÃÃÂ¾ÃÃÂ´ ÃÃÂ¸ÃÃÂ· ÃÃÂ¿ÃÃÃÂ¸ÃÃÂ»ÃÃÂ¾ÃÃÂ¶ÃÃÂµÃÃÂ½ÃÃÂ¸Ã."""
        self.brain.stop()
        icon.stop()

    def stop(self):
        """ÃÃÃÃÃÂ°ÃÃÂ½ÃÃÂ¾ÃÃÂ²ÃÃÂºÃÃÂ° ÃÃÂ¸ÃÃÂºÃÃÂ¾ÃÃÂ½ÃÃÂºÃÃÂ¸."""
        if self.icon:
            self.icon.stop()
