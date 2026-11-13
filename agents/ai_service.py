"""
JARVIS - AI Service for Agents
   OpenAI API  
"""

import os
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI


class AgentAIService:
    """AI-    ."""

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
        """    AI."""
        if not self.client:
            return {
                'status': 'error',
                'message': 'AI service not available. Please set OPENAI_API_KEY.'
            }

        try:
            #       
            prompt = self._build_prompt(task, agent_type, context, language)

            #  OpenAI API
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
        """   AI."""
        context_str = ""
        if context:
            context_str = f"\n\n: {context}"

        if agent_type == "web_developer":
            return f""" -    : {task}{context_str}

:
-   HTML5, CSS3, JavaScript
-  
-    
-    

     :
```filename

```"""

        elif agent_type == "programmer":
            return f"""   {language}  : {task}{context_str}

:
-    
-  
-   
-  best practices  {language}

    :
```{language}

```"""

        elif agent_type == "data_analyst":
            return f"""    : {task}{context_str}

:
-  pandas, numpy, matplotlib/seaborn
-  
-  
-    

    :
```python

```"""

        else:
            return f""" : {task}{context_str}

    ."""

    def _get_system_prompt(self, agent_type: str) -> str:
        """    ."""
        prompts = {
            "web_developer": " -  -.  ,    -.    HTML, CSS  JavaScript.",
            "programmer": " -  .  ,     .   SOLID  DRY.",
            "data_analyst": " -    .    ,       pandas, numpy  matplotlib."
        }
        return prompts.get(agent_type, " -  AI-.")

    def parse_code_blocks(self, text: str) -> Dict[str, str]:
        """     AI."""
        import re

        files = {}
        #     : ```filename\n\n```
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

        for i, (lang, code) in enumerate(matches):
            filename = f"file_{i+1}.{lang or 'txt'}"
            files[filename] = code.strip()

        #      ,      
        if not files:
            files['generated_code.txt'] = text

        return files


#      
_ai_service_instance = None

def get_ai_service() -> AgentAIService:
    """   AI-."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AgentAIService()
    return _ai_service_instance
