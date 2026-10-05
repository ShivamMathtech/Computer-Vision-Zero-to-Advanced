"""Measured optimization, service, scheduling and monitoring experiments."""

from __future__ import annotations

import base64
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np

from .classical import picture, video_frames
from .result import Result


def quantize_symmetric(weights):
    """Per-tensor signed int8 quantization and floating reconstruction."""
    scale = max(float(np.max(np.abs(weights))) / 127, np.finfo(float).eps)
    quantized = np.clip(np.rint(weights / scale), -127, 127).astype(np.int8)
    return quantized, scale, quantized.astype(np.float32) * scale


def optimization(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    weights = rng.normal(0, 0.1 * amount, (64, 128)).astype("float32")
    x = rng.normal(size=(16, 128)).astype("float32")
    q, scale, reconstructed = quantize_symmetric(weights)
    baseline = x @ weights.T
    approximation = x @ reconstructed.T
    timings = []
    for matrix in (weights, reconstructed):
        samples = []
        for _ in range(30):
            start = time.perf_counter()
            x @ matrix.T
            samples.append((time.perf_counter() - start) * 1e6)
        timings.append(float(np.median(samples)))
    return Result(
        "49 · Quantization error and fair measurement",
        {
            "Original weights": weights,
            "Reconstructed weights": reconstructed,
            "Output error": approximation - baseline,
        },
        metrics={
            "float_storage_bytes": weights.nbytes,
            "int8_storage_bytes_with_scale": q.nbytes + 4,
            "scale": scale,
            "output_rmse": float(np.sqrt(np.mean((baseline - approximation) ** 2))),
            "float_matmul_median_us": timings[0],
            "dequantized_matmul_median_us": timings[1],
        },
        notes="Both timings use float32 multiplication. Reduced storage alone does not imply int8 acceleration. Actual ONNX export/runtime comparison is available through scripts/export_model.py; TensorRT requires supported NVIDIA hardware.",
    )


def deployment(lesson=0, seed=42, amount=1.0):
    try:
        from fastapi.testclient import TestClient

        from cvzero.platform.app import create_app
    except ImportError as exc:
        raise ImportError('Install API dependencies: python -m pip install -e ".[api]"') from exc
    image = np.zeros((96, 128, 3), np.uint8)
    cv2.circle(image, (32, 40), 18, (235, 70, 60), -1)
    cv2.rectangle(image, (78, 45), (111, 78), (40, 220, 100), -1)
    _, encoded = cv2.imencode(".png", image[..., ::-1])
    with tempfile.TemporaryDirectory() as folder:
        with TestClient(create_app(Path(folder) / "events.sqlite")) as client:
            sid = client.post("/sessions").json()["session_id"]
            payload = {"frame_id": 0, "image_base64": base64.b64encode(encoded).decode()}
            response = client.post(f"/sessions/{sid}/frames", json=payload)
            response.raise_for_status()
            report = response.json()
            duplicate = client.post(f"/sessions/{sid}/frames", json=payload)
            history = client.get(f"/sessions/{sid}/history").json()["events"]
    annotated = cv2.imdecode(
        np.frombuffer(base64.b64decode(report["image_base64"]), np.uint8), cv2.IMREAD_COLOR
    )[..., ::-1]
    return Result(
        "50 · Inference API contract and persistence",
        {"RGB request": image, "API response overlay": annotated},
        metrics={
            "http_status": response.status_code,
            "duplicate_frame_status": duplicate.status_code,
            "persisted_frames": len(history),
            "detections": report["count"],
            "engine_latency_ms": report["latency_ms"],
        },
        notes="Actual FastAPI request handling and SQLite writes through an in-process HTTP client. No public server is launched. Network latency, authentication and concurrent load are not measured here.",
    )


def edge(lesson=0, seed=42, amount=1.0):
    image = picture(seed, size=192)
    reference = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), 80, 160) > 0
    errors = []
    latency = []
    sizes = []
    for size in (192, 144, 96, 48):
        samples = []
        for _ in range(8):
            start = time.perf_counter()
            small = cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
            edges = cv2.Canny(cv2.cvtColor(small, cv2.COLOR_RGB2GRAY), 80, 160)
            samples.append((time.perf_counter() - start) * 1000)
        restored = cv2.resize(edges, (192, 192), interpolation=cv2.INTER_NEAREST) > 0
        union = (reference | restored).sum()
        errors.append(float((reference & restored).sum() / max(union, 1)))
        latency.append(float(np.median(samples)))
        sizes.append(small.nbytes)
    return Result(
        "51 · Resolution, memory and edge fidelity",
        {"Full-resolution RGB": image, "Small edge map resized for display": restored},
        curves={
            "Input side→median processing milliseconds": np.column_stack(
                [[192, 144, 96, 48], latency]
            ),
            "Input side→edge IoU": np.column_stack([[192, 144, 96, 48], errors]),
        },
        metrics={
            "resolutions": [192, 144, 96, 48],
            "rgb_buffer_bytes": sizes,
            "median_processing_ms": latency,
            "edge_iou": errors,
        },
        notes="Local CPU measurements are not edge-device benchmarks. Edge IoU compares to the full-resolution algorithm, not annotated ground truth. Quantization, power and device runtimes require separate target-device measurements.",
    )


