"""
File Manager for MARK 12
Provides safe file operations inside the project and storage workspaces.
"""
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from database.repository import Repository

BASE_DIR = Path(__file__).resolve().parent.parent

class FileManager:
    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or BASE_DIR

    def list_directory(self, rel_path: str = "") -> List[Dict[str, Any]]:
        target = (self.root_dir / rel_path).resolve()
        if not target.exists():
            return []

        entries = []
        for item in target.iterdir():
            entries.append({
                "name": item.name,
                "is_dir": item.is_dir(),
                "size_bytes": item.stat().st_size if item.is_file() else 0,
                "path": str(item.relative_to(self.root_dir)).replace("\\", "/")
            })
        return entries

    def read_text(self, rel_path: str) -> Optional[str]:
        target = (self.root_dir / rel_path).resolve()
        if not target.is_file():
            return None
        try:
            return target.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None

    def write_text(self, rel_path: str, content: str) -> bool:
        target = (self.root_dir / rel_path).resolve()
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            Repository.log_automation("write_file", str(rel_path), "SUCCESS")
            return True
        except Exception as e:
            Repository.log_automation("write_file", str(rel_path), "FAILED", str(e))
            return False

    def delete_file(self, rel_path: str) -> bool:
        target = (self.root_dir / rel_path).resolve()
        if not target.exists() or not target.is_file():
            return False
        try:
            target.unlink()
            Repository.log_automation("delete_file", str(rel_path), "SUCCESS")
            return True
        except Exception as e:
            Repository.log_automation("delete_file", str(rel_path), "FAILED", str(e))
            return False

global_file_manager = FileManager()
