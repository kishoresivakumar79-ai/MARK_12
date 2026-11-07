"""
Memory Summarizer for MARK 12
Distills long dialog transcripts into high-density declarative knowledge facts.
"""
from typing import List, Dict, Any

class MemorySummarizer:
    @staticmethod
    def extract_facts(dialog_text: str) -> List[str]:
        facts = []
        lines = dialog_text.split("\n")
        for line in lines:
            line_str = line.strip()
            # Simple heuristic detection for explicit preferences or facts
            lower = line_str.lower()
            if any(phrase in lower for phrase in ["my name is", "i prefer", "i like", "i work on", "remember that", "don't forget"]):
                facts.append(line_str)
        return facts

    @staticmethod
    def summarize_conversation(messages: List[Dict[str, Any]]) -> str:
        if not messages:
            return "No messages to summarize."
        user_msgs = [m["content"] for m in messages if m.get("role") == "user" or m.get("sender") == "user"]
        summary = f"Summary of {len(messages)} interactions. User discussed: {', '.join(user_msgs[-3:])}"
        return summary
