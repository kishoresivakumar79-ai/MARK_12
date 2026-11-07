"""
Audio Manager for MARK 12
Implements Queue Data Structure for thread-safe sequential voice command processing.
"""
import queue
import time
from typing import Optional, Dict, Any

class AudioCommandQueue:
    """FIFO Queue ensuring voice requests are processed in strict temporal order."""
    def __init__(self, maxsize: int = 50):
        self._queue = queue.Queue(maxsize=maxsize)

    def enqueue_audio_command(self, audio_data: Any, metadata: Optional[Dict[str, Any]] = None) -> bool:
        try:
            item = {
                "audio": audio_data,
                "metadata": metadata or {},
                "enqueued_at": time.time()
            }
            self._queue.put(item, block=False)
            return True
        except queue.Full:
            return False

    def dequeue_audio_command(self, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def task_done(self):
        self._queue.task_done()

    def size(self) -> int:
        return self._queue.qsize()

    def is_empty(self) -> bool:
        return self._queue.empty()

global_audio_queue = AudioCommandQueue()
