"""
Hybrid Memory Retriever for MARK 12
Blends Short-Term working context and Long-Term semantic memories with ranking.
"""
from typing import List, Dict, Any
from ai_engine.memory.short_term import global_short_term_memory
from ai_engine.memory.long_term import global_long_term_memory

class MemoryRetriever:
    def retrieve_relevant_context(self, query: str, max_memories: int = 4) -> str:
        long_term = global_long_term_memory.recall(query, limit=max_memories)
        short_term = global_short_term_memory.get_context_window()

        context_parts = []
        if long_term:
            context_parts.append("### Retrieved Relevant Long-Term Memories:")
            for m in long_term:
                content = m.get("content") or m.get("text", "")
                cat = m.get("category", "info")
                context_parts.append(f"- [{cat.upper()}]: {content}")

        if short_term:
            context_parts.append("\n### Recent Working Memory (Short-Term):")
            for item in short_term[-5:]:
                context_parts.append(f"- {item['role']}: {item['content']}")

        return "\n".join(context_parts)

global_memory_retriever = MemoryRetriever()
