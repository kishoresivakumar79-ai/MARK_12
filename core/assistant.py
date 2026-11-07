"""
MARK 12 Assistant Master Facade
High-level programmatic interface for the entire AI Personal Life Assistant.
"""
from typing import Dict, Any, Optional
from core.brain import global_brain
from core.orchestrator import global_orchestrator
from ai_engine.speech.wake_word import global_wake_word_detector

class Mark12Assistant:
    def __init__(self):
        self.orchestrator = global_orchestrator
        self.brain = global_brain

    def start(self):
        self.orchestrator.startup()

    def stop(self):
        self.orchestrator.shutdown()

    def send_message(self, message: str, conv_id: str = "default", enable_voice: bool = False) -> Dict[str, Any]:
        """Processes text or transcribed voice messages."""
        # Strip wake word if present
        cleaned_text = global_wake_word_detector.strip_wake_word(message)
        return self.brain.process_input(cleaned_text, conv_id=conv_id, enable_voice=enable_voice)

mark_12 = Mark12Assistant()
