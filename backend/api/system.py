"""
System Telemetry API Endpoint for MARK 12
GET /api/system/status - Retrieve full system telemetry and health stats
GET /api/system/settings - Retrieve runtime settings
POST /api/system/settings - Update runtime settings
"""
from typing import Dict, Any
from automation.system_monitor import global_system_monitor
from core.context_manager import global_context
from agents.agent_manager import global_agent_manager

def get_telemetry() -> Dict[str, Any]:
    stats = global_system_monitor.get_system_telemetry()
    stats["active_agents"] = global_agent_manager.active_agents
    return stats

try:
    from fastapi import APIRouter
    from database.schemas import SystemStatusResponse
    router = APIRouter(prefix="/api/system", tags=["System"])

    @router.get("/status")
    async def status_endpoint():
        return get_telemetry()

    @router.get("/settings")
    async def get_settings_endpoint():
        return global_context.get_all_preferences()

    @router.post("/settings")
    async def update_settings_endpoint(settings_update: Dict[str, Any]):
        for k, v in settings_update.items():
            global_context.set_preference(k, v)
        return {"status": "updated", "preferences": global_context.get_all_preferences()}
except ImportError:
    router = None
