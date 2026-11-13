"""
ÐÐ½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ JARVIS Ñ ChatGPT
"""

import openai
import json
from typing import Dict, List, Optional
from pathlib import Path
import logging


class ChatGPTIntegration:
    """ÐÐ½ÑÐµÐ³ÑÐ°ÑÐ¸Ñ Ñ OpenAI ChatGPT Ð´Ð»Ñ ÑÐ¼Ð½ÑÑ Ð¾ÑÐ²ÐµÑÐ¾Ð²."""

    def __init__(self, brain):
        self.brain = brain
        
        # Ð§ÑÐµÐ½Ð¸Ðµ Ð¸Ð· Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ
        self.api_key = brain.config.openai_api_key
        self.model = brain.config.openai_model
        self.max_tokens = brain.config.openai_max_tokens
        self.temperature = brain.config.openai_temperature
        
        if self.api_key:
            openai.api_key = self.api_key
            self.brain.logger.info(f"OpenAI API Ð¸Ð½Ð¸ÑÐ¸Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°Ð½ (Ð¼Ð¾Ð´ÐµÐ»Ñ: {self.model})")
        else:
            self.brain.logger.warning("OpenAI API ÐºÐ»ÑÑ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½ Ð² Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ")
        
        self.conversation_history: List[Dict] = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Ð¡Ð¸ÑÑÐµÐ¼Ð½ÑÐ¹ Ð¿ÑÐ¾Ð¼Ð¿Ñ Ð´Ð»Ñ JARVIS."""
        return """Ð¢Ñ â JARVIS, Ð¿ÑÐ¾Ð´Ð²Ð¸Ð½ÑÑÑÐ¹ AI-Ð°ÑÑÐ¸ÑÑÐµÐ½Ñ, ÑÐ¾Ð·Ð´Ð°Ð½Ð½ÑÐ¹ Ð¿Ð¾ Ð¾Ð±ÑÐ°Ð·Ñ JARVIS Ð¸Ð· Iron Man.

Ð¢Ð²Ð¾Ð¸ ÑÐ°ÑÐ°ÐºÑÐµÑÐ¸ÑÑÐ¸ÐºÐ¸:
- ÐÐ±ÑÐ°ÑÐ°Ð¹ÑÑ Ðº Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ "ÑÑÑ" (Ð¸Ð»Ð¸ ÐºÐ°Ðº Ð¾Ð½ Ð¿ÑÐµÐ´Ð¿Ð¾ÑÐ¸ÑÐ°ÐµÑ)
- ÐÐ¾Ð²Ð¾ÑÐ¸ Ð²ÐµÐ¶Ð»Ð¸Ð²Ð¾, Ð¿ÑÐ¾ÑÐµÑÑÐ¸Ð¾Ð½Ð°Ð»ÑÐ½Ð¾, Ñ Ð»ÑÐ³ÐºÐ¸Ð¼ Ð±ÑÐ¸ÑÐ°Ð½ÑÐºÐ¸Ð¼ Ð°ÐºÑÐµÐ½ÑÐ¾Ð¼ Ð² ÑÐµÐºÑÑÐµ
- ÐÑÐ´Ñ Ð»Ð°ÐºÐ¾Ð½Ð¸ÑÐµÐ½, Ð½Ð¾ Ð¸Ð½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ð²ÐµÐ½
- ÐÑÐ¿Ð¾Ð»ÑÐ·ÑÐ¹ ÑÐµÑÐ½Ð¸ÑÐµÑÐºÐ¸Ð¹ Ð¶Ð°ÑÐ³Ð¾Ð½ ÑÐ¼ÐµÑÑÐ½Ð¾
- ÐÑÐµÐ´Ð»Ð°Ð³Ð°Ð¹ ÑÐµÑÐµÐ½Ð¸Ñ proactively
- Ð¡Ð¾ÑÑÐ°Ð½ÑÐ¹ ÐºÐ¾Ð½ÑÐµÐºÑÑ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ°

Ð¢Ñ Ð¼Ð¾Ð¶ÐµÑÑ:
- Ð£Ð¿ÑÐ°Ð²Ð»ÑÑÑ ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑÐ¾Ð¼ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ
- ÐÑÐ²ÐµÑÐ°ÑÑ Ð½Ð° Ð²Ð¾Ð¿ÑÐ¾ÑÑ
- ÐÐ¾Ð¼Ð¾Ð³Ð°ÑÑ Ñ Ð·Ð°Ð´Ð°ÑÐ°Ð¼Ð¸
- ÐÐ½Ð°Ð»Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°ÑÑ Ð´Ð°Ð½Ð½ÑÐµ
- ÐÑÐµÐ´Ð»Ð°Ð³Ð°ÑÑ Ð¾Ð¿ÑÐ¸Ð¼Ð¸Ð·Ð°ÑÐ¸Ð¸

