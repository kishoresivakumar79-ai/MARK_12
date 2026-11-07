"""
Text to Speech Engine for MARK 12
Supports Edge-TTS, pyttsx3 offline speech synthesis, and audio file generation.
"""
import os
import uuid
import asyncio
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
AUDIO_DIR = BASE_DIR / "storage" / "audio"

class TextToSpeech:
    def __init__(self, voice: str = "en-US-ChristopherNeural"):
        self.voice = voice
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        self._pyttsx3_engine = None

    def synthesize(self, text: str, filename: Optional[str] = None) -> Optional[str]:
        """Synthesizes text into an audio file and returns relative path."""
        if not text:
            return None

        out_name = filename or f"tts_{uuid.uuid4().hex[:8]}.mp3"
        out_path = AUDIO_DIR / out_name

        # 1. Try edge-tts (Natural neural voice)
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, self.voice)
            # Run async communication in synchronous context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(communicate.save(str(out_path)))
            loop.close()
            if out_path.exists():
                return f"/storage/audio/{out_name}"
        except Exception:
            pass

        # 2. Try pyttsx3 (Native system TTS)
        try:
            import pyttsx3
            if not self._pyttsx3_engine:
                self._pyttsx3_engine = pyttsx3.init()
            wav_name = f"tts_{uuid.uuid4().hex[:8]}.wav"
            wav_path = AUDIO_DIR / wav_name
            self._pyttsx3_engine.save_to_file(text, str(wav_path))
            self._pyttsx3_engine.runAndWait()
            if wav_path.exists():
                return f"/storage/audio/{wav_name}"
        except Exception:
            pass

        return None

global_tts = TextToSpeech()
