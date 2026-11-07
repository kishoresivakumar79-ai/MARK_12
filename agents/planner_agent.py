"""
Planner Agent for MARK 12
Decomposes user objectives into an executable Directed Acyclic Graph (DAG) of sub-agent tasks.
"""
import re
from typing import List, Dict, Any
from ai_engine.llm.model_manager import global_model_manager
from ai_engine.llm.prompt_templates import PLANNER_PROMPT

class PlannerAgent:
    def __init__(self):
        self.name = "Planner"
        self.role = "Workflow Architect & Task Decomposer"

    def plan_workflow(self, objective: str) -> List[Dict[str, Any]]:
        """Deconstructs complex goals into a sequential or branched workflow."""
        lower = objective.lower()
        steps = []

        # Heuristic detection for common complex operations
        if "course" in lower or "compare" in lower or "research" in lower:
            steps.append({
                "step": 1,
                "agent": "Research",
                "action": "Gather and compare data",
                "description": f"Perform comprehensive comparison on: {objective}"
            })
            if "save" in lower or "document" in lower or "report" in lower:
                steps.append({
                    "step": 2,
                    "agent": "Document",
                    "action": "Generate structured document",
                    "description": "Synthesize findings into an executive report format"
                })
            steps.append({
                "step": len(steps) + 1,
                "agent": "Personal",
                "action": "Log memory and schedule",
                "description": "Store comparison results into long-term memory"
            })
            return steps

        if any(term in lower for term in ["build", "write code", "create app", "script", "program"]):
            steps.append({
                "step": 1,
                "agent": "Planner",
                "action": "Architecture breakdown",
                "description": "Define component boundaries, file layout, and specifications"
            })
            steps.append({
                "step": 2,
                "agent": "Coding",
                "action": "Synthesize code",
                "description": "Generate clean, typed Python/JS code implementation"
            })
            steps.append({
                "step": 3,
                "agent": "Automation",
                "action": "Save to workspace",
                "description": "Write code to storage/generated_code folder"
            })
            return steps

        # Default multi-step DAG
        steps.append({
            "step": 1,
            "agent": "Planner",
            "action": "Analyze requirement",
            "description": f"Examine parameters for '{objective}'"
        })
        steps.append({
            "step": 2,
            "agent": "Research" if "find" in lower else "Coding",
            "action": "Execute core logic",
            "description": "Synthesize targeted answer and solutions"
        })
        return steps

global_planner_agent = PlannerAgent()
