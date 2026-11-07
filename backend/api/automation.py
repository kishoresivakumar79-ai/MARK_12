"""
Automation API Endpoint for MARK 12
POST /api/automation/execute - Execute system automation
GET /api/automation/logs - Retrieve audit trail
POST /api/automation/screenshot - Capture desktop screen
"""
from typing import Dict, Any, List
from agents.automation_agent import global_automation_agent
from automation.keyboard_mouse import global_input_controller
from database.repository import Repository

def execute_automation(action: str, target: str = "") -> Dict[str, Any]:
    return global_automation_agent.execute_action(action, target)

def get_automation_logs(limit: int = 50) -> List[Dict[str, Any]]:
    return Repository.get_automation_logs(limit=limit)

try:
    from fastapi import APIRouter
    from database.schemas import AutomationCommand
    router = APIRouter(prefix="/api/automation", tags=["Automation"])

    @router.post("/execute")
    async def execute_endpoint(cmd: AutomationCommand):
        action = cmd.action
        target = cmd.target or ""
        return execute_automation(action, target)

    @router.get("/logs")
    async def logs_endpoint(limit: int = 50):
        return get_automation_logs(limit)

    @router.post("/screenshot")
    async def screenshot_endpoint():
        return global_input_controller.take_screenshot()
except ImportError:
    router = None
