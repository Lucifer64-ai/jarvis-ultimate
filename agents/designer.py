"""
JARVIS - Designer Agent
   UI/UX ,    
"""

from .base_agent import BaseAgent
from .ai_service import get_ai_service
from typing import Dict, Optional, Any


class DesignerAgent(BaseAgent):
    """  UI/UX ."""

    def __init__(self):
        super().__init__(
            name="Designer",
            description="UI/UX , ,    AI"
        )
        self.capabilities = [
            " UI ",
            " CSS ",
            " ",
            "  ",
            " SVG ",
            " ",
            "AI- "
        ]
        self.ai_service = get_ai_service()

    def can_handle(self, task: str) -> bool:
        """,     ."""
        keywords = [
            "", "", "ui", "ux", "", "", "",
            "svg", "", "", "", "", " "
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in keywords)

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """   ."""
        context = context or {}

        #   AI  
        if self.ai_service.client:
            return self._execute_with_ai(task, context)
        else:
            # Fallback    AI 
            return self._execute_with_templates(task, context)

    def _execute_with_ai(self, task: str, context: Dict) -> Dict[str, Any]:
        """    AI."""
        result = self.ai_service.generate_code(
            task=task,
            agent_type="designer",
            context=context,
            language="css"
        )

        if result['status'] == 'success':
            #      AI
            files = self.ai_service.parse_code_blocks(result['code'])

            return {
                'status': 'success',
                'type': 'ai_generated',
                'message': f'AI  : {task}',
                'files': files,
                'tokens_used': result.get('tokens_used', 0),
                'model': result.get('model', 'unknown')
            }
        else:
            #  AI ,  
            return self._execute_with_templates(task, context)

    def _execute_with_templates(self, task: str, context: Dict) -> Dict[str, Any]:
        """     (fallback)."""
        if "" in task.lower() or "" in task.lower():
            return self._create_color_scheme(task, context)
        elif "svg" in task.lower() or "" in task.lower():
            return self._create_svg(task, context)
        else:
            return self._create_ui_design(task, context)

    def _create_color_scheme(self, task: str, context: Dict) -> Dict[str, Any]:
        """  ."""
        return {
            'status': 'success',
            'type': 'color_scheme',
            'message': f'  : {task}',
            'files': {
                'colors.css': self._generate_color_scheme(task)
            }
        }

    def _create_svg(self, task: str, context: Dict) -> Dict[str, Any]:
        """ SVG ."""
        return {
            'status': 'success',
            'type': 'svg',
            'message': f' SVG: {task}',
            'files': {
                'icon.svg': self._generate_svg_icon(task)
            }
        }

    def _create_ui_design(self, task: str, context: Dict) -> Dict[str, Any]:
        """ UI ."""
        return {
            'status': 'success',
            'type': 'ui_design',
            'message': f' UI : {task}',
            'files': {
                'design.css': self._generate_ui_styles(task),
                'layout.html': self._generate_layout(task)
            }
        }

    def _generate_color_scheme(self, task: str) -> str:
        """  ."""
        return f"""/*  : {task} */
/*  JARVIS Designer Agent */

:root {{
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --background-color: #f5f7fa;
    --text-color: #333333;
    --text-light: #666666;
    --border-color: #e0e0e0;
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --error-color: #f44336;
}}

/*   */
[data-theme="dark"] {{
    --primary-color: #7c8cf5;
    --secondary-color: #8b5fbf;
    --accent-color: #f5a8fc;
    --background-color: #1a1a1a;
    --text-color: #ffffff;
    --text-light: #b0b0b0;
    --border-color: #333333;
}}

/*   */
body {{
    background-color: var(--background-color);
    color: var(--text-color);
}}

.primary {{
    color: var(--primary-color);
}}

.secondary {{
    color: var(--secondary-color);
}}

.accent {{
    color: var(--accent-color);
}}
"""

    def _generate_svg_icon(self, task: str) -> str:
        """ SVG ."""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <!-- {task} -->
    <!--  JARVIS Designer Agent -->

    <!--  -->
    <circle cx="32" cy="32" r="30" fill="#667eea" opacity="0.1"/>

    <!--  -->
    <path d="M32 16 L40 28 L32 24 L24 28 Z" fill="#667eea"/>
    <circle cx="32" cy="36" r="8" fill="#764ba2"/>

    <!--  -->
    <text x="32" y="56" font-family="Arial" font-size="8" fill="#333" text-anchor="middle">
        JARVIS
    </text>
</svg>
"""

    def _generate_ui_styles(self, task: str) -> str:
        """ UI ."""
        return f"""/* UI : {task} */
/*  JARVIS Designer Agent */

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}}

.card {{
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
}}

h1, h2, h3 {{
    color: #667eea;
    margin-bottom: 1rem;
}}

.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
}}

.btn:hover {{
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}}

.input {{
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}}

.input:focus {{
    outline: none;
    border-color: #667eea;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}}

@media (max-width: 768px) {{
    .container {{
        padding: 1rem;
    }}

    .grid {{
        grid-template-columns: 1fr;
    }}
}}
"""

    def _generate_layout(self, task: str) -> str:
        """ layout."""
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{task}</title>
    <link rel="stylesheet" href="design.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{task}</h1>
            <p>UI   JARVIS Designer Agent</p>
        </header>

        <main class="grid">
            <div class="card">
                <h2> 1</h2>
                <p> </p>
                <button class="btn"></button>
            </div>

            <div class="card">
                <h2> 2</h2>
                <p> </p>
                <button class="btn"></button>
            </div>

            <div class="card">
                <h2> 3</h2>
                <p> </p>
                <button class="btn"></button>
            </div>
        </main>
    </div>
</body>
</html>
"""
