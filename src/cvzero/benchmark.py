"""Small honest benchmark: same image, same operation, measured local timings."""

from __future__ import annotations

import platform
from importlib.metadata import PackageNotFoundError, version
from statistics import median
from time import perf_counter

import cv2
import numpy as np

from .images import adjust_brightness, brightness_loop
from .synthetic import make_scene


def environment_info() -> dict:
    """Record runtime context; never treat it as cross-machine performance."""
    packages = {}
    for name in ("numpy", "matplotlib", "Pillow", "opencv-python-headless", "cvzero"):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = "not installed as a distribution"
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "not reported",
        "opencv_runtime": cv2.__version__,
        "packages": packages,
    }


def benchmark_brightness(repeats: int = 5, seed: int = 42) -> dict:
    """Measure a fixed 96x128 RGB workload after one warm-up per implementation.

    This includes each function's allocation and excludes file I/O and plotting.
    Memory is limited to exact input/output array byte counts; peak RSS is not
    measured. Correctness is pixel equality, not model or dataset accuracy.
    """
    if isinstance(repeats, bool) or not isinstance(repeats, int) or not 1 <= repeats <= 50:
        raise ValueError("repeats must be an integer from 1 to 50.")
    image = make_scene(96, 128, seed)
    expected = adjust_brightness(image, 30)
    operations = {
        "python_loop": lambda: brightness_loop(image, 30),
        "numpy": lambda: adjust_brightness(image, 30),
        "opencv": lambda: cv2.addWeighted(image, 1.0, image, 0.0, 30.0),
    }
    previous_threads = cv2.getNumThreads()
    rows = []
    try:
        cv2.setNumThreads(1)
        for name, operation in operations.items():
            operation()
            times = []
            for _ in range(repeats):
                start = perf_counter()
                result = operation()
                times.append((perf_counter() - start) * 1000)
            error = int(np.abs(result.astype(np.int16) - expected.astype(np.int16)).max())
            rows.append(
                {
                    "implementation": name,
                    "median_ms": median(times),
                    "samples_ms": times,
                    "max_absolute_pixel_error": error,
                    "input_array_bytes": image.nbytes,
                    "output_array_bytes": result.nbytes,
                }
            )
    finally:
        cv2.setNumThreads(previous_threads)
    return {
        "environment": environment_info(),
        "seed": seed,
        "shape": list(image.shape),
        "delta": 30,
        "repeats": repeats,
        "warmup_runs": 1,
        "opencv_threads": 1,
        "metric": "wall time in milliseconds; allocation included, I/O excluded",
        "peak_memory_measured": False,
        "results": rows,
    }
