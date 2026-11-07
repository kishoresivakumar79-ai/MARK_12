"""
Voice API Endpoint for MARK 12
POST /api/voice - Transcribes voice input and processes through AI Brain
"""
from typing import Dict, Any
from ai_engine.speech.speech_to_text import global_stt
from core.assistant import mark_12

def handle_voice_input(data: Dict[str, Any]) -> Dict[str, Any]:
    b64_audio = data.get("audio_base64")
    direct_transcription = data.get("transcription")

    if direct_transcription:
        transcription = direct_transcription
    elif b64_audio:
        transcription = global_stt.transcribe_base64(b64_audio)
    else:
        return {"error": "No audio data or transcription provided."}

    # Process through assistant with voice response enabled
    result = mark_12.send_message(transcription, enable_voice=True)
    result["transcription"] = transcription
    return result

try:
    from fastapi import APIRouter
    from database.schemas import VoiceRequest
    router = APIRouter(prefix="/api/voice", tags=["Voice"])

    @router.post("")
    async def voice_endpoint(req: VoiceRequest):
        return handle_voice_input(req.model_dump() if hasattr(req, "model_dump") else req.dict())
except ImportError:
    router = None
