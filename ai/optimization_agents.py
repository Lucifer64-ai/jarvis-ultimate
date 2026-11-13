"""Advanced optimization agents for JARVIS.

These agents do not mutate the system by themselves. They observe
resource pressure, cache repeated work, and prioritize likely repeated
workflow tasks by reusing the existing pattern-recognition data.
"""

from __future__ import annotations

import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List

try:
    import psutil
except ImportError:  # pragma: no cover - optional dependency
    psutil = None


class ResourceOptimizationAgent:
    """Monitor CPU and memory pressure and return safe recommendations."""

    def __init__(self, brain):
        self.brain = brain

    def analyze(self) -> Dict:
        config = self.brain.config
        cpu_threshold = config.get("optimization.cpu_threshold_percent", 80)
        memory_threshold = config.get("optimization.memory_threshold_percent", 85)
        recommendations: List[str] = []
        metrics = {"cpu_percent": None, "memory_percent": None, "active_processes": None}

        if psutil is None:
            return {
                "status": "unavailable",
                "metrics": metrics,
                "recommendations": [],
                "message": "ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ ÑÐµÑÑÑÑÐ¾Ð² Ð½ÐµÐ´Ð¾ÑÑÑÐ¿ÐµÐ½: psutil Ð½Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½",
            }

        try:
            metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
            metrics["memory_percent"] = psutil.virtual_memory().percent
            metrics["active_processes"] = len(psutil.pids())
        except Exception as error:
            self.brain.logger.debug("ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ Ð¼ÐµÑÑÐ¸ÐºÐ¸ ÑÐµÑÑÑÑÐ¾Ð²: %s", error)
            return {
                "status": "error",
                "metrics": metrics,
                "recommendations": [],
                "message": "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ Ð¼ÐµÑÑÐ¸ÐºÐ¸ ÑÐµÑÑÑÑÐ¾Ð²",
            }

        if metrics["cpu_percent"] >= cpu_threshold:
            recommendations.append(
                "ÐÑÑÐ¾ÐºÐ°Ñ Ð½Ð°Ð³ÑÑÐ·ÐºÐ° Ð½Ð° CPU: Ð²ÑÐµÐ¼ÐµÐ½Ð½Ð¾ Ð¾ÑÐ»Ð¾Ð¶Ð¸ÑÐµ ÑÑÐ¶ÑÐ»ÑÐµ ÑÐ¾Ð½Ð¾Ð²ÑÐµ Ð¿ÑÐ¾Ð²ÐµÑÐºÐ¸ Ð¸ Ð¿Ð¾Ð²ÑÐ¾ÑÐ¸ÑÐµ Ð·Ð°Ð´Ð°ÑÑ Ð¿Ð¾Ð·Ð¶Ðµ."
            )
        if metrics["memory_percent"] >= memory_threshold:
            recommendations.append(
                "ÐÐ¸Ð·ÐºÐ¸Ð¹ Ð·Ð°Ð¿Ð°Ñ Ð¿Ð°Ð¼ÑÑÐ¸: Ð¿ÑÐ¾Ð²ÐµÑÑÑÐµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ Ñ Ð²ÑÑÐ¾ÐºÐ¸Ð¼ Ð¿Ð¾ÑÑÐµÐ±Ð»ÐµÐ½Ð¸ÐµÐ¼ RAM Ð¸ ÑÐ¼ÐµÐ½ÑÑÐ¸ÑÐµ Ð¾Ð´Ð½Ð¾Ð²ÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð½Ð°Ð³ÑÑÐ·ÐºÑ."
            )
        if metrics["active_processes"] and metrics["active_processes"] > 200:
            recommendations.append(
                "Ð ÑÐ¸ÑÑÐµÐ¼Ðµ Ð¼Ð½Ð¾Ð³Ð¾ Ð°ÐºÑÐ¸Ð²Ð½ÑÑ Ð¿ÑÐ¾ÑÐµÑÑÐ¾Ð²: ÑÐ½Ð¸Ð·ÑÑÐµ ÐºÐ¾Ð»Ð¸ÑÐµÑÑÐ²Ð¾ ÑÐ¾Ð½Ð¾Ð²ÑÑ Ð·Ð°Ð´Ð°Ñ Ð¸ Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ð¹."
            )

        return {
            "status": "ok",
            "metrics": metrics,
            "recommendations": recommendations,
        }


