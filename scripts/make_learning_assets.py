"""Create original, precise learning figures and the runnable project's preview."""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch

from cvzero.images import adjust_brightness
from cvzero.lab import render_contact_sheet
from cvzero.synthetic import make_scene

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    assets = ROOT / "assets"
    chapter_assets = ROOT / "01-python-for-computer-vision" / "assets"
    assets.mkdir(exist_ok=True)
    chapter_assets.mkdir(exist_ok=True)
    fig = Figure(figsize=(15, 8), facecolor="#f5f7fa")
    FigureCanvasAgg(fig)
    ax = fig.subplots()
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.set_axis_off()
    ax.text(0.025, 0.945, "COMPUTER VISION", fontsize=28, color="#182e45", weight="bold")
    ax.text(0.025, 0.88, "Zero to Advanced", fontsize=20, color="#247782")
    ax.text(
        0.025,
        0.825,
        "Learn the numbers. Explain the method. Build the system.",
        fontsize=13,
        color="#586b7d",
    )
    stages = [
        (
            "01  FOUNDATIONS",
            "Python · NumPy · pixels · OpenCV",
            "Understand and manipulate image data",
        ),
        (
            "02  CLASSICAL VISION",
            "Filters · geometry · features · motion",
            "Build explainable image pipelines",
        ),
        (
            "03  LEARNING",
            "ML · CNNs · PyTorch · transfer",
            "Train and evaluate with disciplined splits",
        ),
        (
            "04  SCENE UNDERSTANDING",
            "Detection · masks · pose · tracking",
            "Connect predictions across space and time",
        ),
        (
            "05  REPRESENTATIONS",
            "Transformers · multimodal · generation",
            "Study what models learn and miss",
        ),
        (
            "06  SPATIAL REASONING",
            "Geometry · depth · point clouds · NeRF",
            "Reason about cameras and 3D structure",
        ),
        ("07  ENGINEERING", "Optimize · deploy · monitor", "Measure and maintain real systems"),
        (
            "THIS RELEASE: ALL 53 CHAPTERS",
            "160 notebooks + projects + capstone",
            "CPU experiments with measured evidence",
        ),
    ]
    for index, (title, concepts, objective) in enumerate(stages):
        row, column = divmod(index, 2)
        x = 0.025 + column * 0.49
        y = 0.61 - row * 0.185
        face = "#e4f0ee" if index == 7 else "white"
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                0.45,
                0.151,
                boxstyle="round,pad=0.012",
                facecolor=face,
                edgecolor="#d7e0e8",
                linewidth=1,
            )
        )
        ax.text(x + 0.018, y + 0.112, title, fontsize=10.5, weight="bold", color="#20737e")
        ax.text(x + 0.018, y + 0.066, concepts, fontsize=11.5, color="#182e45")
        ax.text(x + 0.018, y + 0.025, objective, fontsize=10.4, color="#637183")
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
    fig.savefig(assets / "learning-journey.png", dpi=130)
    fig.clear()

    fig = Figure(figsize=(8, 5), layout="constrained")
    FigureCanvasAgg(fig)
    ax = fig.subplots()
    grid = np.array([[0, 40, 80, 120], [40, 80, 120, 160], [80, 120, 160, 200]], dtype=np.uint8)
    ax.imshow(grid, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    for y in range(3):
        for x in range(4):
            ax.text(
                x,
                y,
                str(grid[y, x]),
                ha="center",
                va="center",
                fontsize=18,
                color="white" if grid[y, x] < 128 else "black",
            )
    ax.set(
        xticks=range(4),
        yticks=range(3),
        xlabel="x = column",
        ylabel="y = row",
        title="An image is a grid of numbers",
    )
    fig.savefig(chapter_assets / "pixel-grid.png", dpi=130)
    fig.clear()

    scene = make_scene()
    fig = Figure(figsize=(12, 3), layout="constrained")
    FigureCanvasAgg(fig)
    axes = fig.subplots(1, 4)
    axes[0].imshow(scene)
    axes[0].set_title("Original RGB")
    for channel, title in enumerate(("Red", "Green", "Blue")):
        plane = np.zeros_like(scene)
        plane[..., channel] = scene[..., channel]
        axes[channel + 1].imshow(plane)
        axes[channel + 1].set_title(title)
    for axis in axes:
        axis.set_axis_off()
    fig.savefig(chapter_assets / "channels.png", dpi=130)
    fig.clear()
    sample = ROOT / "projects/beginner/pixel-lab/sample-output/contact-sheet.png"
    if sample.is_file():
        shutil.copyfile(sample, chapter_assets / "pixel-lab-preview.png")
    else:
        render_contact_sheet(
            scene, adjust_brightness(scene, 20), chapter_assets / "pixel-lab-preview.png"
        )
    print("Generated learning journey, pixel grid, channel planes and project preview.")


if __name__ == "__main__":
    main()
