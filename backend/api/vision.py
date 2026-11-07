"""
Vision API Endpoint for MARK 12
POST /api/vision/analyze - Analyzes image content and metadata
POST /api/vision/snapshot - Captures live webcam snapshot
"""
import os
import time
from pathlib import Path
from typing import Dict, Any
from ai_engine.vision.image_analyzer import global_image_analyzer
from ai_engine.vision.object_detection import global_object_detector
from ai_engine.vision.webcam import global_webcam

IMAGES_DIR = Path("storage/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def analyze_image_bytes(file_name: str, file_bytes: bytes) -> Dict[str, Any]:
    save_path = IMAGES_DIR / file_name
    save_path.write_bytes(file_bytes)

    analysis = global_image_analyzer.analyze_file(str(save_path))
    detection = global_object_detector.detect_entities(str(save_path))

    return {
        "file_name": file_name,
        "image_url": f"/storage/images/{file_name}",
        "metadata": analysis,
        "detections": detection
    }

try:
    from fastapi import APIRouter, UploadFile, File
    from database.schemas import VisionRequest
    router = APIRouter(prefix="/api/vision", tags=["Vision"])

    @router.post("/analyze")
    async def analyze_endpoint(file: UploadFile = File(...)):
        content = await file.read()
        return analyze_image_bytes(file.filename, content)

    @router.post("/snapshot")
    async def snapshot_endpoint():
        res = global_webcam.capture_snapshot()
        return res
except ImportError:
    router = None
