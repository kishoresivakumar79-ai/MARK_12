"""
Coding Agent for MARK 12
Generates production code, explains algorithms, and resolves bugs.
"""
from typing import Dict, Any
from ai_engine.llm.model_manager import global_model_manager
from ai_engine.llm.prompt_templates import CODING_AGENT_PROMPT

class CodingAgent:
    def __init__(self):
        self.name = "Coding"
        self.role = "Software Engineering & Code Intelligence"

    def execute(self, task_description: str) -> Dict[str, Any]:
        prompt = (
            f"{CODING_AGENT_PROMPT}\n\n"
            f"Software Task: {task_description}\n\n"
            f"Output clean, modular code with comments and type annotations."
        )
        code_result = global_model_manager.generate_response(prompt)
        return {
            "agent": self.name,
            "status": "completed",
            "task": task_description,
            "code_output": code_result
        }

global_coding_agent = CodingAgent()
