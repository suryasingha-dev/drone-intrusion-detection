"""
detector.py
-----------
Wraps the YOLOv5 model and exposes a clean inference interface.
"""

import torch
from PIL import Image


class DroneDetector:
    """Loads a custom YOLOv5 model and runs inference on PIL images."""

    def __init__(self, model_path: str, input_size: int = 640, conf_threshold: float = 0.5):
        self.input_size     = input_size
        self.conf_threshold = conf_threshold
        self.model          = torch.hub.load("ultralytics/yolov5", "custom", path=model_path)
        self.model.conf     = conf_threshold

    def detect(self, frame_bgr):
        """
        Run inference on a BGR numpy frame (as returned by OpenCV).

        Returns a list of dicts:
            [{"x1", "y1", "x2", "y2", "conf", "cls"}, ...]
        """
        img     = Image.fromarray(frame_bgr[..., ::-1])   # BGR → RGB
        results = self.model(img, size=self.input_size)

        detections = []
        for *box, conf, cls in results.xyxy[0].tolist():
            x1, y1, x2, y2 = box
            detections.append({
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2,
                "conf": conf,
                "cls": int(cls),
            })

        return detections
