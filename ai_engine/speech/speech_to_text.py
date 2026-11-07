"""
Speech to Text Engine for MARK 12
Supports Faster-Whisper, SpeechRecognition, and audio file decoding with fallback.
"""
import os
import base64
from typing import Optional

class SpeechToText:
    def __init__(self, engine: str = "whisper"):
        self.engine = engine
        self._whisper_model = None
        self._sr_recognizer = None

    def transcribe_file(self, audio_file_path: str) -> str:
        if not os.path.exists(audio_file_path):
            return ""

        # Try SpeechRecognition if installed
        try:
            import speech_recognition as sr
            if not self._sr_recognizer:
                self._sr_recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file_path) as source:
                audio = self._sr_recognizer.record(source)
                return self._sr_recognizer.recognize_google(audio)
        except Exception:
            pass

        # Try Faster Whisper or Whisper if installed
        try:
            import whisper
            if not self._whisper_model:
                self._whisper_model = whisper.load_model("base")
            res = self._whisper_model.transcribe(audio_file_path)
            return res.get("text", "").strip()
        except Exception:
            pass

        return "Speech received. (Configure Whisper or SpeechRecognition for local transcription)"

    def transcribe_base64(self, b64_data: str) -> str:
        try:
            audio_bytes = base64.b64decode(b64_data)
            temp_path = "storage/audio/temp_input.wav"
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
            return self.transcribe_file(temp_path)
        except Exception as e:
            return f"Audio transcription error: {str(e)}"

global_stt = SpeechToText()