def queue_simulation(arrivals, service_seconds, capacity=2):
    """Discrete-event latest-frame queue. Returns completed latencies and drops."""
    if service_seconds <= 0 or capacity < 1:
        raise ValueError("Positive service time and capacity required.")
    waiting = []
    completed = []
    dropped = 0
    busy_until = None
    active = None
    for arrival in arrivals:
        while busy_until is not None and busy_until <= arrival:
            completed.append(busy_until - active)
            if waiting:
                active = waiting.pop(0)
                busy_until += service_seconds
            else:
                busy_until = None
                active = None
        if busy_until is None:
            active = float(arrival)
            busy_until = active + service_seconds
        else:
            if len(waiting) >= capacity:
                waiting.pop(0)
                dropped += 1
            waiting.append(float(arrival))
    while busy_until is not None:
        completed.append(busy_until - active)
        if waiting:
            active = waiting.pop(0)
            busy_until += service_seconds
        else:
            busy_until = None
    return np.array(completed), dropped


def realtime(lesson=0, seed=42, amount=1.0):
    arrivals = np.arange(90) / 30
    duration = 0.045 * amount
    bounded, drops = queue_simulation(arrivals, duration, 2)
    fifo, _ = queue_simulation(arrivals, duration, 1000)
    return Result(
        "52 · Bounded queues and frame age",
        curves={"FIFO latency seconds": fifo, "Latest bounded queue latency seconds": bounded},
        metrics={
            "input_frames": len(arrivals),
            "bounded_processed": len(bounded),
            "bounded_dropped": drops,
            "bounded_p95_seconds": float(np.percentile(bounded, 95)),
            "fifo_p95_seconds": float(np.percentile(fifo, 95)),
        },
        notes="Deterministic scheduling simulation, not a measured FPS benchmark. Dropped frames change tracking time steps; production motion models must use timestamps, not assume a fixed unit interval.",
    )


def population_stability(reference, current, bins=10):
    """PSI on fixed quantile bins, with smoothing; a drift flag, not accuracy."""
    boundaries = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))
    boundaries[0] = -np.inf
    boundaries[-1] = np.inf
    a = np.histogram(reference, boundaries)[0] + 0.5
    b = np.histogram(current, boundaries)[0] + 0.5
    a = a / a.sum()
    b = b / b.sum()
    return float(np.sum((b - a) * np.log(b / a)))


def production(lesson=0, seed=42, amount=1.0):
    from cvzero.platform.engine import Engine
    from cvzero.platform.store import EventStore

    rng = np.random.default_rng(seed)
    reference = rng.normal(120, 20, 500)
    current = rng.normal(120 + 20 * amount, 25, 500)
    counts = []
    times = []
    engine = Engine()
    with tempfile.TemporaryDirectory() as folder:
        store = EventStore(Path(folder) / "events.sqlite")
        for i, frame in enumerate(video_frames(12)):
            rgb = frame.copy() if frame.ndim == 3 else cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            rgb[..., 1] = 0
            report, _ = engine.analyze(rgb)
            store.append("smoke", i, float(i) / 30, report)
            counts.append(report["count"])
            times.append(report["latency_ms"])
        events = store.history("smoke")
    return Result(
        "53 · Monitoring and reproducible event logs",
        curves={"Frame→engine milliseconds": times, "Frame→detections": counts},
        panels={
            "Reference intensity histogram": np.histogram(reference, bins=20, range=(0, 255))[0],
            "Shifted intensity histogram": np.histogram(current, bins=20, range=(0, 255))[0],
        },
        metrics={
            "stored_events": len(events),
            "intensity_psi": population_stability(reference, current),
            "engine_p95_ms": float(np.percentile(times, 95)),
        },
        notes="PSI detects a distribution change in a synthetic scalar feature; it cannot establish label accuracy or cause. Only local frame-processing time is measured. Database queries, frontend and network overhead are separate.",
    )
