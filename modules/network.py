"""
Сетевые операции JARVIS
"""

import requests
import speedtest
from typing import Dict


class NetworkModule:
    """Сетевые функции."""

    def __init__(self, brain):
        self.brain = brain

    def get_ip(self) -> Dict:
        """Получить IP адрес."""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            data = response.json()
            return {"status": "ok", "ip": data['ip']}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def speed_test(self) -> Dict:
        """Тест скорости интернета."""
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            ping = st.results.ping

            return {
                "status": "ok",
                "download": round(download, 2),
                "upload": round(upload, 2),
                "ping": round(ping, 2),
                "unit": "Mbps"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def check_connection(self) -> Dict:
        """Проверить подключение к интернету."""
        try:
            requests.get('https://www.google.com', timeout=5)
            return {"status": "ok", "connected": True}
        except:
            return {"status": "ok", "connected": False}
