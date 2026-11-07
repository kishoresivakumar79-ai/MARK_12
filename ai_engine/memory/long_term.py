"""
Long Term Memory Engine for MARK 12
Stores, categorizes, and persists facts, preferences, and important conversation outcomes.
"""
from typing import List, Dict, Any, Optional
from database.repository import Repository
from ai_engine.memory.vector_memory import global_vector_memory

class LongTermMemory:
    def remember(self, content: str, category: str = "general", importance: int = 3, tags: str = "") -> str:
        # Store in relational database
        mem_id = Repository.add_memory(
            category=category,
            content=content,
            importance=importance,
            tags=tags
        )
        # Store vector representation for semantic search
        global_vector_memory.add_vector(
            item_id=mem_id,
            text=content,
            metadata={"category": category, "importance": importance, "tags": tags}
        )
        return mem_id

    def recall(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        # Vector semantic retrieval
        similar_items = global_vector_memory.search_similar(query, top_k=limit)
        results = []
        for item in similar_items:
            results.append({
                "id": item["id"],
                "content": item["text"],
                "category": item["metadata"].get("category", "general"),
                "importance": item["metadata"].get("importance", 3),
                "score": item["score"]
            })
        
        # If vector score is low, fallback to SQL keyword search
        if not results or (results and results[0]["score"] < 0.3):
            sql_results = Repository.search_memories(query=query, category=category, limit=limit)
            return sql_results
            
        return results

    def forget(self, memory_id: str) -> bool:
        global_vector_memory.delete_vector(memory_id)
        return Repository.delete_memory(memory_id)

    def list_all(self, limit: int = 50) -> List[Dict[str, Any]]:
        return Repository.search_memories(limit=limit)

global_long_term_memory = LongTermMemory()
