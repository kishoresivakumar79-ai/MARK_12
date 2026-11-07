"""
Scheduler module for MARK 12
Executes scheduled background jobs and recurring routines.
"""
import time
import threading
from typing import Dict, Any, Callable, List

class BackgroundScheduler:
    def __init__(self):
        self.jobs: List[Dict[str, Any]] = []
        self._running = False
        self._thread = None

    def add_job(self, name: str, interval_seconds: int, func: Callable):
        self.jobs.append({
            "name": name,
            "interval": interval_seconds,
            "func": func,
            "last_run": 0.0
        })

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            now = time.time()
            for job in self.jobs:
                if now - job["last_run"] >= job["interval"]:
                    job["last_run"] = now
                    try:
                        job["func"]()
                    except Exception as e:
                        print(f"[Scheduler Job Error] {job['name']}: {e}")
            time.sleep(1)

    def stop(self):
        self._running = False

global_scheduler = BackgroundScheduler()
