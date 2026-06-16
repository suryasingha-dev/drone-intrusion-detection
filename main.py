"""
main.py
-------
Entry point for the Drone Detection System.
Loads config, wires up modules, and runs the main detection loop.
"""

import time
import argparse

import cv2
import yaml
import winsound

from src import DroneDetector, RestrictedZone, EventLogger, Visualizer


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main(config_path: str):
    cfg = load_config(config_path)

    # ── Initialise modules ────────────────────────────────────────────────────
    detector   = DroneDetector(
        model_path      = cfg["model"]["path"],
        input_size      = cfg["model"]["input_size"],
        conf_threshold  = cfg["model"]["confidence_threshold"],
    )
    zone       = RestrictedZone()
    logger     = EventLogger(base_dir=cfg["output"]["base_dir"])
    visualizer = Visualizer()

    cap = cv2.VideoCapture(cfg["camera"]["source"])
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        raise RuntimeError("Could not open camera / video source.")

    cv2.namedWindow("Drone Detection")
    cv2.resizeWindow("Drone Detection", 1280, 720)
    cv2.setMouseCallback("Drone Detection", zone.handle_mouse)

    # ── Detection state ───────────────────────────────────────────────────────
    intrusion_delay    = cfg["detection"]["intrusion_delay"]
    total_detections   = 0
    detection_time     = 0.0
    intrusion_duration = 0.0
    detection_recorded = False

    print("[INFO] System running. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections     = detector.detect(frame)
        drone_in_frame = False
        alert_active   = False

        for det in detections:
            x1, y1, x2, y2, conf = det["x1"], det["y1"], det["x2"], det["y2"], det["conf"]
            drone_in_frame = True

            visualizer.draw_detection(frame, x1, y1, x2, y2, conf)

            if zone.contains_box(x1, y1, x2, y2):
                alert_active = True

                if detection_time == 0.0:
                    detection_time = time.time()

                intrusion_duration = time.time() - detection_time

                if intrusion_duration >= intrusion_delay and not detection_recorded:
                    winsound.Beep(
                        cfg["alert"]["beep_frequency"],
                        cfg["alert"]["beep_duration"],
                    )
                    logger.save_evidence(frame, conf, intrusion_duration)
                    total_detections  += 1
                    detection_recorded = True

        # Reset when drone leaves frame
        if not drone_in_frame:
            detection_time     = 0.0
            intrusion_duration = 0.0
            detection_recorded = False

        if alert_active:
            visualizer.draw_warning(frame)

        zone.draw(frame, alert=alert_active)
        visualizer.draw_hud(frame, total_detections, intrusion_duration)

        cv2.imshow("Drone Detection", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Session ended. Total intrusions recorded: {total_detections}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time drone intrusion detection system.")
    parser.add_argument(
        "--config", type=str,
        default="configs/config.yaml",
        help="Path to the YAML configuration file."
    )
    args = parser.parse_args()
    main(args.config)
