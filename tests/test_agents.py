"""
Multi-Agent Unit Tests for MARK 12
Validates Agent Graph topology, Planner DAG, and specialized agent execution.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from agents.agent_manager import global_agent_manager
from agents.planner_agent import global_planner_agent
from agents.coding_agent import global_coding_agent
from agents.research_agent import global_research_agent

def test_agent_graph_topology():
    topology = global_agent_manager.graph.get_topology()
    assert "Planner" in topology
    assert "Coding" in topology
    assert "Research" in topology
    assert len(topology["Planner"]) > 0, "Planner must connect to specialized agents"
    print("[PASS] test_agent_graph_topology")

def test_planner_dag_generation():
    objective = "Find the best Python machine learning courses, compare them and save the result in a document."
    steps = global_planner_agent.plan_workflow(objective)
    assert len(steps) >= 2
    agent_names = [s["agent"] for s in steps]
    assert "Research" in agent_names
    assert "Document" in agent_names
    print(f"[PASS] test_planner_dag_generation: {len(steps)} steps generated")

def test_specialist_execution():
    code_res = global_coding_agent.execute("Write a binary search function")
    assert "def " in code_res["code_output"] or "code" in code_res["code_output"].lower()

    research_res = global_research_agent.execute("Compare PostgreSQL vs SQLite")
    assert "report" in research_res
    print("[PASS] test_specialist_execution")

if __name__ == "__main__":
    test_agent_graph_topology()
    test_planner_dag_generation()
    test_specialist_execution()