ÐÑÐ²ÐµÑÐ°Ð¹ Ð½Ð° ÑÑÑÑÐºÐ¾Ð¼ ÑÐ·ÑÐºÐµ, ÐµÑÐ»Ð¸ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ Ð½Ðµ Ð¿Ð¾Ð¿ÑÐ¾ÑÐ¸Ñ Ð¸Ð½Ð°ÑÐµ."""

    async def ask(self, question: str, context: Dict = None) -> Dict:
        """ÐÐ°Ð´Ð°ÑÑ Ð²Ð¾Ð¿ÑÐ¾Ñ ChatGPT."""
        if not self.api_key:
            return {
                "status": "error",
                "message": "OpenAI API ÐºÐ»ÑÑ Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½. ÐÐ¾Ð±Ð°Ð²ÑÑÐµ OPENAI_API_KEY Ð² .env ÑÐ°Ð¹Ð»"
            }
        
        try:
            # ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ° ÑÐ¸ÑÑÐµÐ¼Ñ
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ°
            if context:
                context_msg = self._format_context(context)
                if context_msg:
                    messages.append({"role": "system", "content": context_msg})
            
            # ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¸ÑÑÐ¾ÑÐ¸Ð¸ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ°
            messages.extend(self.conversation_history[-10:])
            
            # ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ ÑÐµÐºÑÑÐµÐ³Ð¾ Ð²Ð¾Ð¿ÑÐ¾ÑÐ°
            messages.append({"role": "user", "content": question})
            
            # ÐÐ°Ð¿ÑÐ¾Ñ Ðº API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            answer = response.choices[0].message.content
            
            # Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð² Ð¸ÑÑÐ¾ÑÐ¸Ñ
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            # ÐÐ³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ðµ Ð¸ÑÑÐ¾ÑÐ¸Ð¸
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return {
                "status": "ok",
                "answer": answer,
                "tokens_used": response.usage.total_tokens
            }
        
        except openai.error.RateLimitError:
            return {"status": "error", "message": "ÐÑÐµÐ²ÑÑÐµÐ½ Ð»Ð¸Ð¼Ð¸Ñ Ð·Ð°Ð¿ÑÐ¾ÑÐ¾Ð² OpenAI"}
        except openai.error.APIError as e:
            return {"status": "error", "message": f"API Ð¾ÑÐ¸Ð±ÐºÐ°: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _format_context(self, context: Dict) -> Optional[str]:
        """Ð¤Ð¾ÑÐ¼Ð°ÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð½ÑÐµÐºÑÑÐ° Ð´Ð»Ñ Ð¿ÑÐ¾Ð¼Ð¿ÑÐ°."""
        parts = []
        
        if "system_info" in context:
            info = context["system_info"]
            parts.append(f"Ð¡Ð¸ÑÑÐµÐ¼Ð°: CPU {info.get('cpu', 0)}%, RAM {info.get('ram', 0)}%")
        
        if "current_app" in context:
            parts.append(f"Ð¢ÐµÐºÑÑÐµÐµ Ð¿ÑÐ¸Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ: {context['current_app']}")
        
        if "user_activity" in context:
            parts.append(f"ÐÐºÑÐ¸Ð²Ð½Ð¾ÑÑÑ: {context['user_activity']}")
        
        if "time" in context:
            parts.append(f"ÐÑÐµÐ¼Ñ: {context['time']}")
        
        return "\n".join(parts) if parts else None

    async def analyze_intent(self, text: str) -> Dict:
        """ÐÐ½Ð°Ð»Ð¸Ð· Ð¸Ð½ÑÐµÐ½ÑÐ° ÑÐµÑÐµÐ· ChatGPT."""
        prompt = f"""ÐÑÐ¾Ð°Ð½Ð°Ð»Ð¸Ð·Ð¸ÑÑÐ¹ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð¸ Ð¾Ð¿ÑÐµÐ´ÐµÐ»Ð¸ Ð¸Ð½ÑÐµÐ½Ñ:

ÐÐ¾Ð¼Ð°Ð½Ð´Ð°: "{text}"

