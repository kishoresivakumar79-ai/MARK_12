"""
Command Parser for MARK 12
Implements Dictionary Data Structure for O(1) fast key-value intent and command dispatch.
"""
from typing import Dict, Any, Callable, Optional, Tuple
import re

class CommandParser:
    def __init__(self):
        # Dictionary: Exact and prefix command lookup table (O(1))
        self.command_registry: Dict[str, Dict[str, Any]] = {
            "open notepad": {"intent": "automation_launch", "target": "notepad"},
            "launch notepad": {"intent": "automation_launch", "target": "notepad"},
            "open calculator": {"intent": "automation_launch", "target": "calculator"},
            "launch calc": {"intent": "automation_launch", "target": "calculator"},
            "open browser": {"intent": "automation_launch", "target": "browser"},
            "take screenshot": {"intent": "automation_screenshot", "target": "screen"},
            "capture screen": {"intent": "automation_screenshot", "target": "screen"},
            "system status": {"intent": "system_telemetry", "target": "system"},
            "diagnostics": {"intent": "system_telemetry", "target": "system"},
            "daily briefing": {"intent": "personal_briefing", "target": "tasks"},
            "undo": {"intent": "system_undo", "target": "history"}
        }

    def parse(self, text: str) -> Tuple[str, Optional[str]]:
        """Parses natural language and dispatches against O(1) dictionary command table."""
        clean = text.lower().strip()

        # 1. Exact match in command dictionary
        if clean in self.command_registry:
            entry = self.command_registry[clean]
            return entry["intent"], entry["target"]

        # 2. Pattern matching for open/launch
        open_match = re.match(r'^(?:open|launch|start|run)\s+([a-zA-Z0-9_\-\.\s]+)$', clean)
        if open_match:
            app_target = open_match.group(1).strip()
            return "automation_launch", app_target

        # 3. Search pattern
        search_match = re.match(r'^(?:search|google|find)\s+(?:for\s+)?(.+)$', clean)
        if search_match:
            query = search_match.group(1).strip()
            return "browser_search", query

        # 4. Remember pattern
        remember_match = re.match(r'^(?:remember\s+(?:that\s+)?|save\s+memory\s+:?\s*)(.+)$', clean)
        if remember_match:
            memory_fact = remember_match.group(1).strip()
            return "memory_save", memory_fact

        # 5. Task pattern
        task_match = re.match(r'^(?:create\s+task|add\s+task|todo\s*:?\s*)(.+)$', clean)
        if task_match:
            task_title = task_match.group(1).strip()
            return "task_create", task_title

        return "conversational", None

global_command_parser = CommandParser()
