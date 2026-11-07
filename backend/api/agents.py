"""
Multi-Agent API Endpoint for MARK 12
GET /api/agents - Agent status and graph topology
POST /api/agents/workflow - Execute multi-agent objective
"""
from typing import Dict, Any, List
from agents.agent_manager import global_agent_manager

def get_agent_overview() -> Dict[str, Any]:
    return {
        "agents": global_agent_manager.get_agents_status(),
        "graph_topology": global_agent_manager.graph.get_topology()
    }

def run_agent_workflow(objective: str) -> Dict[str, Any]:
    return global_agent_manager.execute_multi_agent_workflow(objective)

try:
    from fastapi import APIRouter
    from pydantic import BaseModel
    router = APIRouter(prefix="/api/agents", tags=["Agents"])

    class WorkflowRequest(BaseModel):
        objective: str

    @router.get("")
    async def get_agents_endpoint():
        return get_agent_overview()

    @router.post("/workflow")
    async def run_workflow_endpoint(req: WorkflowRequest):
        return run_agent_workflow(req.objective)
except ImportError:
    router = None
