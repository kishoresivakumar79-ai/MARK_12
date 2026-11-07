"""
Chat API Endpoint for MARK 12
POST /api/chat - Sends chat message to AI Brain
GET /api/chat/history - Retrieves conversation history
"""
from typing import Dict, Any, Optional
from core.assistant import mark_12
from database.repository import Repository

def handle_chat_message(data: Dict[str, Any]) -> Dict[str, Any]:
    message = data.get("message", "")
    conv_id = data.get("conversation_id", "default")
    enable_voice = data.get("enable_voice_response", False)
    return mark_12.send_message(message, conv_id=conv_id, enable_voice=enable_voice)

def handle_get_history(conv_id: str = "default", limit: int = 50) -> Dict[str, Any]:
    history = Repository.get_conversation_history(conv_id, limit=limit)
    return {"conversation_id": conv_id, "messages": history}

# FastAPI router integration
try:
    from fastapi import APIRouter
    from database.schemas import ChatRequest, ChatResponse
    router = APIRouter(prefix="/api/chat", tags=["Chat"])

    @router.post("", response_model=None)
    async def chat_endpoint(req: ChatRequest):
        return handle_chat_message(req.model_dump() if hasattr(req, "model_dump") else req.dict())

    @router.get("/history")
    async def history_endpoint(conversation_id: str = "default", limit: int = 50):
        return handle_get_history(conversation_id, limit)
except ImportError:
    router = None
