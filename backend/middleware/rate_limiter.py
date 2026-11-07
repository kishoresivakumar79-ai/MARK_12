"""
Rate Limiter Middleware for MARK 12
Protects APIs from excessive request bursts.
"""
import time
from typing import Dict, List

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.client_records: Dict[str, List[float]] = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        timestamps = self.client_records.get(client_ip, [])
        # Filter timestamps outside window
        valid = [t for t in timestamps if now - t < self.window_seconds]
        if len(valid) >= self.max_requests:
            return False
        valid.append(now)
        self.client_records[client_ip] = valid
        return True

global_rate_limiter = RateLimiter()
