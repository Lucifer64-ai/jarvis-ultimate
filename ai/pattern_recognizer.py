"""
Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ðµ Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð² JARVIS
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import re


class PatternRecognizer:
    """Ð Ð°ÑÐ¿Ð¾Ð·Ð½Ð°Ð²Ð°Ð½Ð¸Ðµ Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð² Ð² Ð¿Ð¾Ð²ÐµÐ´ÐµÐ½Ð¸Ð¸ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ."""

    def __init__(self, brain):
        self.brain = brain
        self.patterns_file = Path("data/patterns.json")
        self.patterns_file.parent.mkdir(exist_ok=True)
        self.patterns: Dict = self._load_patterns()
        self.suggestions: List[Dict] = []

    def _load_patterns(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð²."""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "recurring_commands": {},
            "time_based_patterns": {},
            "sequence_patterns": {},
            "learned_automations": []
        }

    def _save_patterns(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð²."""
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)

    def analyze_command_history(self, history: List[Dict]) -> List[Dict]:
        """ÐÐ½Ð°Ð»Ð¸Ð· Ð¸ÑÑÐ¾ÑÐ¸Ð¸ ÐºÐ¾Ð¼Ð°Ð½Ð´ Ð´Ð»Ñ Ð²ÑÑÐ²Ð»ÐµÐ½Ð¸Ñ Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð²."""
        suggestions = []
        
        # 1. ÐÐ¾Ð²ÑÐ¾ÑÑÑÑÐ¸ÐµÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð² Ð¾Ð´Ð½Ð¾ Ð²ÑÐµÐ¼Ñ
        time_patterns = self._detect_time_patterns(history)
        suggestions.extend(time_patterns)
        
        # 2. ÐÐ¾ÑÐ»ÐµÐ´Ð¾Ð²Ð°ÑÐµÐ»ÑÐ½Ð¾ÑÑÐ¸ ÐºÐ¾Ð¼Ð°Ð½Ð´
        sequence_patterns = self._detect_sequence_patterns(history)
        suggestions.extend(sequence_patterns)
        
        # 3. Ð§Ð°ÑÑÐ¾ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÐµÐ¼ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ
        frequent_commands = self._detect_frequent_commands(history)
        suggestions.extend(frequent_commands)
        
        self.suggestions = suggestions
        self._save_patterns()
        
        return suggestions

    def _detect_time_patterns(self, history: List[Dict]) -> List[Dict]:
        """ÐÐ±Ð½Ð°ÑÑÐ¶ÐµÐ½Ð¸Ðµ Ð²ÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð¿Ð°ÑÑÐµÑÐ½Ð¾Ð²."""
        suggestions = []
        time_groups = defaultdict(list)
        
        for entry in history:
            try:
                dt = datetime.fromisoformat(entry["timestamp"])
                hour = dt.hour
                minute = dt.minute
                # ÐÑÑÐ¿Ð¿Ð¸ÑÑÐµÐ¼ Ð¿Ð¾ 15-Ð¼Ð¸Ð½ÑÑÐ½ÑÐ¼ Ð¸Ð½ÑÐµÑÐ²Ð°Ð»Ð°Ð¼
                time_slot = f"{hour:02d}:{(minute // 15) * 15:02d}"
                time_groups[time_slot].append(entry["command"])
            except:
                continue
        
        # ÐÑÐµÐ¼ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ, ÐºÐ¾ÑÐ¾ÑÑÐµ Ð¿Ð¾Ð²ÑÐ¾ÑÑÑÑÑÑ Ð² Ð¾Ð´Ð½Ð¾ Ð²ÑÐµÐ¼Ñ
        for time_slot, commands in time_groups.items():
            command_counts = defaultdict(int)
            for cmd in commands:
                command_counts[cmd] += 1
            
            for cmd, count in command_counts.items():
                if count >= 3:  # ÐÑÐ»Ð¸ ÐºÐ¾Ð¼Ð°Ð½Ð´Ð° Ð¿Ð¾Ð²ÑÐ¾ÑÑÐµÑÑÑ 3+ ÑÐ°Ð·Ð° Ð² ÑÑÐ¾ Ð²ÑÐµÐ¼Ñ
                    suggestions.append({
                        "type": "time_pattern",
                        "command": cmd,
                        "time": time_slot,
                        "count": count,
                        "suggestion": f"ÐÑ ÑÐ°ÑÑÐ¾ Ð³Ð¾Ð²Ð¾ÑÐ¸ÑÐµ '{cmd}' Ð² {time_slot}. Ð¡Ð¾Ð·Ð´Ð°ÑÑ Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸ÑÐµÑÐºÐ¾Ðµ ÑÐ°ÑÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ?",
                        "action": "create_schedule"
                    })
        
        return suggestions

    def _detect_sequence_patterns(self, history: List[Dict]) -> List[Dict]:
        """ÐÐ±Ð½Ð°ÑÑÐ¶ÐµÐ½Ð¸Ðµ Ð¿Ð¾ÑÐ»ÐµÐ´Ð¾Ð²Ð°ÑÐµÐ»ÑÐ½Ð¾ÑÑÐµÐ¹ ÐºÐ¾Ð¼Ð°Ð½Ð´."""
        suggestions = []
        
        if len(history) < 3:
            return suggestions
        
        # ÐÑÐµÐ¼ Ð¿Ð¾Ð²ÑÐ¾ÑÑÑÑÐ¸ÐµÑÑ Ð¿Ð¾ÑÐ»ÐµÐ´Ð¾Ð²Ð°ÑÐµÐ»ÑÐ½Ð¾ÑÑÐ¸ Ð¸Ð· 2-3 ÐºÐ¾Ð¼Ð°Ð½Ð´
        for seq_length in [2, 3]:
            sequences = defaultdict(int)
            
            for i in range(len(history) - seq_length + 1):
                seq = tuple(entry["command"] for entry in history[i:i+seq_length])
                sequences[seq] += 1
            
            for seq, count in sequences.items():
                if count >= 2:  # ÐÑÐ»Ð¸ Ð¿Ð¾ÑÐ»ÐµÐ´Ð¾Ð²Ð°ÑÐµÐ»ÑÐ½Ð¾ÑÑÑ Ð¿Ð¾Ð²ÑÐ¾ÑÑÐµÑÑÑ 2+ ÑÐ°Ð·Ð°
                    suggestions.append({
                        "type": "sequence_pattern",
                        "sequence": list(seq),
                        "count": count,
                        "suggestion": f"ÐÑ ÑÐ°ÑÑÐ¾ Ð²ÑÐ¿Ð¾Ð»Ð½ÑÐµÑÐµ Ð¿Ð¾ÑÐ»ÐµÐ´Ð¾Ð²Ð°ÑÐµÐ»ÑÐ½Ð¾ÑÑÑ: {' â '.join(seq)}. Ð¡Ð¾Ð·Ð´Ð°ÑÑ Ð¼Ð°ÐºÑÐ¾Ñ?",
                        "action": "create_macro"
                    })
        
        return suggestions

    def _detect_frequent_commands(self, history: List[Dict]) -> List[Dict]:
        """ÐÐ±Ð½Ð°ÑÑÐ¶ÐµÐ½Ð¸Ðµ ÑÐ°ÑÑÐ¾ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÐµÐ¼ÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´."""
        suggestions = []
        command_counts = defaultdict(int)
        
        for entry in history:
            command_counts[entry["command"]] += 1
        
        for cmd, count in command_counts.items():
            if count >= 10:  # ÐÑÐ»Ð¸ ÐºÐ¾Ð¼Ð°Ð½Ð´Ð° Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÐµÑÑÑ 10+ ÑÐ°Ð·
                suggestions.append({
                    "type": "frequent_command",
                    "command": cmd,
                    "count": count,
                    "suggestion": f"ÐÐ¾Ð¼Ð°Ð½Ð´Ð° '{cmd}' Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÐµÑÑÑ Ð¾ÑÐµÐ½Ñ ÑÐ°ÑÑÐ¾ ({count} ÑÐ°Ð·). Ð¡Ð¾Ð·Ð´Ð°ÑÑ Ð±ÑÑÑÑÑÐ¹ Ð°Ð»Ð¸Ð°Ñ?",
                    "action": "create_alias"
                })
        
        return suggestions

    def get_suggestions(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ ÑÐµÐºÑÑÐ¸Ñ Ð¿ÑÐµÐ´Ð»Ð¾Ð¶ÐµÐ½Ð¸Ð¹."""
        return self.suggestions

    def accept_suggestion(self, index: int) -> Dict:
        """ÐÑÐ¸Ð½ÑÑÐ¸Ðµ Ð¿ÑÐµÐ´Ð»Ð¾Ð¶ÐµÐ½Ð¸Ñ."""
        if index >= len(self.suggestions):
            return {"status": "error", "message": "ÐÑÐµÐ´Ð»Ð¾Ð¶ÐµÐ½Ð¸Ðµ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð¾"}
        
        suggestion = self.suggestions[index]
        action = suggestion["action"]
        
        if action == "create_schedule":
            # Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ ÑÐ°ÑÐ¿Ð¸ÑÐ°Ð½Ð¸Ñ
            return {
                "status": "ok",
                "message": f"Ð Ð°ÑÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ ÑÐ¾Ð·Ð´Ð°Ð½Ð¾ Ð´Ð»Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ '{suggestion['command']}' Ð² {suggestion['time']}",
                "action_taken": "schedule_created"
            }
        
        elif action == "create_macro":
            # Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð¼Ð°ÐºÑÐ¾ÑÐ°
            return {
                "status": "ok",
                "message": f"ÐÐ°ÐºÑÐ¾Ñ ÑÐ¾Ð·Ð´Ð°Ð½ Ð´Ð»Ñ Ð¿Ð¾ÑÐ»ÐµÐ´Ð¾Ð²Ð°ÑÐµÐ»ÑÐ½Ð¾ÑÑÐ¸: {' â '.join(suggestion['sequence'])}",
                "action_taken": "macro_created"
            }
        
        elif action == "create_alias":
            # Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð°Ð»Ð¸Ð°ÑÐ°
            return {
                "status": "ok",
                "message": f"ÐÑÐµÐ´Ð»Ð¾Ð¶Ð¸ÑÐµ Ð°Ð»Ð¸Ð°Ñ Ð´Ð»Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ '{suggestion['command']}'",
                "action_taken": "alias_pending"
            }
        
        return {"status": "error", "message": "ÐÐµÐ¸Ð·Ð²ÐµÑÑÐ½Ð¾Ðµ Ð´ÐµÐ¹ÑÑÐ²Ð¸Ðµ"}

    def learn_automation(self, trigger: str, action: str) -> Dict:
        """ÐÐ±ÑÑÐµÐ½Ð¸Ðµ Ð½Ð¾Ð²Ð¾Ð¹ Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸Ð·Ð°ÑÐ¸Ð¸."""
        automation = {
            "trigger": trigger,
            "action": action,
            "created": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        self.patterns["learned_automations"].append(automation)
        self._save_patterns()
        
        return {
            "status": "ok",
            "message": f"ÐÐ²ÑÐ¾Ð¼Ð°ÑÐ¸Ð·Ð°ÑÐ¸Ñ Ð¾Ð±ÑÑÐµÐ½Ð°: '{trigger}' â '{action}'"
        }

    def get_learned_automations(self) -> List[Dict]:
        """ÐÐ¾Ð»ÑÑÐµÐ½Ð¸Ðµ Ð¾Ð±ÑÑÐµÐ½Ð½ÑÑ Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸Ð·Ð°ÑÐ¸Ð¹."""
        return self.patterns.get("learned_automations", [])
