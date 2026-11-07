"""
Database Initializer Script for MARK 12
Initializes tables and seeds initial configuration, memory, and task hierarchy.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.repository import Repository
from database.connection import get_db

def initialize_database():
    print("[MARK 12] Initializing SQLite database...")
    Repository.init_tables()

    # Seed default admin user
    with get_db() as conn:
        user = conn.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
        if not user:
            conn.execute(
                "INSERT INTO users (id, username, password_hash, role) VALUES ('admin-01', 'admin', 'pbkdf2:sha256:default_admin_hash', 'admin')"
            )
            print("  Created default admin user.")

    # Seed initial memories
    memories = Repository.search_memories(limit=10)
    if len(memories) == 0:
        Repository.add_memory(
            category="system",
            content="MARK 12 is a personal AI operating system created to manage daily activities, computer operations, multi-agent workflows, and document intelligence.",
            importance=5,
            tags="system,core,purpose"
        )
        Repository.add_memory(
            category="user_preference",
            content="User prefers concise answers, dark futuristic UI themes, and autonomous execution with safety confirmation on destructive actions.",
            importance=4,
            tags="preferences,ui,safety"
        )
        print("  Seeded core memories.")

    # Seed initial tasks
    tasks = Repository.get_tasks()
    if len(tasks) == 0:
        parent_id = Repository.create_task(
            title="Initialize MARK 12 System",
            description="Verify all 10 core modules: Speech, LLM Brain, Automation, Memory, Vision, Documents, Agents.",
            priority=1,
            tags="system,setup"
        )
        Repository.create_task(
            title="Explore Multi-Agent Collaboration",
            description="Test planner agent delegating tasks to research and document agents.",
            priority=2,
            parent_id=parent_id,
            tags="agents,testing"
        )
        Repository.create_task(
            title="Configure Voice & Desktop Automation Whitelist",
            description="Set authorized applications and speech synthesizer voice preferences.",
            priority=3,
            parent_id=parent_id,
            tags="voice,automation"
        )
        print("  Seeded task hierarchy.")

    print("[MARK 12] Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
