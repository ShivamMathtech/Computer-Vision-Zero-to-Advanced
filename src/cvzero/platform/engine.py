"""CPU perception pipeline with explicit classical and optional learned adapters."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import cv2
import numpy as np

from cvzero.course.tracking import KalmanTracker


@dataclass
class Engine:
    """Per-session tracker. Call from one ordered stream or under a session lock."""

    min_area: int = 35
    tracker: KalmanTracker = field(default_factory=lambda: KalmanTracker(gate=50, max_missed=5))
    yolo_model: object | None = None

    def analyze(self, rgb: np.ndarray) -> tuple[dict, np.ndarray]:
        start = time.perf_counter()
        if rgb.ndim != 3 or rgb.shape[2] != 3 or rgb.dtype != np.uint8:
            raise ValueError("Expected H×W×3 RGB uint8 image.")
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, np.array([0, 90, 70]), np.array([179, 255, 255]))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        detections = []
        if self.yolo_model is None:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < self.min_area:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / max(perimeter**2, 1)
                label = "round" if circularity > 0.78 else "angular"
                detections.append(
                    {
                        "box": [x, y, x + w, y + h],
                        "class": label,
                        "score": None,
                        "area_px": float(area),
                    }
                )
        else:
            prediction = self.yolo_model.predict(rgb[..., ::-1], verbose=False, device="cpu")[0]
            for box in prediction.boxes:
                detections.append(
                    {
                        "box": [int(v) for v in box.xyxy[0].tolist()],
                        "class": prediction.names[int(box.cls[0])],
                        "score": float(box.conf[0]),
                        "area_px": None,
                    }
                )
        centers = np.array(
            [[(d["box"][0] + d["box"][2]) / 2, (d["box"][1] + d["box"][3]) / 2] for d in detections]
        ).reshape(-1, 2)
        tracks = self.tracker.update(centers)
        # Assignment is solved inside the tracker. Recover current detection association
        # by a second one-to-one assignment, not independent nearest-neighbor choices.
        if len(centers) and tracks:
            from scipy.optimize import linear_sum_assignment

            cost = np.linalg.norm(
                centers[:, None, :] - np.array([t.state[:2] for t in tracks])[None, :, :], axis=-1
            )
            rows, cols = linear_sum_assignment(cost)
            for row, col in zip(rows, cols, strict=True):
                if cost[row, col] <= self.tracker.gate:
                    detections[row]["track_id"] = tracks[col].identity
        overlay = rgb.copy()
        for detection in detections:
            x1, y1, x2, y2 = detection["box"]
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.putText(
                overlay,
                f"{detection.get('track_id', '?')} {detection['class']}",
                (x1, max(12, y1 - 3)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1,
            )
        return {
            "detections": detections,
            "count": len(detections),
            "segmentation_fraction": float((mask > 0).mean()),
            "latency_ms": (time.perf_counter() - start) * 1000,
            "detector": "yolo" if self.yolo_model is not None else "color-contours",
            "segmentation": "HSV saturation mask",
            "classification": "detector labels"
            if self.yolo_model is not None
            else "contour circularity",
        }, overlay