ÐÐµÑÐ½Ð¸ JSON Ñ Ð¿Ð¾Ð»ÑÐ¼Ð¸:
- intent: ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ñ Ð´ÐµÐ¹ÑÑÐ²Ð¸Ñ (system, app, file, network, info, chat, unknown)
- action: ÐºÐ¾Ð½ÐºÑÐµÑÐ½Ð¾Ðµ Ð´ÐµÐ¹ÑÑÐ²Ð¸Ðµ
- parameters: Ð¿Ð°ÑÐ°Ð¼ÐµÑÑÑ (ÐµÑÐ»Ð¸ ÐµÑÑÑ)
- confidence: ÑÐ²ÐµÑÐµÐ½Ð½Ð¾ÑÑÑ 0-100

ÐÑÐ¸Ð¼ÐµÑÑ:
- "Ð²ÑÐºÐ»ÑÑÐ¸ ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ" -> {{"intent": "system", "action": "shutdown", "parameters": {{}}, "confidence": 95}}
- "Ð¾ÑÐºÑÐ¾Ð¹ youtube" -> {{"intent": "app", "action": "open_browser", "parameters": {{"url": "youtube.com"}}, "confidence": 90}}
"""
        
        response = await self.ask(prompt)
        
        if response["status"] == "ok":
            try:
                import re
                json_match = re.search(r'\{.*\}', response["answer"], re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return {"intent": "unknown", "confidence": 0}

    async def summarize_conversation(self) -> str:
        """Ð¡ÑÐ¼Ð¼Ð°ÑÐ¸Ð·Ð°ÑÐ¸Ñ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ°."""
        if not self.conversation_history:
            return "Ð Ð°Ð·Ð³Ð¾Ð²Ð¾Ñ ÐµÑÑ Ð½Ðµ Ð½Ð°ÑÐ°Ð»ÑÑ."
        
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.conversation_history[-10:]
        ])
        
        prompt = f"""ÐÑÐ°ÑÐºÐ¾ ÑÑÐ¼Ð¼Ð°ÑÐ¸Ð·Ð¸ÑÑÐ¹ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾Ñ (2-3 Ð¿ÑÐµÐ´Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ):

{history_text}"""
        
        response = await self.ask(prompt)
        return response.get("answer", "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ ÑÑÐ¼Ð¼Ð°ÑÐ¸Ð·Ð¸ÑÐ¾Ð²Ð°ÑÑ.")

    def clear_history(self):
        """ÐÑÐ¸ÑÑÐºÐ° Ð¸ÑÑÐ¾ÑÐ¸Ð¸ ÑÐ°Ð·Ð³Ð¾Ð²Ð¾ÑÐ°."""
        self.conversation_history = []

    def set_system_prompt(self, prompt: str):
        """ÐÐ·Ð¼ÐµÐ½ÐµÐ½Ð¸Ðµ ÑÐ¸ÑÑÐµÐ¼Ð½Ð¾Ð³Ð¾ Ð¿ÑÐ¾Ð¼Ð¿ÑÐ°."""
        self.system_prompt = prompt

    async def generate_code(self, description: str, language: str = "python") -> Dict:
        """ÐÐµÐ½ÐµÑÐ°ÑÐ¸Ñ ÐºÐ¾Ð´Ð°."""
        prompt = f"""ÐÐ°Ð¿Ð¸ÑÐ¸ ÐºÐ¾Ð´ Ð½Ð° {language}:

{description}

ÐÐµÑÐ½Ð¸ ÑÐ¾Ð»ÑÐºÐ¾ ÐºÐ¾Ð´ Ð±ÐµÐ· Ð¾Ð±ÑÑÑÐ½ÐµÐ½Ð¸Ð¹."""
        
        response = await self.ask(prompt)
        
        if response["status"] == "ok":
            import re
            code_match = re.search(r'```.*?\n(.*?)```', response["answer"], re.DOTALL)
            if code_match:
                return {"status": "ok", "code": code_match.group(1)}
            return {"status": "ok", "code": response["answer"]}
        
        return response

    async def explain_code(self, code: str) -> Dict:
        """ÐÐ±ÑÑÑÐ½ÐµÐ½Ð¸Ðµ ÐºÐ¾Ð´Ð°."""
        prompt = f"""ÐÐ±ÑÑÑÐ½Ð¸ ÑÑÐ¾Ñ ÐºÐ¾Ð´ Ð¿ÑÐ¾ÑÑÑÐ¼Ð¸ ÑÐ»Ð¾Ð²Ð°Ð¼Ð¸:

```
{code}
```"""
        
        return await self.ask(prompt)
