"""
Task Management API Endpoint for MARK 12
GET /api/tasks - Retrieve tasks
POST /api/tasks - Create task
PUT /api/tasks/{task_id} - Update task status
DELETE /api/tasks/{task_id} - Delete task
"""
from typing import Dict, Any, Optional, List
from task_manager.task_service import global_task_service

def list_tasks(status: Optional[str] = None, view: str = "flat") -> Any:
    if view == "tree":
        return global_task_service.get_task_tree()
    elif view == "priority":
        return global_task_service.get_priority_tasks()
    return global_task_service.get_all_tasks(status=status)

def create_task(data: Dict[str, Any]) -> Dict[str, Any]:
    return global_task_service.create_task(
        title=data.get("title", "Untitled Task"),
        description=data.get("description", ""),
        priority=int(data.get("priority", 3)),
        parent_id=data.get("parent_id"),
        due_date=data.get("due_date"),
        tags=data.get("tags", "")
    )

def update_task(task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    status = data.get("status")
    if status:
        global_task_service.update_task_status(task_id, status)
    return {"id": task_id, "updated": True}

def delete_task(task_id: str) -> Dict[str, Any]:
    success = global_task_service.delete_task(task_id)
    return {"id": task_id, "deleted": success}

try:
    from fastapi import APIRouter
    from database.schemas import TaskCreate, TaskUpdate
    router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

    @router.get("")
    async def get_tasks_endpoint(status: Optional[str] = None, view: str = "flat"):
        return list_tasks(status=status, view=view)

    @router.post("")
    async def create_task_endpoint(req: TaskCreate):
        return create_task(req.model_dump() if hasattr(req, "model_dump") else req.dict())

    @router.put("/{task_id}")
    async def update_task_endpoint(task_id: str, req: TaskUpdate):
        return update_task(task_id, req.model_dump() if hasattr(req, "model_dump") else req.dict())

    @router.delete("/{task_id}")
    async def delete_task_endpoint(task_id: str):
        return delete_task(task_id)
except ImportError:
    router = None
