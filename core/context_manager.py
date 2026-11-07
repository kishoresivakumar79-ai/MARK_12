"""
Context Manager for MARK 12
Implements core data structures:
- List: Conversation history
- Stack: Undo operations (LIFO)
- HashMap: User preferences and runtime cache (O(1))
- Set: Duplicate command and intent detection (O(1))
"""
from typing import Any, Dict, List, Optional, Set
from collections import deque
import time

class UndoAction:
    def __init__(self, action_type: str, rollback_fn, description: str, data: Any = None):
        self.action_type = action_type
        self.rollback_fn = rollback_fn
        self.description = description
        self.data = data
        self.timestamp = time.time()

    def undo(self):
        if callable(self.rollback_fn):
            return self.rollback_fn(self.data)
        return False

class ContextManager:
    def __init__(self, max_history: int = 100):
        # 1. List: Sequential conversation history
        self._history: List[Dict[str, Any]] = []
        self._max_history = max_history

        # 2. Stack: Undo operations for user actions (LIFO)
        self._undo_stack: List[UndoAction] = []

        # 3. HashMap: User preferences and runtime states
        self._preferences: Dict[str, Any] = {
            "assistant_name": "MARK 12",
            "personality": "professional_concise",
            "voice_gender": "male",
            "tts_speed": 1.0,
            "theme": "futuristic_dark",
            "safety_level": "standard",
            "auto_execute_code": False
        }

        # 4. Set: Duplicate command detection (Prevents accidental re-triggers)
        self._recent_command_hashes: Set[str] = set()
        self._command_timestamps: Dict[str, float] = {}

    # --- List Operations (History) ---
    def add_message(self, role: str, content: str, **kwargs):
        entry = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
            **kwargs
        }
        self._history.append(entry)
        if len(self._history) > self._max_history:
            self._history.pop(0)

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit:
            return self._history[-limit:]
        return list(self._history)

    def clear_history(self):
        self._history.clear()

    # --- Stack Operations (Undo) ---
    def push_undo(self, action_type: str, rollback_fn, description: str, data: Any = None):
        action = UndoAction(action_type, rollback_fn, description, data)
        self._undo_stack.append(action)

    def pop_undo(self) -> Optional[UndoAction]:
        if self._undo_stack:
            return self._undo_stack.pop()
        return None

    def execute_undo(self) -> Dict[str, Any]:
        action = self.pop_undo()
        if not action:
            return {"success": False, "message": "Nothing to undo."}
        try:
            res = action.undo()
            return {"success": True, "message": f"Undid: {action.description}", "result": res}
        except Exception as e:
            return {"success": False, "message": f"Undo failed: {str(e)}"}

    # --- HashMap Operations (Preferences) ---
    def set_preference(self, key: str, value: Any):
        self._preferences[key] = value

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self._preferences.get(key, default)

    def get_all_preferences(self) -> Dict[str, Any]:
        return dict(self._preferences)

    # --- Set Operations (Duplicate Command Detection) ---
    def is_duplicate_command(self, command: str, window_seconds: float = 3.0) -> bool:
        cmd_norm = command.strip().lower()
        now = time.time()
        
        # Clean expired hashes
        expired = [c for c, t in self._command_timestamps.items() if now - t > window_seconds]
        for c in expired:
            self._command_timestamps.pop(c, None)
            self._recent_command_hashes.discard(c)

        if cmd_norm in self._recent_command_hashes:
            return True

        self._recent_command_hashes.add(cmd_norm)
        self._command_timestamps[cmd_norm] = now
        return False

# Global context manager instance
global_context = ContextManager()
