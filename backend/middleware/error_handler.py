"""
Error Handler for MARK 12
Formats exceptions into standardized JSON API responses.
"""
from typing import Dict, Any

def format_error_response(status_code: int, message: str, details: Any = None) -> Dict[str, Any]:
    return {
        "success": False,
        "error": {
            "code": status_code,
            "message": message,
            "details": details
        }
    }
