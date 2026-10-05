"""RGB uint8 operations: readable reference code before optimized libraries.

Public image arrays use (height, width, 3), in red/green/blue order. Operations
return new arrays. Coordinates are zero-based; crop end points are exclusive.
"""

from __future__ import annotations

import math
from numbers import Integral

import numpy as np
from numpy.typing import NDArray

RGB = NDArray[np.uint8]


def require_rgb(image: RGB) -> RGB:
    """Reject ambiguous dtype, empty input or an unexpected channel layout."""
    if not isinstance(image, np.ndarray):
        raise TypeError("Expected a NumPy array; load it with cvzero.io.load_rgb().")
    if image.ndim != 3 or image.shape[2] != 3 or min(image.shape[:2]) < 1:
        raise ValueError("Expected a nonempty RGB image with shape (height, width, 3).")
    if image.dtype != np.uint8:
        raise TypeError("Expected uint8 values in [0, 255]; convert and scale explicitly.")
    return image


def validate_delta(delta: float) -> float:
    """Require a finite additive brightness offset in the teaching range."""
    value = float(delta)
    if not math.isfinite(value) or not -255 <= value <= 255:
        raise ValueError("Brightness must be a finite number between -255 and 255.")
    return value


def validate_gains(gains: tuple[float, float, float]) -> NDArray[np.float64]:
    """Require one nonnegative, bounded multiplier per RGB channel."""
    values = np.asarray(gains, dtype=np.float64)
    if values.shape != (3,) or not np.isfinite(values).all():
        raise ValueError("Gains must contain three finite numbers: red green blue.")
    if np.any((values < 0) | (values > 4)):
        raise ValueError("Each channel gain must be between 0 and 4.")
    return values


def brightness_loop(image: RGB, delta: float) -> RGB:
    """Reference loop: add, clip and round each channel without uint8 overflow."""
    require_rgb(image)
    delta = validate_delta(delta)
    result = np.empty_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(3):
                value = float(image[y, x, c]) + delta
                result[y, x, c] = round(min(255.0, max(0.0, value)))
    return result


def adjust_brightness(image: RGB, delta: float) -> RGB:
    """Vectorized equivalent of brightness_loop; input is never mutated."""
    require_rgb(image)
    delta = validate_delta(delta)
    values = image.astype(np.float64) + delta
    return np.rint(np.clip(values, 0, 255)).astype(np.uint8)


def adjust_channels(image: RGB, gains: tuple[float, float, float]) -> RGB:
    """Broadcast a (3,) gain vector across all rows and columns."""
    require_rgb(image)
    values = image.astype(np.float64) * validate_gains(gains)
    return np.rint(np.clip(values, 0, 255)).astype(np.uint8)


def grayscale_loop(image: RGB) -> NDArray[np.uint8]:
    """A readable weighted RGB grayscale approximation, using Python loops.

    Weights apply to encoded channel values; this is not physical luminance.
    OpenCV uses fixed-point arithmetic and may differ by one intensity level.
    """
    require_rgb(image)
    gray = np.empty(image.shape[:2], dtype=np.uint8)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            r, g, b = [float(value) for value in image[y, x]]
            gray[y, x] = round(0.299 * r + 0.587 * g + 0.114 * b)
    return gray


def rgb_to_gray(image: RGB) -> NDArray[np.uint8]:
    """Vectorized weighted grayscale; produces shape (height, width)."""
    require_rgb(image)
    weights = np.array([0.299, 0.587, 0.114], dtype=np.float64)
    values = (image.astype(np.float64) * weights).sum(axis=2)
    return np.rint(np.clip(values, 0, 255)).astype(np.uint8)


def crop_rgb(image: RGB, x0: int, y0: int, x1: int, y1: int) -> RGB:
    """Return a copy of image[y0:y1, x0:x1]; reject empty/out-of-range crops."""
    require_rgb(image)
    bounds = (x0, y0, x1, y1)
    if any(isinstance(v, bool) or not isinstance(v, Integral) for v in bounds):
        raise TypeError("Crop bounds must be integers: x0 y0 x1 y1.")
    height, width = image.shape[:2]
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError(f"Crop must satisfy 0 <= x0 < x1 <= {width} and 0 <= y0 < y1 <= {height}.")
    return image[y0:y1, x0:x1].copy()


def channel_histograms(image: RGB) -> NDArray[np.int64]:
    """Return exact counts with shape (3, 256); row 0 is the red channel."""
    require_rgb(image)
    return np.stack([np.bincount(image[..., c].ravel(), minlength=256) for c in range(3)])


def image_summary(image: RGB) -> dict:
    """Return JSON-compatible shape, storage and descriptive pixel statistics."""
    require_rgb(image)
    return {
        "height": int(image.shape[0]),
        "width": int(image.shape[1]),
        "channels": 3,
        "color_order": "RGB",
        "dtype": str(image.dtype),
        "array_bytes": int(image.nbytes),
        "min_rgb": image.min(axis=(0, 1)).tolist(),
        "max_rgb": image.max(axis=(0, 1)).tolist(),
        "mean_rgb": image.mean(axis=(0, 1)).tolist(),
    }
