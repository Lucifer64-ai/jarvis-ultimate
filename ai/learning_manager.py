"""
Менеджер обучения JARVIS - координирует все модули обучения
"""

from typing import Dict, List, Optional
from datetime import datetime


class LearningManager:
    """Централизованное управление обучением."""

    def __init__(self, brain):
        self.brain = brain
        
        # Инициализация модулей обучения
        self.adaptive_ml = None
        self.alias_system = None
        self.user_profile = None
        self.pattern_recognizer = None
        self.local_llm = None
        
        self._init_modules()

    def _init_modules(self):
        """Инициализация модулей обучения."""
        try:
            from ai.adaptive_ml import AdaptiveMLEngine
            self.adaptive_ml = AdaptiveMLEngine(self.brain)
            self.brain.logger.info("✓ Адаптивный ML загружен")
        except Exception as e:
            self.brain.logger.error(f"Ошибка загрузки адаптивного ML: {e}")
        
        try:
            from ai.alias_system import AliasSystem
            self.alias_system = AliasSystem(self.brain)
            self.brain.logger.info("✓ Система алиасов загружена")
        except Exception as e:
            self.brain.logger.error(f"Ошибка загрузки системы алиасов: {e}")
        
        try:
            from ai.user_profile import UserProfile
            self.user_profile = UserProfile(self.brain)
            self.brain.logger.info("✓ Профиль пользователя загружен")
        except Exception as e:
            self.brain.logger.error(f"Ошибка загрузки профиля: {e}")
        
        try:
            from ai.pattern_recognizer import PatternRecognizer
            self.pattern_recognizer = PatternRecognizer(self.brain)
            self.brain.logger.info("✓ Распознавание паттернов загружено")
        except Exception as e:
            self.brain.logger.error(f"Ошибка загрузки распознавания паттернов: {e}")
        
        try:
            from ai.local_llm import LocalLLM
            self.local_llm = LocalLLM(self.brain)
            self.brain.logger.info("✓ Локальная LLM загружена")
        except Exception as e:
            self.brain.logger.error(f"Ошибка загрузки локальной LLM: {e}")

    def process_command(self, text: str) -> Dict:
        """Обработка команды с использованием всех модулей обучения."""
        result = {
            "original": text,
            "processed": text,
            "modules_used": []
        }
        
        # 1. Разрешение алиасов
        if self.alias_system:
            resolved = self.alias_system.resolve_alias(text)
            if resolved != text:
                result["processed"] = resolved
                result["alias_resolved"] = True
                result["modules_used"].append("alias_system")
        
        # 2. Классификация через адаптивный ML
        if self.adaptive_ml:
            classification = self.adaptive_ml.predict(result["processed"])
            result["classification"] = classification
            result["modules_used"].append("adaptive_ml")
            
            # Если уверенность низкая — предлагаем обучить
            if classification.get("needs_learning"):
                result["learning_suggestion"] = classification.get("suggestion")
        
        # 3. Логирование в профиль
        if self.user_profile:
            self.user_profile.log_command(text)
            self.user_profile.update_activity()
            result["modules_used"].append("user_profile")
        
        return result

    def learn_new_command(self, text: str, category: str) -> Dict:
        """Обучение новой команде."""
        if not self.adaptive_ml:
            return {"status": "error", "message": "Адаптивный ML не загружен"}
        
        return self.adaptive_ml.add_training_example(text, category)

    def create_alias(self, alias: str, command: str) -> Dict:
        """Создание алиаса."""
        if not self.alias_system:
            return {"status": "error", "message": "Система алиасов не загружена"}
        
        return self.alias_system.add_alias(alias, command)

    def get_learning_status(self) -> Dict:
        """Получение статуса обучения."""
        status = {
            "modules": {},
            "timestamp": datetime.now().isoformat()
        }
        
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
        
        return status

    def analyze_patterns(self) -> List[Dict]:
        """Анализ паттернов в истории команд."""
        if not self.pattern_recognizer or not self.user_profile:
            return []
        
        # Получаем историю из профиля
        history = self.user_profile.command_history
        
        # Анализируем паттерны
        suggestions = self.pattern_recognizer.analyze_command_history(history)
        
        return suggestions

    def get_greeting(self) -> str:
        """Получение персонализированного приветствия."""
        if self.user_profile:
            return self.user_profile.get_greeting()
        return "Здравствуйте, сэр."
