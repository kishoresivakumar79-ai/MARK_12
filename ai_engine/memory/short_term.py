"""
Short Term Memory Engine for MARK 12
Manages real-time working memory and immediate conversation context window.
"""
from typing import List, Dict, Any
from collections import deque

class ShortTermMemory:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def add(self, role: str, content: str, intent: str = None):
        self.buffer.append({
            "role": role,
            "content": content,
            "intent": intent
        })

    def get_context_window(self) -> List[Dict[str, Any]]:
        return list(self.buffer)

    def get_formatted_context(self) -> str:
        lines = []
        for item in self.buffer:
            lines.append(f"{item['role'].upper()}: {item['content']}")
        return "\n".join(lines)

    def clear(self):
        self.buffer.clear()

global_short_term_memory = ShortTermMemory()
