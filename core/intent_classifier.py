"""
Intent Classifier for MARK 12
Categorizes user requests across conversational, automation, coding, document, task, and vision.
"""
import re
from typing import Dict, Any

class IntentClassifier:
    def classify(self, text: str) -> str:
        t = text.lower().strip()

        # Multi-agent triggers
        if any(w in t for w in ["compare", "research", "workflow", "multi-agent", "delegate to"]):
            return "multi_agent_workflow"

        # Automation triggers
        if any(t.startswith(w) for w in ["open ", "launch ", "start ", "close ", "screenshot", "system status"]):
            return "computer_automation"

        # Coding triggers
        if any(w in t for w in ["code", "function", "debug", "python", "script", "algorithm", "implement"]):
            return "coding"

        # Memory triggers
        if any(w in t for w in ["remember", "recall", "memory", "what did i say about"]):
            return "memory"

        # Task triggers
        if any(w in t for w in ["task", "todo", "schedule", "deadline", "reminder"]):
            return "task"

        # Document triggers
        if any(w in t for w in ["document", "pdf", "summarize file", "read doc"]):
            return "document"

        # Vision triggers
        if any(w in t for w in ["image", "picture", "photo", "camera", "webcam", "look at"]):
            return "vision"

        return "chat"

global_intent_classifier = IntentClassifier()
