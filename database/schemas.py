"""
Pydantic Schemas for MARK 12 Request and Response Validation.
Includes fallback dictionary models if pydantic is not installed.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    from pydantic import BaseModel, Field

    class ChatRequest(BaseModel):
        message: str
        conversation_id: Optional[str] = "default"
        stream: Optional[bool] = False
        enable_voice_response: Optional[bool] = False

    class ChatResponse(BaseModel):
        response: str
        conversation_id: str
        intent: Optional[str] = "general_query"
        agent_used: Optional[str] = "brain"
        audio_url: Optional[str] = None
        plan_steps: Optional[List[Dict[str, Any]]] = None

    class VoiceRequest(BaseModel):
        audio_base64: Optional[str] = None
        transcription: Optional[str] = None

    class MemoryCreate(BaseModel):
        category: str = "general"
        content: str
        importance: int = 3
        tags: Optional[str] = ""

    class TaskCreate(BaseModel):
        title: str
        description: Optional[str] = ""
        priority: int = 3
        parent_id: Optional[str] = None
        due_date: Optional[str] = None
        tags: Optional[str] = ""

    class TaskUpdate(BaseModel):
        title: Optional[str] = None
        description: Optional[str] = None
        priority: Optional[int] = None
        status: Optional[str] = None
        due_date: Optional[str] = None

    class AutomationCommand(BaseModel):
        action: str
        target: Optional[str] = None
        parameters: Optional[Dict[str, Any]] = None

    class VisionRequest(BaseModel):
        image_base64: Optional[str] = None
        prompt: Optional[str] = "Analyze this image and describe what you see."

    class SystemStatusResponse(BaseModel):
        status: str
        cpu_usage: float
        memory_usage: float
        disk_usage: float
        os: str
        python_version: str
        uptime_seconds: float
        active_agents: List[str]

except ImportError:
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
        def model_dump(self):
            return self.__dict__

    class ChatRequest(BaseModel): pass
    class ChatResponse(BaseModel): pass
    class VoiceRequest(BaseModel): pass
    class MemoryCreate(BaseModel): pass
    class TaskCreate(BaseModel): pass
    class TaskUpdate(BaseModel): pass
    class AutomationCommand(BaseModel): pass
    class VisionRequest(BaseModel): pass
    class SystemStatusResponse(BaseModel): pass
