"""
Safety Manager for MARK 12
Enforces operational boundaries and validates external execution requests.
"""
from typing import Dict, Any

class SafetyManager:
    def __init__(self, restricted_mode: bool = False):
        self.restricted_mode = restricted_mode

    def check_operation(self, operation_type: str, details: str = "") -> Dict[str, Any]:
        lower = details.lower()
        if "delete all" in lower or "format" in lower or "shutdown" in lower:
            return {"allowed": False, "reason": "Operation denied by Safety Protocol."}
        return {"allowed": True, "reason": "Operation verified safe."}

global_safety_manager = SafetyManager()
