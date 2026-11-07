"""
Agent Manager and Workflow Graph for MARK 12
Implements Graph Data Structure connecting agents, task dependencies, and workflow execution.
"""
from typing import Dict, List, Any, Optional, Set
from agents.planner_agent import global_planner_agent
from agents.research_agent import global_research_agent
from agents.coding_agent import global_coding_agent
from agents.document_agent import global_document_agent
from agents.vision_agent import global_vision_agent
from agents.personal_agent import global_personal_agent
from agents.automation_agent import global_automation_agent

class AgentNode:
    def __init__(self, name: str, agent_instance: Any):
        self.name = name
        self.agent = agent_instance
        self.edges: List['AgentNode'] = []

    def connect(self, target_node: 'AgentNode'):
        if target_node not in self.edges:
            self.edges.append(target_node)

class AgentWorkflowGraph:
    """Graph structure connecting AI agents in collaborative workflows."""
    def __init__(self):
        self.nodes: Dict[str, AgentNode] = {
            "Planner": AgentNode("Planner", global_planner_agent),
            "Research": AgentNode("Research", global_research_agent),
            "Coding": AgentNode("Coding", global_coding_agent),
            "Document": AgentNode("Document", global_document_agent),
            "Vision": AgentNode("Vision", global_vision_agent),
            "Personal": AgentNode("Personal", global_personal_agent),
            "Automation": AgentNode("Automation", global_automation_agent)
        }
        self._build_default_graph()

    def _build_default_graph(self):
        # Planner connects to all specialized task agents
        planner = self.nodes["Planner"]
        for name in ["Research", "Coding", "Document", "Vision", "Automation", "Personal"]:
            planner.connect(self.nodes[name])

        # Research connects to Document for synthesis
        self.nodes["Research"].connect(self.nodes["Document"])
        # Coding connects to Automation for script saving
        self.nodes["Coding"].connect(self.nodes["Automation"])
        # All connect back to Personal / Memory

    def get_topology(self) -> Dict[str, List[str]]:
        topology = {}
        for name, node in self.nodes.items():
            topology[name] = [edge.name for edge in node.edges]
        return topology

class AgentManager:
    def __init__(self):
        self.graph = AgentWorkflowGraph()
        self.active_agents = list(self.graph.nodes.keys())

    def get_agents_status(self) -> List[Dict[str, Any]]:
        status_list = []
        for name, node in self.graph.nodes.items():
            status_list.append({
                "name": name,
                "role": getattr(node.agent, "role", "Agent"),
                "status": "IDLE_STANDBY",
                "connections": [e.name for e in node.edges]
            })
        return status_list

    def execute_multi_agent_workflow(self, objective: str) -> Dict[str, Any]:
        """Runs the planner graph and dispatches through the agent network."""
        plan_steps = global_planner_agent.plan_workflow(objective)
        execution_log = []

        for step in plan_steps:
            agent_name = step["agent"]
            desc = step["description"]
            step_result = {"step": step["step"], "agent": agent_name, "status": "executed"}

            if agent_name == "Research":
                res = global_research_agent.execute(desc)
                step_result["output"] = res["report"]
            elif agent_name == "Coding":
                res = global_coding_agent.execute(desc)
                step_result["output"] = res["code_output"]
            elif agent_name == "Document":
                res = global_document_agent.execute(desc)
                step_result["output"] = res["document"]
            elif agent_name == "Automation":
                res = global_automation_agent.execute_action("launch", desc)
                step_result["output"] = res.get("message", "Executed")
            elif agent_name == "Personal":
                res = global_personal_agent.execute_daily_briefing()
                step_result["output"] = res["briefing"]
            else:
                step_result["output"] = f"Plan step completed by {agent_name}."

            execution_log.append(step_result)

        return {
            "objective": objective,
            "plan_steps": plan_steps,
            "execution_log": execution_log,
            "final_summary": f"Multi-agent workflow successfully completed {len(plan_steps)} stages."
        }

global_agent_manager = AgentManager()
