"""
ÃÃÂµÃÂ½ÃÂµÃÂ´ÃÂ¶ÃÂµÃ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã JARVIS - ÃÂºÃÂ¾ÃÂ¾ÃÃÂ´ÃÂ¸ÃÂ½ÃÂ¸ÃÃÃÂµÃ ÃÂ²ÃÃÂµ ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂ¸ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã
"""

from typing import Dict, List
from datetime import datetime


class LearningManager:
    """ÃÂ¦ÃÂµÃÂ½ÃÃÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ½ÃÂ¾ÃÂµ ÃÃÂ¿ÃÃÂ°ÃÂ²ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸ÃÂµÃÂ¼."""

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
        """ÃÃÂ½ÃÂ¸ÃÃÂ¸ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã ÃÂ¼ÃÂ¾ÃÂ´ÃÃÂ»ÃÂµÃÂ¹ ÃÂ¾ÃÂ±ÃÃÃÂµÃÂ½ÃÂ¸Ã."""
        modules = [
            ("adaptive_ml", "ai.adaptive_ml", "AdaptiveMLEngine", "ÃÃÂ´ÃÂ°ÃÂ¿ÃÃÂ¸ÃÂ²ÃÂ½ÃÃÂ¹ ML"),
            ("alias_system", "ai.alias_system", "AliasSystem", "ÃÂ¡ÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÂ°ÃÂ»ÃÂ¸ÃÂ°ÃÃÂ¾ÃÂ²"),
            ("user_profile", "ai.user_profile", "UserProfile", "ÃÃÃÂ¾ÃÃÂ¸ÃÂ»Ã ÃÂ¿ÃÂ¾ÃÂ»ÃÃÂ·ÃÂ¾ÃÂ²ÃÂ°ÃÃÂµÃÂ»Ã"),
            ("pattern_recognizer", "ai.pattern_recognizer", "PatternRecognizer", "ÃÂ ÃÂ°ÃÃÂ¿ÃÂ¾ÃÂ·ÃÂ½ÃÂ°ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ¿ÃÂ°ÃÃÃÂµÃÃÂ½ÃÂ¾ÃÂ²"),
            ("local_llm", "ai.local_llm", "LocalLLM", "ÃÃÂ¾ÃÂºÃÂ°ÃÂ»ÃÃÂ½ÃÂ°Ã LLM"),
        ]

        for attribute, module_name, class_name, label in modules:
            try:
                module = __import__(module_name, fromlist=[class_name])
                setattr(self, attribute, getattr(module, class_name)(self.brain))
                self.brain.logger.info("Ã¢ %s ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½", label)
            except Exception as error:
                self.brain.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ %s: %s", label, error)

        try:
            from ai.optimization_agents import OptimizationManager
            self.optimization_manager = OptimizationManager(self.brain, self)
            self.brain.logger.info("Ã¢ ÃÃÂ³ÃÂµÃÂ½ÃÃ ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½Ã")
        except Exception as error:
            self.brain.logger.error("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ·ÃÂºÃÂ¸ ÃÂ°ÃÂ³ÃÂµÃÂ½ÃÃÂ¾ÃÂ² ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸: %s", error)

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
                    self.brain.logger.info("ÃÂ ÃÂµÃÂºÃÂ¾ÃÂ¼ÃÂµÃÂ½ÃÂ´ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸: %s", "; ".join(recommendations))

                hud = getattr(self.brain, "hud", None)
                if hud and hasattr(hud, "set_optimization_status"):
                    hud.set_optimization_status(report)

            except Exception as error:
                self.brain.logger.debug("ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÂ°ÃÂ½ÃÂ°ÃÂ»ÃÂ¸ÃÂ·ÃÂ° ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸: %s", error)

        return result

    def optimize_runtime(self, text: str = "") -> Dict:
        """Return a fresh optimization report for CLI, API, or UI callers."""
        return self.get_optimization_report()

    def learn_new_command(self, text: str, category: str) -> Dict:
        if not self.adaptive_ml:
            return {"status": "error", "message": "ÃÃÂ´ÃÂ°ÃÂ¿ÃÃÂ¸ÃÂ²ÃÂ½ÃÃÂ¹ ML ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½"}
        return self.adaptive_ml.add_training_example(text, category)

    def create_alias(self, alias: str, command: str) -> Dict:
        if not self.alias_system:
            return {"status": "error", "message": "ÃÂ¡ÃÂ¸ÃÃÃÂµÃÂ¼ÃÂ° ÃÂ°ÃÂ»ÃÂ¸ÃÂ°ÃÃÂ¾ÃÂ² ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½ÃÂ°"}
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
            return "ÃÃÂ³ÃÂµÃÂ½ÃÃ ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ÃÃÂºÃÂ»ÃÃÃÂµÃÂ½Ã ÃÂ¸ÃÂ»ÃÂ¸ ÃÂ½ÃÂµÃÂ´ÃÂ¾ÃÃÃÃÂ¿ÃÂ½Ã."

        cache = status.get("cache", {})
        return (
            f"ÃÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸Ã: {len(status['agent_names'])} ÃÂ°ÃÂ³ÃÂµÃÂ½ÃÃÂ¾ÃÂ²; "
            f"ÃÃÂµÃÂºÃÂ¾ÃÂ¼ÃÂµÃÂ½ÃÂ´ÃÂ°ÃÃÂ¸ÃÂ¹: {status['recommendation_count']}; "
            f"ÃÂºÃÃ: {cache.get('cache_entries', 0)} ÃÂ·ÃÂ°ÃÂ¿ÃÂ¸ÃÃÂµÃÂ¹ "
            f"(hits={cache.get('hits', 0)}, misses={cache.get('misses', 0)})."
        )

    def get_optimization_report(self) -> Dict:
        if not self.optimization_manager:
            return {"status": "error", "message": "ÃÃÂ³ÃÂµÃÂ½ÃÃ ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ½ÃÂµ ÃÂ·ÃÂ°ÃÂ³ÃÃÃÂ¶ÃÂµÃÂ½Ã", "recommendations": []}
        if not self.brain.config.get("optimization.enabled", True):
            return {"status": "disabled", "message": "ÃÃÂ³ÃÂµÃÂ½ÃÃ ÃÂ¾ÃÂ¿ÃÃÂ¸ÃÂ¼ÃÂ¸ÃÂ·ÃÂ°ÃÃÂ¸ÃÂ¸ ÃÂ¾ÃÃÂºÃÂ»ÃÃÃÂµÃÂ½Ã", "recommendations": []}
        return self.optimization_manager.analyze()

    def analyze_patterns(self) -> List[Dict]:
        if not self.pattern_recognizer or not self.user_profile:
            return []
        return self.pattern_recognizer.analyze_command_history(self.user_profile.command_history)

    def get_greeting(self) -> str:
        if self.user_profile:
            return self.user_profile.get_greeting()
        return "ÃÃÂ´ÃÃÂ°ÃÂ²ÃÃÃÂ²ÃÃÂ¹ÃÃÂµ, ÃÃÃ."
