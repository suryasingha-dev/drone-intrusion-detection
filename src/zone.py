"""
zone.py
-------
Manages the draggable restricted zone rectangle and intrusion logic.
"""

import cv2


class RestrictedZone:
    """
    An interactive, draggable quadrilateral drawn over the video feed.
    Corners can be repositioned via mouse drag.
    """

    HANDLE_RADIUS  = 8
    HANDLE_HIT     = 12   # px tolerance for clicking a corner
    COLOR_NORMAL   = (0, 220, 0)
    COLOR_ALERT    = (0, 0, 255)

    def __init__(self, corners=None):
        self.corners  = corners or [(50, 50), (250, 50), (250, 250), (50, 250)]
        self._dragging = False
        self._drag_idx = -1

    # ── Mouse interaction ────────────────────────────────────────────────────

    def handle_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, (cx, cy) in enumerate(self.corners):
                if abs(cx - x) <= self.HANDLE_HIT and abs(cy - y) <= self.HANDLE_HIT:
                    self._dragging = True
                    self._drag_idx = i
                    break
        elif event == cv2.EVENT_LBUTTONUP:
            self._dragging = False
        elif event == cv2.EVENT_MOUSEMOVE and self._dragging:
            self.corners[self._drag_idx] = (x, y)

    # ── Geometry ─────────────────────────────────────────────────────────────

    def contains_box(self, x1, y1, x2, y2) -> bool:
        """Return True if any corner of the bounding box lies inside the zone."""
        rx0, ry0 = self.corners[0]
        rx2, ry2 = self.corners[2]
        return any(
            rx0 <= px <= rx2 and ry0 <= py <= ry2
            for px, py in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
        )

    # ── Drawing ──────────────────────────────────────────────────────────────

    def draw(self, frame, alert: bool = False):
        color = self.COLOR_ALERT if alert else self.COLOR_NORMAL
        for i in range(4):
            cv2.line(frame, self.corners[i], self.corners[(i + 1) % 4], color, 2)
            cv2.circle(frame, self.corners[i], self.HANDLE_RADIUS, color, -1)
