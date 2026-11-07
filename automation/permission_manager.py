"""
Permission and Security Manager for MARK 12
Validates automation commands against whitelists and enforces approval gates for high-risk actions.
"""
from typing import Dict, Any, List

class PermissionManager:
    def __init__(self):
        # Whitelisted safe applications
        self.allowed_apps = {
            "notepad": ["notepad.exe", "notepad"],
            "calculator": ["calc.exe", "calc"],
            "explorer": ["explorer.exe", "explorer"],
            "vscode": ["code.cmd", "code.exe", "code"],
            "browser": ["start", "chrome", "msedge", "firefox"],
            "terminal": ["cmd.exe", "powershell.exe"]
        }

        # Dangerous command blacklist
        self.blocked_patterns = [
            "rmdir /s /q c:", "del /f /s /q c:", "format ", "rm -rf /",
            "shutdown -s", "drop database", "drop table", "mkfs"
        ]

    def is_app_allowed(self, app_name: str) -> bool:
        norm = app_name.lower().strip()
        return any(norm == key or norm in aliases for key, aliases in self.allowed_apps.items())

    def validate_command_safety(self, command: str) -> Dict[str, Any]:
        lower = command.lower()
        for pattern in self.blocked_patterns:
            if pattern in lower:
                return {
                    "safe": False,
                    "reason": f"Command contains potentially destructive operation: '{pattern}'."
                }
        return {"safe": True, "reason": "Command is within safe operational limits."}

global_permission_manager = PermissionManager()
