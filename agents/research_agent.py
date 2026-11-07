"""
Research Agent for MARK 12
Conducts structured comparisons, technical analysis, and synthesizes findings.
"""
from typing import Dict, Any
from ai_engine.llm.model_manager import global_model_manager
from ai_engine.llm.prompt_templates import RESEARCH_AGENT_PROMPT

class ResearchAgent:
    def __init__(self):
        self.name = "Research"
        self.role = "Data Investigation & Knowledge Synthesis"

    def execute(self, query: str) -> Dict[str, Any]:
        prompt = (
            f"{RESEARCH_AGENT_PROMPT}\n\n"
            f"Research Subject: {query}\n\n"
            f"Provide an analytical synthesis covering:\n"
            f"1. Key Findings & Core Overview\n"
            f"2. Comparative Analysis / Tradeoffs\n"
            f"3. Strategic Recommendation"
        )
        report = global_model_manager.generate_response(prompt)
        return {
            "agent": self.name,
            "status": "completed",
            "query": query,
            "report": report
        }

global_research_agent = ResearchAgent()
