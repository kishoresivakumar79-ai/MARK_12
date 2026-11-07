"""
Wake Word Detection Engine for MARK 12
Listens for activation keywords ('Mark 12', 'Mark', 'Hey Mark', 'Jarvis') to trigger active listening.
"""
import re
from typing import Callable, Optional

class WakeWordDetector:
    def __init__(self, wake_words=None):
        self.wake_words = wake_words or [
            "mark 12", "mark", "hey mark 12", "hey mark", "ok mark 12", "ok mark", "jarvis"
        ]
        self._pattern = re.compile(r'\b(' + '|'.join(re.escape(w) for w in self.wake_words) + r')\b', re.IGNORECASE)

    def contains_wake_word(self, text: str) -> bool:
        if not text:
            return False
        return bool(self._pattern.search(text))

    def strip_wake_word(self, text: str) -> str:
        cleaned = self._pattern.sub("", text).strip()
        # Clean leading punctuation
        cleaned = re.sub(r'^[,\s!]+', '', cleaned)
        return cleaned

global_wake_word_detector = WakeWordDetector()
