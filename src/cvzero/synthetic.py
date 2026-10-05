"""Deterministic arrays for offline lessons; not a real-world benchmark dataset."""

from __future__ import annotations

from numbers import Integral

import numpy as np
from numpy.typing import NDArray


def make_scene(height: int = 160, width: int = 240, seed: int = 42) -> NDArray[np.uint8]:
    """Create a gradient, rectangle, circle and seeded texture using NumPy only."""
    for value in (height, width):
        if isinstance(value, bool) or not isinstance(value, Integral) or not 16 <= value <= 2048:
            raise ValueError("Synthetic height and width must be integers from 16 to 2048.")
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[:height, :width]
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[..., 0] = np.rint(40 + 150 * x / (width - 1)).astype(np.uint8)
    image[..., 1] = np.rint(35 + 150 * y / (height - 1)).astype(np.uint8)
    image[..., 2] = rng.integers(35, 65, size=(height, width), dtype=np.uint8)
    image[height // 5 : height // 2, width // 8 : width // 3] = (230, 60, 50)
    radius = min(height, width) // 6
    circle = (x - 3 * width // 4) ** 2 + (y - height // 2) ** 2 <= radius**2
    image[circle] = (45, 100, 235)
    image[3 * height // 4 : 7 * height // 8, width // 5 : 4 * width // 5] = (70, 215, 100)
    return image


def tiny_palette() -> NDArray[np.uint8]:
    """A two-row, three-column RGB image with hand-checkable values."""
    return np.array(
        [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            [[0, 0, 0], [127, 127, 127], [255, 255, 255]],
        ],
        dtype=np.uint8,
    )
