"""
System Orchestrator for MARK 12
Coordinates system lifecycle, background workers, and service availability.
"""
from typing import Dict, Any
from task_manager.scheduler import global_scheduler
from task_manager.reminder import global_reminder_system

class SystemOrchestrator:
    def __init__(self):
        self.is_running = False

    def startup(self):
        if self.is_running:
            return
        print("[Orchestrator] Starting MARK 12 subsystems...")
        global_scheduler.start()
        global_reminder_system.start()
        self.is_running = True
        print("[Orchestrator] All subsystems online.")

    def shutdown(self):
        print("[Orchestrator] Shutting down subsystems...")
        global_scheduler.stop()
        global_reminder_system.stop()
        self.is_running = False
        print("[Orchestrator] Subsystems shutdown complete.")

global_orchestrator = SystemOrchestrator()
