"""Consistent plots and measured reports shared by independent chapter labs."""

from __future__ import annotations

import json
import platform
import textwrap
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


@dataclass
class Result:
    title: str
    panels: dict = field(default_factory=dict)
    curves: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    notes: str = ""
    points: dict = field(default_factory=dict)

    def plot(self):
        """Create a labeled figure without changing a notebook's plot backend."""
        count = len(self.panels) + bool(self.curves) + len(self.points)
        fig = Figure(figsize=(12, max(3.6, 3.4 * ((count + 2) // 3))), layout="constrained")
        FigureCanvasAgg(fig)
        fig.suptitle(self.title, fontsize=15, weight="bold")
        i = 1
        for title, data in self.panels.items():
            ax = fig.add_subplot((count + 2) // 3, min(3, count), i)
            i += 1
            data = np.asarray(data)
            if data.ndim == 1:
                ax.plot(data)
                ax.set(xlabel="Index", ylabel="Value")
            else:
                ax.imshow(
                    data,
                    cmap="viridis" if np.nanmax(data) > 1 and data.dtype.kind == "f" else "gray",
                )
                ax.set(xlabel="Column / x", ylabel="Row / y")
            ax.set_title(textwrap.fill(title, 33), fontsize=10)
        if self.curves:
            ax = fig.add_subplot((count + 2) // 3, min(3, count), i)
            i += 1
            for label, values in self.curves.items():
                values = np.asarray(values)
                ax.plot(values[:, 0], values[:, 1], label=label) if values.ndim == 2 else ax.plot(
                    values, label=label
                )
            ax.set(xlabel="Step / sample / parameter (see legend)", ylabel="Recorded value")
            ax.legend(fontsize=8)
            ax.grid(alpha=0.2)
        for label, points in self.points.items():
            ax = fig.add_subplot((count + 2) // 3, min(3, count), i, projection="3d")
            i += 1
            pts = np.asarray(points)
            ax.scatter(*pts.T, s=3)
            ax.set(xlabel="X", ylabel="Y", zlabel="Z", title=label)
        return fig

    def save(self, output, configuration=None):
        output = Path(output)
        if output.exists() and any(output.iterdir()):
            raise ValueError("Use a new or empty output folder.")
        output.mkdir(parents=True, exist_ok=True)
        self.plot().savefig(output / "result.png", dpi=110)
        packages = {}
        for name in ("numpy", "opencv-python-headless", "scipy", "scikit-learn", "torch"):
            try:
                packages[name] = version(name)
            except PackageNotFoundError:
                packages[name] = "not installed"
        report = {
            "title": self.title,
            "metrics": self.metrics,
            "notes": self.notes,
            "configuration": configuration or {},
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": packages,
            "data_scope": "generated teaching data unless explicitly stated otherwise",
        }
        (output / "metrics.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
        np.savez_compressed(
            output / "arrays.npz",
            **{f"panel_{i}": np.asarray(v) for i, v in enumerate(self.panels.values())},
        )
        return output
