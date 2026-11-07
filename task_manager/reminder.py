"""
Scheduler and Reminders for MARK 12
Evaluates upcoming deadlines, overdue tasks, and dispatches reminder notifications.
"""
import time
import threading
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
from database.repository import Repository

class TaskReminderSystem:
    def __init__(self, check_interval_seconds: int = 30):
        self.check_interval = check_interval_seconds
        self.listeners: List[Callable[[Dict[str, Any]], None]] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._notified_tasks = set()

    def add_listener(self, callback: Callable[[Dict[str, Any]], None]):
        self.listeners.append(callback)

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            try:
                self.check_reminders()
            except Exception as e:
                print(f"[ReminderSystem Error] {e}")
            time.sleep(self.check_interval)

    def check_reminders(self) -> List[Dict[str, Any]]:
        tasks = Repository.get_tasks(status="pending")
        now_str = datetime.utcnow().strftime("%Y-%m-%d")
        triggered = []

        for task in tasks:
            due = task.get("due_date")
            task_id = task.get("id")
            if due and task_id not in self._notified_tasks:
                if due <= now_str:
                    triggered.append(task)
                    self._notified_tasks.add(task_id)
                    for listener in self.listeners:
                        try:
                            listener(task)
                        except Exception:
                            pass
        return triggered

global_reminder_system = TaskReminderSystem()
