"""
Repository Layer for MARK 12
Provides database queries and transactions using standard SQLite3.
"""
import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from database.connection import get_db

class Repository:
    @staticmethod
    def init_tables():
        """Create database tables if they do not exist."""
        from database.models import CREATE_TABLES_SQL
        with get_db() as conn:
            conn.executescript(CREATE_TABLES_SQL)

    # --- Conversation & Messages ---
    @staticmethod
    def get_or_create_conversation(conv_id: Optional[str] = None, title: str = "Main Session") -> str:
        with get_db() as conn:
            if conv_id:
                row = conn.execute("SELECT id FROM conversations WHERE id = ?", (conv_id,)).fetchone()
                if row:
                    return row["id"]
            new_id = conv_id or str(uuid.uuid4())
            conn.execute(
                "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                (new_id, title)
            )
            return new_id

    @staticmethod
    def add_message(conv_id: str, sender: str, content: str, intent: str = None, agent: str = None, audio_path: str = None):
        Repository.get_or_create_conversation(conv_id)
        with get_db() as conn:
            msg_id = str(uuid.uuid4())
            conn.execute(
                """INSERT INTO messages (id, conversation_id, sender, content, audio_path, intent, agent_used, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (msg_id, conv_id, sender, content, audio_path, intent, agent)
            )
            conn.execute("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (conv_id,))
            return msg_id

    @staticmethod
    def get_conversation_history(conv_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC LIMIT ?",
                (conv_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

    # --- Memory Operations ---
    @staticmethod
    def add_memory(category: str, content: str, importance: int = 3, tags: str = "", vector_id: str = None) -> str:
        with get_db() as conn:
            mem_id = str(uuid.uuid4())
            conn.execute(
                """INSERT INTO memories (id, category, content, importance, vector_id, tags, created_at, last_accessed)
                   VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                (mem_id, category, content, importance, vector_id, tags)
            )
            return mem_id

    @staticmethod
    def search_memories(query: str = "", category: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        with get_db() as conn:
            if query and category:
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE category = ? AND (content LIKE ? OR tags LIKE ?) ORDER BY importance DESC, created_at DESC LIMIT ?",
                    (category, f"%{query}%", f"%{query}%", limit)
                )
            elif query:
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE content LIKE ? OR tags LIKE ? ORDER BY importance DESC, created_at DESC LIMIT ?",
                    (f"%{query}%", f"%{query}%", limit)
                )
            elif category:
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE category = ? ORDER BY importance DESC, created_at DESC LIMIT ?",
                    (category, limit)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM memories ORDER BY importance DESC, created_at DESC LIMIT ?",
                    (limit,)
                )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def delete_memory(memory_id: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            return cursor.rowcount > 0

    # --- Task Management ---
    @staticmethod
    def create_task(title: str, description: str = "", priority: int = 3, parent_id: Optional[str] = None, due_date: Optional[str] = None, tags: str = "") -> str:
        with get_db() as conn:
            task_id = str(uuid.uuid4())
            conn.execute(
                """INSERT INTO tasks (id, title, description, priority, status, parent_id, due_date, tags, created_at)
                   VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, CURRENT_TIMESTAMP)""",
                (task_id, title, description, priority, parent_id, due_date, tags)
            )
            return task_id

    @staticmethod
    def get_tasks(status: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db() as conn:
            if status:
                cursor = conn.execute("SELECT * FROM tasks WHERE status = ? ORDER BY priority ASC, created_at ASC", (status,))
            else:
                cursor = conn.execute("SELECT * FROM tasks ORDER BY priority ASC, created_at ASC")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def update_task(task_id: str, **kwargs) -> bool:
        if not kwargs:
            return False
        with get_db() as conn:
            fields = []
            values = []
            for k, v in kwargs.items():
                fields.append(f"{k} = ?")
                values.append(v)
            if "status" in kwargs and kwargs["status"] == "completed":
                fields.append("completed_at = CURRENT_TIMESTAMP")
            values.append(task_id)
            query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
            cursor = conn.execute(query, tuple(values))
            return cursor.rowcount > 0

    @staticmethod
    def delete_task(task_id: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    # --- Automation Logs ---
    @staticmethod
    def log_automation(action: str, target: Optional[str], status: str, details: Optional[str] = None):
        with get_db() as conn:
            log_id = str(uuid.uuid4())
            conn.execute(
                """INSERT INTO automation_logs (id, action, target, status, details, timestamp)
                   VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (log_id, action, target, status, details)
            )
            return log_id

    @staticmethod
    def get_automation_logs(limit: int = 50) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM automation_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]
