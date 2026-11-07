"""
Document Agent for MARK 12
Summarizes, queries, and formats structured documents and reports.
"""
from typing import Dict, Any, List
from ai_engine.llm.model_manager import global_model_manager
from ai_engine.llm.prompt_templates import DOCUMENT_AGENT_PROMPT

class DocumentAgent:
    def __init__(self):
        self.name = "Document"
        self.role = "Document Synthesis & Report Generation"

    def execute(self, content_or_prompt: str, document_chunks: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = (
            f"{DOCUMENT_AGENT_PROMPT}\n\n"
            f"Document Objective: {content_or_prompt}\n\n"
            f"Synthesize this into a structured markdown document."
        )
        doc_result = global_model_manager.generate_response(prompt)
        return {
            "agent": self.name,
            "status": "completed",
            "document": doc_result
        }

global_document_agent = DocumentAgent()
