"""
ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ Ð¶ÐµÐ»ÐµÐ·Ðµ JARVIS
"""

import psutil
import cpuinfo
from typing import Dict


class HardwareModule:
    """ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ Ð¾Ð±Ð¾ÑÑÐ´Ð¾Ð²Ð°Ð½Ð¸Ñ."""

    def __init__(self, brain):
        self.brain = brain

    def get_cpu_info(self) -> Dict:
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ Ð¿ÑÐ¾ÑÐµÑÑÐ¾ÑÐµ."""
        cpu = cpuinfo.get_cpu_info()
        return {
            "brand": cpu.get('brand_raw', 'Unknown'),
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "usage": psutil.cpu_percent(interval=1)
        }

    def get_memory_info(self) -> Dict:
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ Ð¿Ð°Ð¼ÑÑÐ¸."""
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024**3), 2),
            "available": round(mem.available / (1024**3), 2),
            "used": round(mem.used / (1024**3), 2),
            "percent": mem.percent
        }

    def get_disk_info(self) -> Dict:
        """ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¾ Ð´Ð¸ÑÐºÐ°Ñ."""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total": round(usage.total / (1024**3), 2),
                    "used": round(usage.used / (1024**3), 2),
                    "free": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            except:
                pass
        return disks

    def get_full_report(self) -> Dict:
        """ÐÐ¾Ð»Ð½ÑÐ¹ Ð¾ÑÑÑÑ Ð¾ ÑÐ¸ÑÑÐµÐ¼Ðµ."""
        return {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disks": self.get_disk_info()
        }
