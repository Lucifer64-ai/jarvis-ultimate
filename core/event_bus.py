"""
Ð¡Ð¸ÑÑÐµÐ¼Ð° ÑÐ¾Ð±ÑÑÐ¸Ð¹ JARVIS
"""

from typing import Dict, List, Callable
from collections import defaultdict
import threading


class EventBus:
    """Ð¨Ð¸Ð½Ð° ÑÐ¾Ð±ÑÑÐ¸Ð¹ Ð´Ð»Ñ ÑÐ²ÑÐ·Ð¸ Ð¼ÐµÐ¶Ð´Ñ Ð¼Ð¾Ð´ÑÐ»ÑÐ¼Ð¸."""

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._events: List[Dict] = []
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable):
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def emit(self, event_type: str, data: Dict = None):
        event = {"type": event_type, "data": data or {}}
        with self._lock:
            self._events.append(event)


    def publish(self, event_type: str, data: Dict = None):
        """Алиас для emit() - публикация события."""
        self.emit(event_type, data)

    def process_events(self):
        with self._lock:
            events = self._events.copy()
            self._events.clear()

        for event in events:
            for listener in self._listeners.get(event["type"], []):
                try:
                    listener(event["data"])
                except Exception as e:
                    print(f"ÐÑÐ¸Ð±ÐºÐ° Ð¾Ð±ÑÐ°Ð±Ð¾ÑÑÐ¸ÐºÐ° ÑÐ¾Ð±ÑÑÐ¸Ñ: {e}")

    def clear(self):
        self._listeners.clear()
        self._events.clear()
