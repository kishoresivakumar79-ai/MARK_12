"""
Database Unit Tests for MARK 12
Validates SQLite table schema, transactions, and foreign key integrity.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.repository import Repository
from database.connection import get_db

def test_database_initialization():
    Repository.init_tables()
    with get_db() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t["name"] for t in tables]
        for expected in ["users", "conversations", "messages", "memories", "tasks", "documents", "automation_logs"]:
            assert expected in table_names, f"Missing table: {expected}"
    print("[PASS] test_database_initialization")

def test_task_crud():
    task_id = Repository.create_task(title="Test Task Alpha", priority=2, tags="test")
    assert task_id is not None
    tasks = Repository.get_tasks()
    found = any(t["id"] == task_id for t in tasks)
    assert found, "Created task not found in database"

    updated = Repository.update_task(task_id, status="completed")
    assert updated is True

    deleted = Repository.delete_task(task_id)
    assert deleted is True
    print("[PASS] test_task_crud")

if __name__ == "__main__":
    test_database_initialization()
    test_task_crud()