class CacheOptimizationAgent:
    """Cache repetitive values for a short TTL to reduce repeated work."""

    def __init__(self, brain):
        self.brain = brain
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get_cache_key(self, prefix: str, payload: str) -> str:
        return f"{prefix}:{payload.lower().strip()}"

    def get_or_compute(self, key: str, callback: Callable[[], Any], ttl_seconds: float | None = None):
        ttl = ttl_seconds if ttl_seconds is not None else self.brain.config.get("optimization.cache_ttl_seconds", 30)
        now = time.time()
        value = self.cache.get(key)

        if value and (now - value["time"]) < ttl:
            return value["value"]

        computed = callback()
        self.cache[key] = {"time": now, "value": computed}
        return computed

    def get_summary(self) -> Dict:
        return {
            "cache_entries": len(self.cache),
            "ttl_seconds": self.brain.config.get("optimization.cache_ttl_seconds", 30),
        }


class WorkflowOptimizationAgent:
    """Rank likely repeated tasks using previous pattern suggestions."""

    def __init__(self, learning_manager):
        self.learning_manager = learning_manager

    def analyze(self) -> Dict:
        recognizer = self.learning_manager.pattern_recognizer
        suggestions = recognizer.get_suggestions() if recognizer else []
        top = []

        for item in suggestions:
            if not isinstance(item, dict):
                continue
            if item.get("action"):
                top.append({
                    "type": item.get("type", "unknown"),
                    "action": item.get("action"),
                    "suggestion": item.get("suggestion"),
                    "count": item.get("count", 0),
                })

        return {
            "status": "ok" if recognizer else "unavailable",
            "suggestions": top,
            "recommendations": [
                item.get("suggestion", "")
                for item in top
                if item.get("suggestion")
            ],
        }


class SchedulingOptimizationAgent:
    """Suggest task prioritization based on frequency and urgency."""

    def __init__(self, brain):
        self.brain = brain

    def analyze(self) -> Dict:
        scheduler = getattr(self.brain, "scheduler", None)
        tasks = scheduler.list_tasks() if scheduler else []
        task_payload = []

        for task in tasks:
            task_payload.append({
                "name": task.get("name"),
                "days": task.get("days", []),
                "time": task.get("time"),
                "callback": task.get("callback"),
            })

        return {
            "status": "ok" if scheduler else "unavailable",
            "task_count": len(task_payload),
            "tasks": task_payload,
            "recommendations": [
                "ÐÑÐ¾Ð²ÐµÑÑÑÐµ Ð¿Ð¾Ð²ÑÐ¾ÑÑÑÑÐ¸ÐµÑÑ ÑÐ¾Ð½Ð¾Ð²ÑÐµ Ð·Ð°Ð´Ð°ÑÐ¸ Ð¸ Ð¾Ð±ÑÐµÐ´Ð¸Ð½Ð¸ÑÐµ Ð¸Ñ, ÐµÑÐ»Ð¸ Ð¾Ð½Ð¸ Ð´ÑÐ±Ð»Ð¸ÑÑÑÑ Ð´ÑÑÐ³ Ð´ÑÑÐ³Ð°."
            ] if task_payload else [],
        }


class OptimizationManager:
    """Coordinate all optimization agents; no automatic execution by default."""

    def __init__(self, brain, learning_manager):
        self.brain = brain
        self.learning_manager = learning_manager
        self.resource_agent = ResourceOptimizationAgent(brain)
        self.cache_agent = CacheOptimizationAgent(brain)
        self.workflow_agent = WorkflowOptimizationAgent(learning_manager)
        self.scheduler_agent = SchedulingOptimizationAgent(brain)

    def analyze(self) -> Dict:
        resource = self.resource_agent.analyze()
        workflow = self.workflow_agent.analyze()
        scheduler = self.scheduler_agent.analyze()
        recommendations = (
            resource.get("recommendations", [])
            + workflow.get("recommendations", [])
            + scheduler.get("recommendations", [])
        )

        max_recommendations = int(self.brain.config.get("optimization.max_recommendations", 3))
        recommendations = recommendations[:max(0, max_recommendations)]

        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "resource": resource,
                "workflow": workflow,
                "scheduler": scheduler,
                "cache": self.cache_agent.get_summary(),
            },
            "recommendations": recommendations,
            "automatic_actions": False,
        }

    def get_or_compute(self, key: str, callback: Callable[[], Any], ttl_seconds: float | None = None):
        return self.cache_agent.get_or_compute(key, callback, ttl_seconds)

