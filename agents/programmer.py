"""
JARVIS - Programmer Agent
         AI
"""

from .base_agent import BaseAgent
from .ai_service import get_ai_service
from typing import Dict, Optional, Any


class ProgrammerAgent(BaseAgent):
    """   ."""

    def __init__(self):
        super().__init__(
            name="Programmer",
            description="   Python, JavaScript, C++, Java     AI"
        )
        self.capabilities = [
            " Python ",
            " JavaScript/TypeScript",
            " C++ ",
            " Java ",
            " SQL ",
            "  ",
            " ",
            " ",
            "AI- "
        ]
        self.ai_service = get_ai_service()

    def can_handle(self, task: str) -> bool:
        """,     ."""
        keywords = [
            "", "", "", "python", "javascript", "c++", "java",
            "", "", "", " ", "",
            "", "sql", " "
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in keywords)

    def execute_task(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """    ."""
        context = context or {}

        #   AI  
        if self.ai_service.client:
            return self._execute_with_ai(task, context)
        else:
            # Fallback    AI 
            return self._execute_with_templates(task, context)

    def _execute_with_ai(self, task: str, context: Dict) -> Dict[str, Any]:
        """    AI."""
        #   
        language = self._detect_language(task)

        result = self.ai_service.generate_code(
            task=task,
            agent_type="programmer",
            context=context,
            language=language
        )

        if result['status'] == 'success':
            #      AI
            files = self.ai_service.parse_code_blocks(result['code'])

            return {
                'status': 'success',
                'type': 'ai_generated',
                'message': f'AI  : {task}',
                'files': files,
                'language': language,
                'tokens_used': result.get('tokens_used', 0),
                'model': result.get('model', 'unknown')
            }
        else:
            #  AI ,  
            return self._execute_with_templates(task, context)

    def _execute_with_templates(self, task: str, context: Dict) -> Dict[str, Any]:
        """     (fallback)."""
        #   
        if "python" in task.lower():
            return self._create_python(task, context)
        elif "javascript" in task.lower() or "js" in task.lower():
            return self._create_javascript(task, context)
        elif "sql" in task.lower() or "" in task.lower():
            return self._create_sql(task, context)
        else:
            return self._create_generic_code(task, context)

    def _detect_language(self, task: str) -> str:
        """    ."""
        task_lower = task.lower()

        if "python" in task_lower:
            return "python"
        elif "javascript" in task_lower or "js" in task_lower:
            return "javascript"
        elif "typescript" in task_lower or "ts" in task_lower:
            return "typescript"
        elif "c++" in task_lower or "cpp" in task_lower:
            return "cpp"
        elif "java" in task_lower:
            return "java"
        elif "sql" in task_lower or "" in task_lower:
            return "sql"
        else:
            return "python"  #  

    def _create_python(self, task: str, context: Dict) -> Dict[str, Any]:
        """ Python ."""
        return {
            'status': 'success',
            'type': 'python_code',
            'message': f' Python : {task}',
            'files': {
                'main.py': self._generate_python_template(task)
            }
        }

    def _create_javascript(self, task: str, context: Dict) -> Dict[str, Any]:
        """ JavaScript ."""
        return {
            'status': 'success',
            'type': 'javascript_code',
            'message': f' JavaScript : {task}',
            'files': {
                'script.js': self._generate_javascript_template(task)
            }
        }

    def _create_sql(self, task: str, context: Dict) -> Dict[str, Any]:
        """ SQL ."""
        return {
            'status': 'success',
            'type': 'sql_query',
            'message': f' SQL : {task}',
            'files': {
                'query.sql': self._generate_sql_template(task)
            }
        }

    def _create_generic_code(self, task: str, context: Dict) -> Dict[str, Any]:
        """  ."""
        return {
            'status': 'success',
            'type': 'generic_code',
            'message': f' : {task}',
            'files': {
                'code.txt': self._generate_generic_template(task)
            }
        }

    def _generate_python_template(self, task: str) -> str:
        """ Python ."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
 JARVIS Programmer Agent
"""

import sys
from typing import List, Dict, Optional


def main():
    """ ."""
    print("JARVIS Programmer Agent:  ")
    print(": {task}")

    #    
    pass


if __name__ == "__main__":
    main()
"""

    def _generate_javascript_template(self, task: str) -> str:
        """ JavaScript ."""
        return f"""// {task}
//  JARVIS Programmer Agent

'use strict';

class TaskExecutor {{
    constructor() {{
        this.task = '{task}';
        console.log('JARVIS Programmer Agent: ');
    }}

    execute() {{
        console.log(` : ${{this.task}}`);
        //    
    }}
}}

// 
const executor = new TaskExecutor();
executor.execute();
"""

    def _generate_sql_template(self, task: str) -> str:
        """ SQL ."""
        return f"""-- {task}
--  JARVIS Programmer Agent

--  SELECT 
SELECT *
FROM users
WHERE active = true
ORDER BY created_at DESC
LIMIT 100;

--  INSERT 
INSERT INTO tasks (name, description, status)
VALUES ('{task}', '  ', 'pending');

--  UPDATE 
UPDATE tasks
SET status = 'completed',
    updated_at = NOW()
WHERE id = 1;
"""

    def _generate_generic_template(self, task: str) -> str:
        """  ."""
        return f"""// {task}
//  JARVIS Programmer Agent

//     
//     

function main() {{
    console.log('JARVIS Programmer Agent');
    console.log(': {task}');
}}

main();
"""
