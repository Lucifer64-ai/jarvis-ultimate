"""Lightweight, recommendation-only optimization agents for JARVIS."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

try:
    import psutil
except ImportError:  # Keep the learning manager usable without optional monitoring.
    psutil = None


class ResourceOptimizationAgent:
    """Observe CPU and memory pressure and suggest safe next steps."""

    def __init__(self, brain):
        self.brain = brain

    def analyze(self) -> Dict:
        config = self.brain.config
        cpu_threshold = config.get("optimization.cpu_threshold_percent", 80)
        memory_threshold = config.get("optimization.memory_threshold_percent", 85)
        recommendations: List[str] = []
        metrics = {"cpu_percent": None, "memory_percent": None}

        if psutil is None:
            return {
                "status": "unavailable",
                "metrics": metrics,
                "recommendations": [],
                "message": "Мониторинг ресурсов недоступен: не установлен psutil",
            }

        try:
            # interval=None reads the latest CPU sample without blocking command handling.
            metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
            metrics["memory_percent"] = psutil.virtual_memory().percent
        except Exception as error:
            self.brain.logger.debug("Не удалось получить метрики ресурсов: %s", error)
            return {
                "status": "error",
                "metrics": metrics,
                "recommendations": [],
                "message": "Не удалось получить метрики ресурсов",
            }

        if metrics["cpu_percent"] >= cpu_threshold:
            recommendations.append(
                "Высокая нагрузка на CPU: отложите тяжёлые фоновые задачи и повторите проверку позже."
            )
        if metrics["memory_percent"] >= memory_threshold:
            recommendations.append(
                "Мало свободной памяти: проверьте приложения с высоким потреблением RAM."
            )

        return {
            "status": "ok",
            "metrics": metrics,
            "recommendations": recommendations,
        }


class WorkflowOptimizationAgent:
    """Expose existing pattern-recognition suggestions without executing them."""

    def __init__(self, learning_manager):
        self.learning_manager = learning_manager

    def analyze(self) -> Dict:
        recognizer = self.learning_manager.pattern_recognizer
        suggestions = recognizer.get_suggestions() if recognizer else []
        return {
            "status": "ok" if recognizer else "unavailable",
            "suggestions": list(suggestions),
            "recommendations": [
                item.get("suggestion", "")
                for item in suggestions
                if isinstance(item, dict) and item.get("suggestion")
            ],
        }


class OptimizationManager:
    """Coordinate optimization agents; agents only observe and recommend."""

    def __init__(self, brain, learning_manager):
        self.brain = brain
        self.resource_agent = ResourceOptimizationAgent(brain)
        self.workflow_agent = WorkflowOptimizationAgent(learning_manager)

    def analyze(self) -> Dict:
        resource = self.resource_agent.analyze()
        workflow = self.workflow_agent.analyze()
        limit = self.brain.config.get("optimization.max_recommendations", 3)
        recommendations = (
            resource.get("recommendations", [])
            + workflow.get("recommendations", [])
        )[:max(0, int(limit))]

        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "resource": resource,
                "workflow": workflow,
            },
            "recommendations": recommendations,
            "automatic_actions": False,
        }
