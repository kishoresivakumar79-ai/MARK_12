"""
Authentication Middleware for MARK 12
JWT token validation and session security.
"""
import time
import hmac
import hashlib
import json
import base64
from typing import Optional, Dict, Any

class AuthManager:
    def __init__(self, secret_key: str = "mark_12_secret"):
        self.secret_key = secret_key

    def create_token(self, payload: Dict[str, Any], exp_seconds: int = 86400) -> str:
        data = dict(payload)
        data["exp"] = time.time() + exp_seconds
        header_b64 = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
        payload_b64 = base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")
        signature = hmac.new(self.secret_key.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
        return f"{header_b64}.{payload_b64}.{sig_b64}"

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            header_b64, payload_b64, sig_b64 = parts
            expected_sig = hmac.new(self.secret_key.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
            expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode().rstrip("=")
            if not hmac.compare_digest(sig_b64, expected_sig_b64):
                return None
            # Decode payload
            padded_payload = payload_b64 + "=" * (-len(payload_b64) % 4)
            payload_data = json.loads(base64.urlsafe_b64decode(padded_payload).decode())
            if payload_data.get("exp", 0) < time.time():
                return None
            return payload_data
        except Exception:
            return None

global_auth_manager = AuthManager()
