"""
Voice and Speech Unit Tests for MARK 12
Validates wake word detection, audio command FIFO queue, and speech formatting.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ai_engine.speech.wake_word import global_wake_word_detector
from ai_engine.speech.audio_manager import global_audio_queue
from core.personality import global_personality

def test_wake_word_detection():
    assert global_wake_word_detector.contains_wake_word("Jarvis, what is the weather?") is True
    assert global_wake_word_detector.contains_wake_word("Hey Jarvis, initialize core") is True
    assert global_wake_word_detector.contains_wake_word("Good morning computer") is False

    stripped = global_wake_word_detector.strip_wake_word("Jarvis, open browser")
    assert stripped == "open browser"
    print("[PASS] test_wake_word_detection")

def test_audio_fifo_queue():
    assert global_audio_queue.is_empty() is True
    global_audio_queue.enqueue_audio_command(b"test_audio_frame_1", {"source": "mic"})
    global_audio_queue.enqueue_audio_command(b"test_audio_frame_2", {"source": "mic"})

    item1 = global_audio_queue.dequeue_audio_command(timeout=0.1)
    assert item1["audio"] == b"test_audio_frame_1"

    item2 = global_audio_queue.dequeue_audio_command(timeout=0.1)
    assert item2["audio"] == b"test_audio_frame_2"
    print("[PASS] test_audio_fifo_queue")

def test_speech_formatting():
    raw_response = "```python\ndef test(): pass\n```\nHere is your code, sir. It is fully operational."
    spoken = global_personality.format_speech(raw_response)
    assert "```" not in spoken
    print("[PASS] test_speech_formatting")

if __name__ == "__main__":
    test_wake_word_detection()
    test_audio_fifo_queue()
    test_speech_formatting()
