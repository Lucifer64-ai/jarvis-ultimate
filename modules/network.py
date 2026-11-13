"""
Ð¡ÐµÑÐµÐ²ÑÐµ Ð¾Ð¿ÐµÑÐ°ÑÐ¸Ð¸ JARVIS.
"""

from concurrent.futures import Future, ThreadPoolExecutor
import threading
import uuid
from typing import Dict

import requests
import speedtest


class NetworkModule:
    """Ð¡ÐµÑÐµÐ²ÑÐµ ÑÑÐ½ÐºÑÐ¸Ð¸ Ñ ÑÐ¾Ð½Ð¾Ð²ÑÐ¼ Ð²ÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸ÐµÐ¼ ÑÐµÑÑÐ° ÑÐºÐ¾ÑÐ¾ÑÑÐ¸."""

    def __init__(self, brain):
        self.brain = brain
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="jarvis-network")
        self._lock = threading.Lock()
        self._speed_future: Future | None = None
        self._speed_job_id: str | None = None
        self._speed_result: Dict | None = None

    def get_ip(self) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ IP Ð°Ð´ÑÐµÑ."""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            response.raise_for_status()
            return {"status": "ok", "ip": response.json()['ip']}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def speed_test(self) -> Dict:
        """ÐÐ¾ÑÑÐ°Ð²Ð¸ÑÑ Ð´Ð»Ð¸ÑÐµÐ»ÑÐ½ÑÐ¹ ÑÐµÑÑ ÑÐºÐ¾ÑÐ¾ÑÑÐ¸ Ð² ÑÐ¾Ð½Ð¾Ð²ÑÑ Ð¾ÑÐµÑÐµÐ´Ñ.

        Ð ÐµÐ·ÑÐ»ÑÑÐ°Ñ Ð¼Ð¾Ð¶Ð½Ð¾ Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ ÑÐµÑÐµÐ· get_speed_test_status(); Ð¿Ð¾Ð²ÑÐ¾ÑÐ½ÑÐ¹ Ð²ÑÐ·Ð¾Ð²
        Ð²Ð¾ Ð²ÑÐµÐ¼Ñ Ð²ÑÐ¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ñ Ð²Ð¾Ð·Ð²ÑÐ°ÑÐ°ÐµÑ Ð¸Ð´ÐµÐ½ÑÐ¸ÑÐ¸ÐºÐ°ÑÐ¾Ñ ÑÐ¶Ðµ Ð·Ð°Ð¿ÑÑÐµÐ½Ð½Ð¾Ð¹ Ð·Ð°Ð´Ð°ÑÐ¸.
        """
        with self._lock:
            if self._speed_future and not self._speed_future.done():
                return {"status": "pending", "job_id": self._speed_job_id,
                        "message": "Ð¢ÐµÑÑ ÑÐºÐ¾ÑÐ¾ÑÑÐ¸ ÑÐ¶Ðµ Ð²ÑÐ¿Ð¾Ð»Ð½ÑÐµÑÑÑ"}

            self._speed_job_id = uuid.uuid4().hex
            self._speed_result = None
            self._speed_future = self._executor.submit(self._run_speed_test)
            self._speed_future.add_done_callback(self._on_speed_test_done)
            return {"status": "pending", "job_id": self._speed_job_id,
                    "message": "Ð¢ÐµÑÑ ÑÐºÐ¾ÑÐ¾ÑÑÐ¸ Ð·Ð°Ð¿ÑÑÐµÐ½ Ð² ÑÐ¾Ð½Ðµ"}

    @staticmethod
    def _run_speed_test() -> Dict:
        """ÐÑÐ¿Ð¾Ð»Ð½Ð¸ÑÑ Ð±Ð»Ð¾ÐºÐ¸ÑÑÑÑÑÑ ÑÐ°Ð±Ð¾ÑÑ Ð² worker-Ð¿Ð¾ÑÐ¾ÐºÐµ."""
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            return {
                "status": "ok",
                "download": round(download, 2),
                "upload": round(upload, 2),
                "ping": round(st.results.ping, 2),
                "unit": "Mbps"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _on_speed_test_done(self, future: Future) -> None:
        try:
            result = future.result()
        except Exception as e:
            result = {"status": "error", "message": str(e)}
        with self._lock:
            self._speed_result = result
        self.brain.logger.info("ÐÑÐ¾Ð²ÐµÑÐºÐ° ÑÐºÐ¾ÑÐ¾ÑÑÐ¸ Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð°: %s", result)

    def get_speed_test_status(self, job_id: str | None = None) -> Dict:
        """ÐÐ¾Ð»ÑÑÐ¸ÑÑ ÑÑÐ°ÑÑÑ Ð¿Ð¾ÑÐ»ÐµÐ´Ð½ÐµÐ¹ Ð¿ÑÐ¾Ð²ÐµÑÐºÐ¸ ÑÐºÐ¾ÑÐ¾ÑÑÐ¸."""
        with self._lock:
            if job_id and job_id != self._speed_job_id:
                return {"status": "error", "message": "ÐÐ°Ð´Ð°ÑÐ° Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°"}
            if self._speed_future is None:
                return {"status": "idle", "message": "ÐÑÐ¾Ð²ÐµÑÐºÐ° ÐµÑÑ Ð½Ðµ Ð·Ð°Ð¿ÑÑÐºÐ°Ð»Ð°ÑÑ"}
            if self._speed_result is not None:
                return {"job_id": self._speed_job_id, **self._speed_result}
            return {"status": "pending", "job_id": self._speed_job_id}

    def check_connection(self) -> Dict:
        """ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¿Ð¾Ð´ÐºÐ»ÑÑÐµÐ½Ð¸Ðµ Ðº Ð¸Ð½ÑÐµÑÐ½ÐµÑÑ."""
        try:
            response = requests.get('https://www.google.com', timeout=5)
            response.raise_for_status()
            return {"status": "ok", "connected": True}
        except requests.RequestException:
            return {"status": "ok", "connected": False}

    def close(self) -> None:
        """ÐÑÑÐ°Ð½Ð¾Ð²Ð¸ÑÑ Ð¾ÑÐµÑÐµÐ´Ñ ÑÐ¾Ð½Ð¾Ð²ÑÑ Ð·Ð°Ð´Ð°Ñ Ð±ÐµÐ· Ð¾Ð¶Ð¸Ð´Ð°Ð½Ð¸Ñ Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð¸Ñ ÑÐµÑÑÐ°."""
        self._executor.shutdown(wait=False, cancel_futures=True)
