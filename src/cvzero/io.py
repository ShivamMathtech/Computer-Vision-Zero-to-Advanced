"""Explicit 8-bit image I/O and JSON helpers for local experiments."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from .images import require_rgb

MAX_PIXELS = 16_000_000


def load_rgb(path: str | Path, max_pixels: int = MAX_PIXELS) -> np.ndarray:
    """Decode an 8-bit image, apply EXIF orientation and composite alpha on white.

    Only common 8-bit modes are accepted; 16-bit/scientific images need explicit
    scaling in a later lesson. EXIF and ICC metadata are not preserved in outputs.
    """
    source = Path(path).expanduser()
    if not source.is_file():
        raise FileNotFoundError(
            f"Image not found: {source}. Check the file path and working folder."
        )
    if not isinstance(max_pixels, int) or isinstance(max_pixels, bool) or max_pixels < 1:
        raise ValueError("max_pixels must be a positive integer.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(source) as opened:
                if opened.width * opened.height > max_pixels:
                    raise ValueError(
                        f"Image exceeds {max_pixels:,} pixels; resize it before this lesson."
                    )
                if opened.mode not in {"1", "L", "LA", "P", "RGB", "RGBA"}:
                    raise ValueError(
                        f"Unsupported image mode {opened.mode}; explicitly convert to 8-bit RGB first."
                    )
                if getattr(opened, "n_frames", 1) != 1:
                    raise ValueError(
                        "Animated/multipage images are not supported; export a single frame."
                    )
                oriented = ImageOps.exif_transpose(opened)
                if "A" in oriented.getbands() or "transparency" in oriented.info:
                    rgba = oriented.convert("RGBA")
                    background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
                    converted = Image.alpha_composite(background, rgba).convert("RGB")
                else:
                    converted = oriented.convert("RGB")
                return np.array(converted, dtype=np.uint8, copy=True)
    except (
        UnidentifiedImageError,
        OSError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as error:
        raise ValueError(f"Cannot decode image {source.name}: {error}") from error


def save_rgb(path: str | Path, image: np.ndarray) -> Path:
    """Save RGB PNG without lossy compression; deliberately reject other suffixes."""
    require_rgb(image)
    destination = Path(path)
    if destination.suffix.lower() != ".png":
        raise ValueError("Use a .png output for exact pixel comparisons in Chapter 01.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image).save(destination, format="PNG")
    return destination


def save_json(path: str | Path, value: dict | list) -> Path:
    """Write portable JSON, rejecting NaN and infinity."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return destination
