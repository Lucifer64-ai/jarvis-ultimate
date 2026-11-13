"""
JARVIS - AI Service for Agents
Сервис для интеграции OpenAI API с агентами
"""

import os
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI


class AgentAIService:
    """AI-сервис для генерации кода агентами."""

    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            self.logger.warning("OpenAI API key not found. AI features disabled.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            self.logger.info("AI Service initialized for agents")

    def generate_code(
        self,
        task: str,
        agent_type: str,
        context: Optional[Dict] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """Генерация кода с помощью AI."""
        if not self.client:
            return {
                'status': 'error',
                'message': 'AI service not available. Please set OPENAI_API_KEY.'
            }

        try:
            # Формируем промпт в зависимости от типа агента
            prompt = self._build_prompt(task, agent_type, context, language)

            # Вызываем OpenAI API
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(agent_type)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
            )

            generated_code = response.choices[0].message.content

            return {
                'status': 'success',
                'code': generated_code,
                'tokens_used': response.usage.total_tokens,
                'model': response.model
            }

        except Exception as e:
            self.logger.error(f"AI generation error: {e}")
            return {
                'status': 'error',
                'message': f'AI generation failed: {str(e)}'
            }

    def _build_prompt(
        self,
        task: str,
        agent_type: str,
        context: Optional[Dict],
        language: str
    ) -> str:
        """Построение промпта для AI."""
        context_str = ""
        if context:
            context_str = f"\n\nКонтекст: {context}"

        if agent_type == "web_developer":
            return f"""Создай веб-приложение или сайт для задачи: {task}{context_str}

Требования:
- Используй современный HTML5, CSS3, JavaScript
- Адаптивный дизайн
- Чистый и читаемый код
- Комментарии на русском языке

Верни полный код файлов в формате:
```filename
код
```"""

        elif agent_type == "programmer":
            return f"""Напиши код на {language} для задачи: {task}{context_str}

Требования:
- Чистый и эффективный код
- Обработка ошибок
- Документация и комментарии
- Следуй best practices для {language}

Верни полный код в формате:
```{language}
код
```"""

        elif agent_type == "data_analyst":
            return f"""Создай код для анализа данных: {task}{context_str}

Требования:
- Используй pandas, numpy, matplotlib/seaborn
- Статистический анализ
- Визуализация данных
- Чистый и документированный код

Верни полный код в формате:
```python
код
```"""

        else:
            return f"""Выполни задачу: {task}{context_str}

Верни результат в формате кода."""

    def _get_system_prompt(self, agent_type: str) -> str:
        """Получить системный промпт для агента."""
        prompts = {
            "web_developer": "Ты - опытный веб-разработчик. Создавай современные, адаптивные и красивые веб-приложения. Используй лучшие практики HTML, CSS и JavaScript.",
            "programmer": "Ты - профессиональный программист. Пиши чистый, эффективный и хорошо документированный код. Следуй принципам SOLID и DRY.",
            "data_analyst": "Ты - эксперт по анализу данных. Создавай код для обработки, анализа и визуализации данных с использованием pandas, numpy и matplotlib."
        }
        return prompts.get(agent_type, "Ты - полезный AI-ассистент.")

    def parse_code_blocks(self, text: str) -> Dict[str, str]:
        """Извлечение блоков кода из ответа AI."""
        import re

        files = {}
        # Паттерн для поиска блоков кода: ```filename\nкод\n```
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

        for i, (lang, code) in enumerate(matches):
            filename = f"file_{i+1}.{lang or 'txt'}"
            files[filename] = code.strip()

        # Если не найдено блоков с именами, возвращаем весь текст как один файл
        if not files:
            files['generated_code.txt'] = text

        return files


# Глобальный экземпляр для использования в агентах
_ai_service_instance = None

def get_ai_service() -> AgentAIService:
    """Получить глобальный экземпляр AI-сервиса."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AgentAIService()
    return _ai_service_instance
