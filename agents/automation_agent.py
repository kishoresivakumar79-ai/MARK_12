"""
Automation Agent for MARK 12
Executes authorized computer tasks, system checks, and application operations.
"""
from typing import Dict, Any
from automation.app_controller import global_app_controller
from automation.browser_controller import global_browser_controller
from automation.system_monitor import global_system_monitor
from automation.keyboard_mouse import global_input_controller

class AutomationAgent:
    def __init__(self):
        self.name = "Automation"
        self.role = "Desktop Operations & Execution Specialist"

    def execute_action(self, action: str, target: str = "") -> Dict[str, Any]:
        act = action.lower()
        if "launch" in act or "open" in act:
            return global_app_controller.launch_app(target)
        elif "browse" in act or "search" in act:
            return global_browser_controller.search_web(target)
        elif "screenshot" in act:
            return global_input_controller.take_screenshot()
        elif "system" in act or "status" in act:
            return {"success": True, "telemetry": global_system_monitor.get_system_telemetry()}
        return {"success": False, "message": f"Action '{action}' is unhandled."}

global_automation_agent = AutomationAgent()
