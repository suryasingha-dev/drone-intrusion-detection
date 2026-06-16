"""
visualizer.py
-------------
All OpenCV drawing logic: bounding boxes, HUD overlay, warning banner.
"""

import cv2


class Visualizer:
    """Renders detection overlays and HUD stats onto video frames."""

    FONT       = cv2.FONT_HERSHEY_SIMPLEX
    COLOR_BOX  = (0, 0, 255)
    COLOR_HUD  = (255, 255, 255)
    COLOR_TIME = (0, 255, 255)
    COLOR_WARN = (0, 0, 255)

    def draw_detection(self, frame, x1, y1, x2, y2, conf):
        """Draw bounding box, confidence score, and centroid coordinates."""
        ix1, iy1, ix2, iy2 = int(x1), int(y1), int(x2), int(y2)
        cx, cy = int((x1 + x2) / 2), int(y2)

        cv2.rectangle(frame, (ix1, iy1), (ix2, iy2), self.COLOR_BOX, 2)
        cv2.putText(frame, f"{conf*100:.1f}%",
                    (ix1, iy1 - 10), self.FONT, 0.5, self.COLOR_BOX, 2)
        cv2.putText(frame, f"({cx}, {cy})",
                    (ix1, iy2 + 20), self.FONT, 0.5, self.COLOR_BOX, 2)

    def draw_warning(self, frame):
        """Overlay a red warning banner across the top of the frame."""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 55), (0, 0, 180), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        cv2.putText(frame, "⚠  DRONE INTRUSION DETECTED  ⚠",
                    (w // 2 - 270, 36), self.FONT, 0.85, (255, 255, 255), 2)

    def draw_hud(self, frame, total_detections: int, intrusion_duration: float):
        """Render detection stats in the bottom-left corner."""
        h = frame.shape[0]
        cv2.putText(frame, f"Detections : {total_detections}",
                    (15, h - 45), self.FONT, 0.65, self.COLOR_HUD, 2)
        cv2.putText(frame, f"Intrusion  : {intrusion_duration:.1f}s",
                    (15, h - 15), self.FONT, 0.65, self.COLOR_TIME, 2)
