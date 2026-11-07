"""
Task Service for MARK 12
Orchestrates task CRUD, priority sorting, hierarchical trees, and status transitions.
"""
from typing import Dict, List, Any, Optional
from database.repository import Repository
from task_manager.priority_manager import TaskPriorityQueue, TaskTree

class TaskService:
    def __init__(self):
        self.priority_queue = TaskPriorityQueue()
        self._refresh_priority_queue()

    def _refresh_priority_queue(self):
        self.priority_queue = TaskPriorityQueue()
        tasks = Repository.get_tasks(status="pending")
        for t in tasks:
            self.priority_queue.push(t["id"], t["priority"], t)

    def create_task(self, title: str, description: str = "", priority: int = 3, parent_id: Optional[str] = None, due_date: Optional[str] = None, tags: str = "") -> Dict[str, Any]:
        task_id = Repository.create_task(
            title=title,
            description=description,
            priority=priority,
            parent_id=parent_id,
            due_date=due_date,
            tags=tags
        )
        self._refresh_priority_queue()
        return {"id": task_id, "title": title, "priority": priority, "status": "pending"}

    def get_all_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        return Repository.get_tasks(status=status)

    def get_priority_tasks(self) -> List[Dict[str, Any]]:
        """Return tasks ordered by urgent priority."""
        self._refresh_priority_queue()
        return self.priority_queue.get_all_sorted()

    def get_task_tree(self) -> List[Dict[str, Any]]:
        """Return hierarchical parent-child task structure."""
        tasks = Repository.get_tasks()
        tree = TaskTree(tasks)
        return tree.get_hierarchy()

    def update_task_status(self, task_id: str, status: str) -> bool:
        res = Repository.update_task(task_id, status=status)
        self._refresh_priority_queue()
        return res

    def delete_task(self, task_id: str) -> bool:
        res = Repository.delete_task(task_id)
        self._refresh_priority_queue()
        return res

global_task_service = TaskService()
