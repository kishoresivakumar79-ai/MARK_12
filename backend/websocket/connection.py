"""
WebSocket Connection Manager for MARK 12
Maintains active real-time client sockets and broadcasts telemetry events.
"""
import json
from typing import List, Any

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Any] = []

    async def connect(self, websocket: Any):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: Any):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: Any):
        await websocket.send_text(message)

    async def broadcast(self, data: dict):
        text = json.dumps(data)
        for conn in list(self.active_connections):
            try:
                await conn.send_text(text)
            except Exception:
                self.disconnect(conn)

global_ws_manager = ConnectionManager()
