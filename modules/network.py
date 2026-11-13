"""
ÃÂ¡ÃÂµÃÃÂµÃÂ²ÃÃÂµ ÃÂ¾ÃÂ¿ÃÂµÃÃÂ°ÃÃÂ¸ÃÂ¸ JARVIS.
"""

from concurrent.futures import Future, ThreadPoolExecutor
import threading
import uuid
from typing import Dict

import requests
import speedtest


class NetworkModule:
    """ÃÂ¡ÃÂµÃÃÂµÃÂ²ÃÃÂµ ÃÃÃÂ½ÃÂºÃÃÂ¸ÃÂ¸ Ã ÃÃÂ¾ÃÂ½ÃÂ¾ÃÂ²ÃÃÂ¼ ÃÂ²ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂµÃÂ½ÃÂ¸ÃÂµÃÂ¼ ÃÃÂµÃÃÃÂ° ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃÂ¸."""

    def __init__(self, brain):
        self.brain = brain
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="jarvis-network")
        self._lock = threading.Lock()
        self._speed_future: Future | None = None
        self._speed_job_id: str | None = None
        self._speed_result: Dict | None = None

    def get_ip(self) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ IP ÃÂ°ÃÂ´ÃÃÂµÃ."""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            response.raise_for_status()
            return {"status": "ok", "ip": response.json()['ip']}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def speed_test(self) -> Dict:
        """ÃÃÂ¾ÃÃÃÂ°ÃÂ²ÃÂ¸ÃÃ ÃÂ´ÃÂ»ÃÂ¸ÃÃÂµÃÂ»ÃÃÂ½ÃÃÂ¹ ÃÃÂµÃÃ ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃÂ¸ ÃÂ² ÃÃÂ¾ÃÂ½ÃÂ¾ÃÂ²ÃÃ ÃÂ¾ÃÃÂµÃÃÂµÃÂ´Ã.

        ÃÂ ÃÂµÃÂ·ÃÃÂ»ÃÃÃÂ°Ã ÃÂ¼ÃÂ¾ÃÂ¶ÃÂ½ÃÂ¾ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÃÂµÃÃÂµÃÂ· get_speed_test_status(); ÃÂ¿ÃÂ¾ÃÂ²ÃÃÂ¾ÃÃÂ½ÃÃÂ¹ ÃÂ²ÃÃÂ·ÃÂ¾ÃÂ²
        ÃÂ²ÃÂ¾ ÃÂ²ÃÃÂµÃÂ¼Ã ÃÂ²ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂµÃÂ½ÃÂ¸Ã ÃÂ²ÃÂ¾ÃÂ·ÃÂ²ÃÃÂ°ÃÃÂ°ÃÂµÃ ÃÂ¸ÃÂ´ÃÂµÃÂ½ÃÃÂ¸ÃÃÂ¸ÃÂºÃÂ°ÃÃÂ¾Ã ÃÃÂ¶ÃÂµ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ÃÂ½ÃÂ¾ÃÂ¹ ÃÂ·ÃÂ°ÃÂ´ÃÂ°ÃÃÂ¸.
        """
        with self._lock:
            if self._speed_future and not self._speed_future.done():
                return {"status": "pending", "job_id": self._speed_job_id,
                        "message": "ÃÂ¢ÃÂµÃÃ ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃÂ¸ ÃÃÂ¶ÃÂµ ÃÂ²ÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÃÂµÃÃÃ"}

            self._speed_job_id = uuid.uuid4().hex
            self._speed_result = None
            self._speed_future = self._executor.submit(self._run_speed_test)
            self._speed_future.add_done_callback(self._on_speed_test_done)
            return {"status": "pending", "job_id": self._speed_job_id,
                    "message": "ÃÂ¢ÃÂµÃÃ ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃÂ¸ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂµÃÂ½ ÃÂ² ÃÃÂ¾ÃÂ½ÃÂµ"}

    @staticmethod
    def _run_speed_test() -> Dict:
        """ÃÃÃÂ¿ÃÂ¾ÃÂ»ÃÂ½ÃÂ¸ÃÃ ÃÂ±ÃÂ»ÃÂ¾ÃÂºÃÂ¸ÃÃÃÃÃÃ ÃÃÂ°ÃÂ±ÃÂ¾ÃÃ ÃÂ² worker-ÃÂ¿ÃÂ¾ÃÃÂ¾ÃÂºÃÂµ."""
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
        self.brain.logger.info("ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃÂ¸ ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÃÃÂµÃÂ½ÃÂ°: %s", result)

    def get_speed_test_status(self, job_id: str | None = None) -> Dict:
        """ÃÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÃÃÂ°ÃÃÃ ÃÂ¿ÃÂ¾ÃÃÂ»ÃÂµÃÂ´ÃÂ½ÃÂµÃÂ¹ ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ¸ ÃÃÂºÃÂ¾ÃÃÂ¾ÃÃÃÂ¸."""
        with self._lock:
            if job_id and job_id != self._speed_job_id:
                return {"status": "error", "message": "ÃÃÂ°ÃÂ´ÃÂ°ÃÃÂ° ÃÂ½ÃÂµ ÃÂ½ÃÂ°ÃÂ¹ÃÂ´ÃÂµÃÂ½ÃÂ°"}
            if self._speed_future is None:
                return {"status": "idle", "message": "ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° ÃÂµÃÃ ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ¿ÃÃÃÂºÃÂ°ÃÂ»ÃÂ°ÃÃ"}
            if self._speed_result is not None:
                return {"job_id": self._speed_job_id, **self._speed_result}
            return {"status": "pending", "job_id": self._speed_job_id}

    def check_connection(self) -> Dict:
        """ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂ¸ÃÃ ÃÂ¿ÃÂ¾ÃÂ´ÃÂºÃÂ»ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂº ÃÂ¸ÃÂ½ÃÃÂµÃÃÂ½ÃÂµÃÃ."""
        try:
            response = requests.get('https://www.google.com', timeout=5)
            response.raise_for_status()
            return {"status": "ok", "connected": True}
        except requests.RequestException:
            return {"status": "ok", "connected": False}

    def close(self) -> None:
        """ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ¸ÃÃ ÃÂ¾ÃÃÂµÃÃÂµÃÂ´Ã ÃÃÂ¾ÃÂ½ÃÂ¾ÃÂ²ÃÃ ÃÂ·ÃÂ°ÃÂ´ÃÂ°Ã ÃÂ±ÃÂµÃÂ· ÃÂ¾ÃÂ¶ÃÂ¸ÃÂ´ÃÂ°ÃÂ½ÃÂ¸Ã ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÃÃÂµÃÂ½ÃÂ¸Ã ÃÃÂµÃÃÃÂ°."""
        self._executor.shutdown(wait=False, cancel_futures=True)
