"""
Personal Agent for MARK 12
Manages daily personal affairs, priority reminders, schedules, and habit tracking.
"""
from typing import Dict, Any, List
from task_manager.task_service import global_task_service
from ai_engine.memory.long_term import global_long_term_memory

class PersonalAgent:
    def __init__(self):
        self.name = "Personal"
        self.role = "Daily Life Assistant & Schedule Custodian"

    def execute_daily_briefing(self) -> Dict[str, Any]:
        tasks = global_task_service.get_priority_tasks()
        pending = [t for t in tasks if t.get("status") == "pending"]
        memories = global_long_term_memory.recall("important priorities", limit=3)

        return {
            "agent": self.name,
            "status": "completed",
            "pending_tasks_count": len(pending),
            "urgent_tasks": pending[:3],
            "relevant_memories": memories,
            "briefing": f"Good day. You have {len(pending)} pending tasks. Highest priority: {pending[0]['title'] if pending else 'None'}."
        }

global_personal_agent = PersonalAgent()
