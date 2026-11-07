"""
Webcam controller for MARK 12
Captures live frames or snapshots from available system camera interfaces.
"""
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any

class WebcamManager:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index

    def capture_snapshot(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        save_path = output_path or f"storage/images/snapshot_{int(time.time())}.jpg"
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            import cv2
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                return {"success": False, "message": "Camera device not accessible or busy."}
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite(save_path, frame)
                return {"success": True, "path": save_path, "message": "Frame captured successfully."}
            return {"success": False, "message": "Failed to read frame from webcam."}
        except Exception as e:
            return {"success": False, "message": f"Webcam error: {str(e)}"}

global_webcam = WebcamManager()
