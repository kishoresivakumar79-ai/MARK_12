"""
WebSocket Event Handlers for MARK 12
Routes incoming socket messages for real-time chat, voice streaming, and system telemetry.
"""
from typing import Dict, Any
from core.assistant import mark_12
from backend.websocket.connection import global_ws_manager

async def handle_websocket_message(websocket: Any, raw_text: str):
    import json
    try:
        data = json.loads(raw_text)
    except Exception:
        data = {"type": "chat", "message": raw_text}

    msg_type = data.get("type", "chat")

    if msg_type == "chat":
        text = data.get("message", "")
        conv_id = data.get("conversation_id", "default")
        enable_voice = data.get("enable_voice", False)
        response = mark_12.send_message(text, conv_id=conv_id, enable_voice=enable_voice)
        await websocket.send_text(json.dumps({
            "event": "chat_response",
            "data": response
        }))
    elif msg_type == "ping":
        await websocket.send_text(json.dumps({"event": "pong"}))
