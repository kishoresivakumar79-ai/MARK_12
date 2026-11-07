"""
Application Controller for MARK 12
Launches, manages, and terminates desktop applications via subprocess.
"""
import subprocess
import os
import platform
from typing import Dict, Any
from automation.permission_manager import global_permission_manager
from database.repository import Repository

class AppController:
    def launch_app(self, app_name: str) -> Dict[str, Any]:
        norm = app_name.lower().strip()
        if not global_permission_manager.is_app_allowed(norm):
            Repository.log_automation("launch_app", app_name, "DENIED", "Application not in security whitelist")
            return {"success": False, "message": f"Application '{app_name}' is not in the approved whitelist."}

        is_win = platform.system() == "Windows"
        cmd = []

        if norm in ["notepad", "note"]:
            cmd = ["notepad.exe"] if is_win else ["gedit"]
        elif norm in ["calculator", "calc"]:
            cmd = ["calc.exe"] if is_win else ["gnome-calculator"]
        elif norm in ["explorer", "files"]:
            cmd = ["explorer.exe"] if is_win else ["nautilus"]
        elif norm in ["vscode", "code"]:
            cmd = ["code"]
        elif norm in ["terminal", "cmd", "powershell"]:
            cmd = ["cmd.exe", "/c", "start"] if is_win else ["x-terminal-emulator"]
        else:
            cmd = [norm]

        try:
            if is_win:
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen(cmd)
            Repository.log_automation("launch_app", app_name, "SUCCESS", f"Command executed: {cmd}")
            return {"success": True, "message": f"Successfully launched {app_name}."}
        except Exception as e:
            Repository.log_automation("launch_app", app_name, "FAILED", str(e))
            return {"success": False, "message": f"Failed to launch {app_name}: {str(e)}"}

global_app_controller = AppController()
