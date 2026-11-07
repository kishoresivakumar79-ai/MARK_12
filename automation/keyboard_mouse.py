"""
Keyboard and Mouse Automation for MARK 12
Safely performs desktop input automation and screenshot capture.
"""
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

SCREENSHOT_DIR = Path("storage/images")

class KeyboardMouseController:
    def __init__(self):
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def take_screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        out_name = filename or f"screenshot_{int(time.time())}.png"
        out_path = SCREENSHOT_DIR / out_name

        # Try PyAutoGUI or PIL ImageGrab
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            img.save(str(out_path))
            return {
                "success": True,
                "file_path": str(out_path).replace("\\", "/"),
                "relative_url": f"/storage/images/{out_name}"
            }
        except Exception:
            pass

        try:
            import pyautogui
            pyautogui.screenshot(str(out_path))
            return {
                "success": True,
                "file_path": str(out_path).replace("\\", "/"),
                "relative_url": f"/storage/images/{out_name}"
            }
        except Exception as e:
            return {"success": False, "message": f"Screenshot failed: {str(e)}"}

    def type_text(self, text: str, interval: float = 0.05) -> bool:
        try:
            import pyautogui
            pyautogui.typewrite(text, interval=interval)
            return True
        except Exception:
            return False

    def press_key(self, key: str) -> bool:
        try:
            import pyautogui
            pyautogui.press(key)
            return True
        except Exception:
            return False

global_input_controller = KeyboardMouseController()
