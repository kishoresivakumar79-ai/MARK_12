"""
Vision Agent for MARK 12
Interprets visual data, recognizes objects, and explains image content.
"""
from typing import Dict, Any
from ai_engine.vision.image_analyzer import global_image_analyzer
from ai_engine.vision.object_detection import global_object_detector

class VisionAgent:
    def __init__(self):
        self.name = "Vision"
        self.role = "Computer Vision & Optical Intelligence"

    def execute(self, image_path: str) -> Dict[str, Any]:
        analysis = global_image_analyzer.analyze_file(image_path)
        detection = global_object_detector.detect_entities(image_path)
        return {
            "agent": self.name,
            "status": "completed",
            "image": image_path,
            "metadata": analysis,
            "detected_objects": detection
        }

global_vision_agent = VisionAgent()
