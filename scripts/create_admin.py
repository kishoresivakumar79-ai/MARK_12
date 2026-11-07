"""
Admin user generation script for MARK 12
"""
import sys
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.connection import get_db

def create_admin(username="admin", password="password123"):
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (id, username, password_hash, role) VALUES ('admin-01', ?, ?, 'admin')",
            (username, pwd_hash)
        )
    print(f"[MARK 12] Admin user '{username}' created successfully.")

if __name__ == "__main__":
    u = sys.argv[1] if len(sys.argv) > 1 else "admin"
    p = sys.argv[2] if len(sys.argv) > 2 else "password123"
    create_admin(u, p)
