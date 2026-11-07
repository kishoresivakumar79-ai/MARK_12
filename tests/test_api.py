"""
API and Assistant End-to-End Unit Tests for MARK 12
Validates natural language chat, command dispatch, and task creation.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.assistant import mark_12
from backend.api import chat, tasks, memory, system

def test_assistant_chat():
    res = mark_12.send_message("Hello Jarvis")
    assert "response" in res
    assert res["agent_used"] in ["Brain", "safety"]
    print(f"[PASS] test_assistant_chat: '{res['response'][:60]}...'")

def test_command_dispatch():
    res = mark_12.send_message("system status")
    assert "MARK 12 Telemetry" in res["response"]
    print("[PASS] test_command_dispatch")

def test_task_creation_via_assistant():
    res = mark_12.send_message("create task Review robotic sensors")
    assert "Task registered" in res["response"]
    print("[PASS] test_task_creation_via_assistant")

def test_memory_via_assistant():
    res = mark_12.send_message("remember that user prefers Python and Rust")
    assert "committed this to long-term memory" in res["response"].lower()
    print("[PASS] test_memory_via_assistant")

if __name__ == "__main__":
    test_assistant_chat()
    test_command_dispatch()
    test_task_creation_via_assistant()
    test_memory_via_assistant()
