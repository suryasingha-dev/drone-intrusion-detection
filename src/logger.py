"""
logger.py
---------
Handles all file I/O: output directories, evidence images, and event logs.
"""

import os
import cv2
from datetime import datetime


class EventLogger:
    """Creates a dated output folder and writes structured intrusion logs."""

    SEPARATOR = "-" * 40

    def __init__(self, base_dir: str):
        today          = datetime.now().strftime("%Y-%m-%d")
        self.output_dir = os.path.join(base_dir, today)
        os.makedirs(self.output_dir, exist_ok=True)

        self.log_path = os.path.join(self.output_dir, "event_log.txt")
        self._write_session_header()

    def _write_session_header(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a") as f:
            f.write(f"\n{'='*50}\nSESSION STARTED: {timestamp}\n{'='*50}\n")

    def save_evidence(self, frame, conf: float, intrusion_duration: float) -> str:
        """Save a frame to disk and write a log entry. Returns the filename."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename  = f"intrusion_{timestamp}.jpg"
        filepath  = os.path.join(self.output_dir, filename)

        cv2.imwrite(filepath, frame)

        with open(self.log_path, "a") as f:
            f.write(
                f"\n[{timestamp}]\n"
                f"Event:          Drone Intrusion\n"
                f"Confidence:     {conf*100:.2f}%\n"
                f"Intrusion Time: {intrusion_duration:.1f}s\n"
                f"Evidence:       {filename}\n"
                f"{self.SEPARATOR}\n"
            )

        return filename
