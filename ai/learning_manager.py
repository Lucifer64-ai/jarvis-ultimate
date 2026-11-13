"""
ÐÐµÐ½ÐµÐ´Ð¶ÐµÑ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ JARVIS - ÐºÐ¾Ð¾ÑÐ´Ð¸Ð½Ð¸ÑÑÐµÑ Ð²ÑÐµ Ð¼Ð¾Ð´ÑÐ»Ð¸ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ
"""

from typing import Dict, List
from datetime import datetime


class LearningManager:
    """Ð¦ÐµÐ½ÑÑÐ°Ð»Ð¸Ð·Ð¾Ð²Ð°Ð½Ð½Ð¾Ðµ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¾Ð±ÑÑÐµÐ½Ð¸ÐµÐ¼."""

    def __init__(self, brain):
        self.brain = brain
        self.adaptive_ml = None
        self.alias_system = None
        self.user_profile = None
        self.pattern_recognizer = None
        self.local_llm = None
        self.optimization_manager = None
        self._init_modules()

    def _init_modules(self):
        """ÐÐ½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð°ÑÐ¸Ñ Ð¼Ð¾Ð´ÑÐ»ÐµÐ¹ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ."""
        modules = [
            ("adaptive_ml", "ai.adaptive_ml", "AdaptiveMLEngine", "ÐÐ´Ð°Ð¿ÑÐ¸Ð²Ð½ÑÐ¹ ML"),
            ("alias_system", "ai.alias_system", "AliasSystem", "Ð¡Ð¸ÑÑÐµÐ¼Ð° Ð°Ð»Ð¸Ð°ÑÐ¾Ð²"),
            ("user_profile", "ai.user_profile", "UserProfile", "ÐÑÐ¾ÑÐ¸Ð»Ñ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ"),
            ("pattern_recognizer", "ai.pattern_recognizer", "PatternRecognizer", "Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ðµ Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð²"),
            ("local_llm", "ai.local_llm", "LocalLLM", "ÐÐ¾ÐºÐ°Ð»ÑÐ½Ð°Ñ LLM"),
        ]

        for attribute, module_name, class_name, label in modules:
            try:
                module = __import__(module_name, fromlist=[class_name])
                setattr(self, attribute, getattr(module, class_name)(self.brain))
                self.brain.logger.info("â %s Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½", label)
            except Exception as error:
                self.brain.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ %s: %s", label, error)

        try:
            from ai.optimization_agents import OptimizationManager
            self.optimization_manager = OptimizationManager(self.brain, self)
            self.brain.logger.info("â ÐÐ³ÐµÐ½ÑÑ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ")
        except Exception as error:
            self.brain.logger.error("ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð°Ð³ÐµÐ½ÑÐ¾Ð² Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸: %s", error)

    def process_command(self, text: str) -> Dict:
        """Process a command and attach current optimization status."""
        result = {"original": text, "processed": text, "modules_used": []}

        if self.alias_system:
            resolved = self.alias_system.resolve_alias(text)
            if resolved != text:
                result["processed"] = resolved
                result["alias_resolved"] = True
                result["modules_used"].append("alias_system")

        if self.adaptive_ml:
            classification = self.adaptive_ml.predict(result["processed"])
            result["classification"] = classification
            result["modules_used"].append("adaptive_ml")

            if classification.get("needs_learning"):
                result["learning_suggestion"] = classification.get("suggestion")

        if self.user_profile:
            self.user_profile.log_command(text)
            self.user_profile.update_activity()
            result["modules_used"].append("user_profile")

        if self.optimization_manager and self.brain.config.get("optimization.enabled", True):
            try:
                report = self.get_optimization_report()
                result["optimization"] = report
                result["modules_used"].append("optimization_agents")

                recommendations = report.get("recommendations", [])
                if recommendations:
                    self.brain.logger.info("Ð ÐµÐºÐ¾Ð¼ÐµÐ½Ð´Ð°ÑÐ¸Ð¸ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸: %s", "; ".join(recommendations))

                hud = getattr(self.brain, "hud", None)
                if hud and hasattr(hud, "set_optimization_status"):
                    hud.set_optimization_status(report)

            except Exception as error:
                self.brain.logger.debug("ÐÑÐ¸Ð±ÐºÐ° Ð°Ð½Ð°Ð»Ð¸Ð·Ð° Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸: %s", error)

        return result

    def optimize_runtime(self, text: str = "") -> Dict:
        """Return a fresh optimization report for CLI, API, or UI callers."""
        return self.get_optimization_report()

    def learn_new_command(self, text: str, category: str) -> Dict:
        if not self.adaptive_ml:
            return {"status": "error", "message": "ÐÐ´Ð°Ð¿ÑÐ¸Ð²Ð½ÑÐ¹ ML Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½"}
        return self.adaptive_ml.add_training_example(text, category)

    def create_alias(self, alias: str, command: str) -> Dict:
        if not self.alias_system:
            return {"status": "error", "message": "Ð¡Ð¸ÑÑÐµÐ¼Ð° Ð°Ð»Ð¸Ð°ÑÐ¾Ð² Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°"}
        return self.alias_system.add_alias(alias, command)

    def get_learning_status(self) -> Dict:
        status = {"modules": {}, "timestamp": datetime.now().isoformat()}

        if self.adaptive_ml:
            status["modules"]["adaptive_ml"] = self.adaptive_ml.get_training_stats()

        if self.alias_system:
            status["modules"]["alias_system"] = self.alias_system.get_alias_stats()

        if self.user_profile:
            status["modules"]["user_profile"] = self.user_profile.get_statistics()

        if self.pattern_recognizer:
            status["modules"]["pattern_recognizer"] = {
                "suggestions_count": len(self.pattern_recognizer.get_suggestions())
            }

        if self.local_llm:
            status["modules"]["local_llm"] = self.local_llm.get_status()

        status["modules"]["optimization_agents"] = self.get_optimization_status()
        return status

    def get_optimization_status(self) -> Dict:
        """Compact status for CLI and UI, independent of the full report."""
        report = self.get_optimization_report()
        agents = report.get("agents", {})
        return {
            "enabled": report.get("status") == "ok",
            "agent_names": list(agents.keys()),
            "recommendation_count": len(report.get("recommendations", [])),
            "cache": agents.get("cache", {}),
            "automatic_actions": False,
            "timestamp": report.get("timestamp"),
        }

    def format_optimization_status(self) -> str:
        """Human-readable status line suitable for CLI and logs."""
        status = self.get_optimization_status()
        if not status["enabled"]:
            return "ÐÐ³ÐµÐ½ÑÑ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð¾ÑÐºÐ»ÑÑÐµÐ½Ñ Ð¸Ð»Ð¸ Ð½ÐµÐ´Ð¾ÑÑÑÐ¿Ð½Ñ."

        cache = status.get("cache", {})
        return (
            f"ÐÐ¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ñ: {len(status['agent_names'])} Ð°Ð³ÐµÐ½ÑÐ¾Ð²; "
            f"ÑÐµÐºÐ¾Ð¼ÐµÐ½Ð´Ð°ÑÐ¸Ð¹: {status['recommendation_count']}; "
            f"ÐºÑÑ: {cache.get('cache_entries', 0)} Ð·Ð°Ð¿Ð¸ÑÐµÐ¹ "
            f"(hits={cache.get('hits', 0)}, misses={cache.get('misses', 0)})."
        )

    def get_optimization_report(self) -> Dict:
        if not self.optimization_manager:
            return {"status": "error", "message": "ÐÐ³ÐµÐ½ÑÑ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ñ", "recommendations": []}
        if not self.brain.config.get("optimization.enabled", True):
            return {"status": "disabled", "message": "ÐÐ³ÐµÐ½ÑÑ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð¾ÑÐºÐ»ÑÑÐµÐ½Ñ", "recommendations": []}
        return self.optimization_manager.analyze()

    def analyze_patterns(self) -> List[Dict]:
        if not self.pattern_recognizer or not self.user_profile:
            return []
        return self.pattern_recognizer.analyze_command_history(self.user_profile.command_history)

    def get_greeting(self) -> str:
        if self.user_profile:
            return self.user_profile.get_greeting()
        return "ÐÐ´ÑÐ°Ð²ÑÑÐ²ÑÐ¹ÑÐµ, ÑÑÑ."
