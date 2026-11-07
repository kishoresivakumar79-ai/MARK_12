"""
Response Generator for MARK 12
Formats output, applies persona, and prepares metadata payloads.
"""
from typing import Dict, Any, Optional

class ResponseGenerator:
    def format_response(self, text: str, agent_name: str = "MARK 12") -> Dict[str, Any]:
        return {
            "agent": agent_name,
            "text": text
        }

global_response_generator = ResponseGenerator()
