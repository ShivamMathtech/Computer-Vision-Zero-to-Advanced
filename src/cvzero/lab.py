"""Small end-to-end image laboratory: transform, visualize and document a run."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from html import escape
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from .benchmark import environment_info
from .images import (
    adjust_brightness,
    adjust_channels,
    channel_histograms,
    crop_rgb,
    image_summary,
    require_rgb,
    rgb_to_gray,
    validate_delta,
    validate_gains,
)
from .io import save_json, save_rgb


@dataclass(frozen=True)
class LabConfig:
    """A named bundle of parameters; the same values appear in the saved report."""

    brightness: float = 20.0
    gains: tuple[float, float, float] = (1.0, 1.0, 1.0)
    crop: tuple[int, int, int, int] | None = None

    def __post_init__(self) -> None:
        validate_delta(self.brightness)
        validate_gains(self.gains)
        if self.crop is not None and len(self.crop) != 4:
            raise ValueError("Crop needs four integer bounds: x0 y0 x1 y1.")


def transform(image: np.ndarray, config: LabConfig) -> np.ndarray:
    """Apply crop, brightness, then channel gains, with clipping at each stage."""
    require_rgb(image)
    region = crop_rgb(image, *config.crop) if config.crop else image.copy()
    return adjust_channels(adjust_brightness(region, config.brightness), config.gains)


def render_contact_sheet(original: np.ndarray, edited: np.ndarray, path: Path) -> None:
    """Save a labeled preview; grayscale display uses a fixed intensity scale."""
    fig = Figure(figsize=(12, 7), layout="constrained")
    FigureCanvasAgg(fig)
    axes = fig.subplots(2, 3)
    fig.suptitle("Pixel Lab | numbers become images", fontsize=18, weight="bold")
    views = [
        (original, "Original · RGB"),
        (edited, "Edited · RGB"),
        (rgb_to_gray(edited), "Weighted grayscale"),
    ]
    for c, title in enumerate(("Red plane", "Green plane", "Blue plane")):
        colored = np.zeros_like(edited)
        colored[..., c] = edited[..., c]
        views.append((colored, title))
    for ax, (view, title) in zip(axes.ravel(), views, strict=True):
        ax.imshow(view, cmap="gray" if view.ndim == 2 else None, vmin=0, vmax=255)
        ax.set_title(title)
        ax.set_xlabel("x = column")
        ax.set_ylabel("y = row")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130)
    fig.clear()


def render_histogram(image: np.ndarray, path: Path) -> None:
    """Count intensities; each channel has height times width observations."""
    fig = Figure(figsize=(9, 4), layout="constrained")
    FigureCanvasAgg(fig)
    ax = fig.subplots()
    counts = channel_histograms(image)
    for c, (color, label) in enumerate(
        zip(("#c7454b", "#22835d", "#3569ba"), ("Red", "Green", "Blue"), strict=True)
    ):
        ax.plot(np.arange(256), counts[c], color=color, label=label)
    ax.set(
        xlabel="8-bit intensity", ylabel="Number of pixels", title="Edited image channel histograms"
    )
    ax.legend()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130)
    fig.clear()


def run_lab(
    image: np.ndarray,
    output: str | Path,
    config: LabConfig,
    source_label: str = "synthetic scene",
    seed: int | None = 42,
) -> dict:
    """Create a local report in a new or empty folder; never overwrite a prior run."""
    require_rgb(image)
    destination = Path(output)
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError(
            f"Output must be a new or empty folder: {destination}. Choose another run name."
        )
    edited = transform(image, config)
    destination.mkdir(parents=True, exist_ok=True)
    save_rgb(destination / "original.png", image)
    save_rgb(destination / "edited.png", edited)
    gray = rgb_to_gray(edited)
    save_rgb(destination / "grayscale.png", np.repeat(gray[..., None], 3, axis=2))
    render_contact_sheet(image, edited, destination / "contact-sheet.png")
    render_histogram(edited, destination / "histograms.png")
    summary = {
        "source": source_label,
        "seed": seed,
        "configuration": asdict(config),
        "operation_order": [
            "crop",
            "brightness (clip and round)",
            "channel gains (clip and round)",
        ],
        "original": image_summary(image),
        "edited": image_summary(edited),
        "environment": environment_info(),
        "result_type": "measured image statistics; no trained model",
    }
    save_json(destination / "summary.json", summary)
    title = escape(source_label)
    html = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pixel Lab report</title>
<style>body{{font:17px/1.6 system-ui,sans-serif;margin:40px auto;padding:0 24px;max-width:1000px;color:#172c42;background:#f4f7fa}}img{{max-width:100%;border:1px solid #d4dde6;border-radius:8px}}h1{{line-height:1.1}}a{{color:#126d83}}code{{background:#e7edf3;padding:2px 5px}}</style>
<h1>Pixel Lab</h1><p>Chapter 01 · Computer Vision — Zero to Advanced</p>
<p>Source: <strong>{title}</strong>. Crop → brightness → channel gains. Each stage clips to 0–255.</p>
<img src="contact-sheet.png" alt="Original image, edited image, grayscale and three color planes">
<h2>Intensity distribution</h2><img src="histograms.png" alt="Counts of red, green and blue intensity values">
<p>Each color histogram counts one observation per pixel. Counts are not probabilities.</p>
<p><a href="summary.json">Configuration, image statistics and runtime versions</a> ·
<a href="edited.png">Edited PNG</a></p>
<p>This is a pixel transformation experiment. It reports no classification accuracy or model performance.</p>
</html>"""
    (destination / "report.html").write_text(html, encoding="utf-8")
    return summary
