"""
Automation Unit Tests for MARK 12
Validates security whitelist, permission checks, and system monitor telemetry.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from automation.permission_manager import global_permission_manager
from automation.system_monitor import global_system_monitor
from automation.file_manager import global_file_manager

def test_permission_whitelist():
    assert global_permission_manager.is_app_allowed("notepad") is True
    assert global_permission_manager.is_app_allowed("calculator") is True
    assert global_permission_manager.is_app_allowed("calc") is True
    assert global_permission_manager.is_app_allowed("malicious_worm.exe") is False
    print("[PASS] test_permission_whitelist")

def test_command_safety_validator():
    safe_check = global_permission_manager.validate_command_safety("notepad.exe")
    assert safe_check["safe"] is True

    unsafe_check = global_permission_manager.validate_command_safety("format c: /fs:NTFS")
    assert unsafe_check["safe"] is False
    print("[PASS] test_command_safety_validator")

def test_system_telemetry():
    telemetry = global_system_monitor.get_system_telemetry()
    assert "cpu_percent" in telemetry
    assert "memory_percent" in telemetry
    assert "os" in telemetry
    assert telemetry["status"] == "HEALTHY"
    print(f"[PASS] test_system_telemetry: CPU {telemetry['cpu_percent']}%, RAM {telemetry['memory_percent']}%")

def test_safe_file_manager():
    rel = "storage/test_io.txt"
    written = global_file_manager.write_text(rel, "MARK 12 I/O test")
    assert written is True
    read_back = global_file_manager.read_text(rel)
    assert read_back == "MARK 12 I/O test"
    deleted = global_file_manager.delete_file(rel)
    assert deleted is True
    print("[PASS] test_safe_file_manager")

if __name__ == "__main__":
    test_permission_whitelist()
    test_command_safety_validator()
    test_system_telemetry()
    test_safe_file_manager()
