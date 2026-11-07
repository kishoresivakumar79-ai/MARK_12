"""
Memory API Endpoint for MARK 12
GET /api/memory - Retrieve and search memories
POST /api/memory - Save explicit memory
DELETE /api/memory/{id} - Delete memory
"""
from typing import Dict, Any, Optional, List
from ai_engine.memory.long_term import global_long_term_memory
from database.repository import Repository

def list_or_search_memories(query: str = "", category: str = None) -> List[Dict[str, Any]]:
    if query:
        return global_long_term_memory.recall(query, category=category)
    return global_long_term_memory.list_all()

def save_memory(data: Dict[str, Any]) -> Dict[str, Any]:
    content = data.get("content", "")
    category = data.get("category", "general")
    importance = int(data.get("importance", 3))
    tags = data.get("tags", "")
    mem_id = global_long_term_memory.remember(content, category=category, importance=importance, tags=tags)
    return {"id": mem_id, "content": content, "status": "saved"}

def delete_memory(memory_id: str) -> Dict[str, Any]:
    success = global_long_term_memory.forget(memory_id)
    return {"id": memory_id, "deleted": success}

try:
    from fastapi import APIRouter
    from database.schemas import MemoryCreate
    router = APIRouter(prefix="/api/memory", tags=["Memory"])

    @router.get("")
    async def get_memories_endpoint(query: str = "", category: Optional[str] = None):
        return list_or_search_memories(query, category)

    @router.post("")
    async def create_memory_endpoint(req: MemoryCreate):
        return save_memory(req.model_dump() if hasattr(req, "model_dump") else req.dict())

    @router.delete("/{memory_id}")
    async def delete_memory_endpoint(memory_id: str):
        return delete_memory(memory_id)
except ImportError:
    router = None
