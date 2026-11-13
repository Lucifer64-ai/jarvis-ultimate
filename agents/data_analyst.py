"""
JARVIS - Data Analyst Agent
          AI
"""

from .base_agent import BaseAgent
from .ai_service import get_ai_service
from typing import Dict, Optional, Any


class DataAnalystAgent(BaseAgent):
    """   ."""

    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description=" , , ,     AI"
        )
        self.capabilities = [
            " CSV/Excel ",
            " ",
            "   ",
            "   ",
            "  (pandas)",
            "  ()",
            "   ",
            "AI-  "
        ]
        self.ai_service = get_ai_service()

    def can_handle(self, task: str) -> bool:
        """,     ."""
        keywords = [
            "", "", "", "", "",
            "csv", "excel", "pandas", "numpy", " ", "sql",
            " ", "", ""
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
        result = self.ai_service.generate_code(
            task=task,
            agent_type="data_analyst",
            context=context,
            language="python"
        )

        if result['status'] == 'success':
            #      AI
            files = self.ai_service.parse_code_blocks(result['code'])

            return {
                'status': 'success',
                'type': 'ai_generated',
                'message': f'AI    : {task}',
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
            return self._create_visualization(task, context)
        elif "" in task.lower() or "" in task.lower():
            return self._create_report(task, context)
        else:
            return self._analyze_data(task, context)

    def _create_visualization(self, task: str, context: Dict) -> Dict[str, Any]:
        """  ."""
        return {
            'status': 'success',
            'type': 'visualization',
            'message': f' : {task}',
            'files': {
                'visualization.py': self._generate_visualization_code(task)
            }
        }

    def _create_report(self, task: str, context: Dict) -> Dict[str, Any]:
        """ ."""
        return {
            'status': 'success',
            'type': 'report',
            'message': f' : {task}',
            'files': {
                'report.py': self._generate_report_code(task)
            }
        }

    def _analyze_data(self, task: str, context: Dict) -> Dict[str, Any]:
        """ ."""
        return {
            'status': 'success',
            'type': 'analysis',
            'message': f' : {task}',
            'files': {
                'analysis.py': self._generate_analysis_code(task)
            }
        }

    def _generate_visualization_code(self, task: str) -> str:
        """   ."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
 JARVIS Data Analyst Agent
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_visualization():
    """  ."""
    #  
    data = {{
        'category': ['A', 'B', 'C', 'D'],
        'values': [10, 25, 15, 30]
    }}

    df = pd.DataFrame(data)

    #  
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='category', y='values')
    plt.title('{task}')
    plt.xlabel('')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('chart.png', dpi=300)
    plt.show()

    print("   chart.png")


if __name__ == "__main__":
    create_visualization()
"""

    def _generate_report_code(self, task: str) -> str:
        """   ."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
 JARVIS Data Analyst Agent
"""

import pandas as pd
from datetime import datetime


def generate_report():
    """ ."""
    print(f"JARVIS Data Analyst Agent:  ")
    print(f": {task}")
    print(f": {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")

    #  
    data = {{
        'metric': ['', '', ''],
        'value': [1000, 150, 15.5]
    }}

    df = pd.DataFrame(data)

    #  
    report_file = 'report.csv'
    df.to_csv(report_file, index=False, encoding='utf-8')

    print(f"\n   {{report_file}}")
    print("\n:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    generate_report()
"""

    def _generate_analysis_code(self, task: str) -> str:
        """   ."""
        return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{task}
 JARVIS Data Analyst Agent
"""

import pandas as pd
import numpy as np


def analyze_data():
    """ ."""
    print("JARVIS Data Analyst Agent:  ")
    print(f": {task}")

    #  
    data = np.random.randn(100, 3)
    df = pd.DataFrame(data, columns=['A', 'B', 'C'])

    #  
    print("\n===  ===")
    print(df.describe())

    # 
    print("\n===  ===")
    print(df.corr())

    #  
    df.to_csv('analysis_results.csv', index=False)
    print("\n   analysis_results.csv")


if __name__ == "__main__":
    analyze_data()
"""
