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
                "message": "ÃÃÂ¾ÃÂ½ÃÂ¸ÃÃÂ¾ÃÃÂ¸ÃÂ½ÃÂ³ ÃÃÂµÃÃÃÃÃÂ¾ÃÂ² ÃÂ½ÃÂµÃÂ´ÃÂ¾ÃÃÃÃÂ¿ÃÂµÃÂ½: psutil ÃÂ½ÃÂµ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½",
            }

        try:
            metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
            metrics["memory_percent"] = psutil.virtual_memory().percent
            metrics["active_processes"] = len(psutil.pids())
        except Exception as error:
            self.brain.logger.debug("ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ¼ÃÂµÃÃÃÂ¸ÃÂºÃÂ¸ ÃÃÂµÃÃÃÃÃÂ¾ÃÂ²: %s", error)
            return {
                "status": "error",
                "metrics": metrics,
                "recommendations": [],
                "message": "ÃÃÂµ ÃÃÂ´ÃÂ°ÃÂ»ÃÂ¾ÃÃ ÃÂ¿ÃÂ¾ÃÂ»ÃÃÃÂ¸ÃÃ ÃÂ¼ÃÂµÃÃÃÂ¸ÃÂºÃÂ¸ ÃÃÂµÃÃÃÃÃÂ¾ÃÂ²",
            }

        if metrics["cpu_percent"] >= cpu_threshold:
            recommendations.append(
                "ÃÃÃÃÂ¾ÃÂºÃÂ°Ã ÃÂ½ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ° ÃÂ½ÃÂ° CPU: ÃÂ²ÃÃÂµÃÂ¼ÃÂµÃÂ½ÃÂ½ÃÂ¾ ÃÂ¾ÃÃÂ»ÃÂ¾ÃÂ¶ÃÂ¸ÃÃÂµ ÃÃÃÂ¶ÃÃÂ»ÃÃÂµ ÃÃÂ¾ÃÂ½ÃÂ¾ÃÂ²ÃÃÂµ ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ¸ ÃÂ¸ ÃÂ¿ÃÂ¾ÃÂ²ÃÃÂ¾ÃÃÂ¸ÃÃÂµ ÃÂ·ÃÂ°ÃÂ´ÃÂ°ÃÃ ÃÂ¿ÃÂ¾ÃÂ·ÃÂ¶ÃÂµ."
            )
        if metrics["memory_percent"] >= memory_threshold:
            recommendations.append(
                "ÃÃÂ¸ÃÂ·ÃÂºÃÂ¸ÃÂ¹ ÃÂ·ÃÂ°ÃÂ¿ÃÂ°Ã ÃÂ¿ÃÂ°ÃÂ¼ÃÃÃÂ¸: ÃÂ¿ÃÃÂ¾ÃÂ²ÃÂµÃÃÃÃÂµ ÃÂ¿ÃÃÂ¸ÃÂ»ÃÂ¾ÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã Ã ÃÂ²ÃÃÃÂ¾ÃÂºÃÂ¸ÃÂ¼ ÃÂ¿ÃÂ¾ÃÃÃÂµÃÂ±ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµÃÂ¼ RAM ÃÂ¸ ÃÃÂ¼ÃÂµÃÂ½ÃÃÃÂ¸ÃÃÂµ ÃÂ¾ÃÂ´ÃÂ½ÃÂ¾ÃÂ²ÃÃÂµÃÂ¼ÃÂµÃÂ½ÃÂ½ÃÃ ÃÂ½ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃ."
            )
        if metrics["active_processes"] and metrics["active_processes"] > 200:
            recommendations.append(
                "Ã ÃÃÂ¸ÃÃÃÂµÃÂ¼ÃÂµ ÃÂ¼ÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ°ÃÂºÃÃÂ¸ÃÂ²ÃÂ½ÃÃ ÃÂ¿ÃÃÂ¾ÃÃÂµÃÃÃÂ¾ÃÂ²: ÃÃÂ½ÃÂ¸ÃÂ·ÃÃÃÂµ ÃÂºÃÂ¾ÃÂ»ÃÂ¸ÃÃÂµÃÃÃÂ²ÃÂ¾ ÃÃÂ¾ÃÂ½ÃÂ¾ÃÂ²ÃÃ ÃÂ·ÃÂ°ÃÂ´ÃÂ°Ã ÃÂ¸ ÃÂ¾ÃÂ±ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂ¹."
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
                "ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÃÃÂµ ÃÂ¿ÃÂ¾ÃÂ²ÃÃÂ¾ÃÃÃÃÃÂ¸ÃÂµÃÃ ÃÃÂ¾ÃÂ½ÃÂ¾ÃÂ²ÃÃÂµ ÃÂ·ÃÂ°ÃÂ´ÃÂ°ÃÃÂ¸ ÃÂ¸ ÃÂ¾ÃÂ±ÃÃÂµÃÂ´ÃÂ¸ÃÂ½ÃÂ¸ÃÃÂµ ÃÂ¸Ã, ÃÂµÃÃÂ»ÃÂ¸ ÃÂ¾ÃÂ½ÃÂ¸ ÃÂ´ÃÃÂ±ÃÂ»ÃÂ¸ÃÃÃÃ ÃÂ´ÃÃÃÂ³ ÃÂ´ÃÃÃÂ³ÃÂ°."
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

