"""
Database and Storage Backup script for MARK 12
"""
import shutil
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "database" / "mark_12.db"
BACKUP_DIR = BASE_DIR / "storage" / "backups"

def run_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"mark_12_db_{timestamp}.db"

    if DB_FILE.exists():
        shutil.copy2(DB_FILE, backup_file)
        print(f"[Backup] Successfully archived database to: {backup_file}")
    else:
        print("[Backup] Database file not found to backup.")

if __name__ == "__main__":
    run_backup()
