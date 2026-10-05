"""Command-line entry points with explicit error messages and nonzero failure exits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

from .benchmark import benchmark_brightness, environment_info
from .images import image_summary
from .io import load_rgb, save_json
from .lab import LabConfig, run_lab
from .synthetic import make_scene


def make_parser() -> argparse.ArgumentParser:
    """Keep the interface discoverable through --help."""
    parser = argparse.ArgumentParser(prog="cvzero", description="Chapter 01: CPU-only Pixel Lab")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Check imports and RGB/BGR conversion; show environment")
    inspect = commands.add_parser("inspect", help="Print shape, type and channel statistics")
    inspect.add_argument("image", type=Path)
    bench = commands.add_parser("benchmark", help="Measure loop, NumPy and OpenCV brightness")
    bench.add_argument("--repeats", type=int, default=5)
    bench.add_argument("--output", type=Path, default=Path("artifacts/benchmark.json"))
    for name, help_text in (
        ("demo", "Edit a seeded synthetic scene"),
        ("edit", "Edit a local image"),
    ):
        command = commands.add_parser(name, help=help_text)
        if name == "edit":
            command.add_argument("image", type=Path)
        else:
            command.add_argument("--seed", type=int, default=42)
        command.add_argument(
            "--output", type=Path, required=True, help="New or empty output folder"
        )
        command.add_argument("--brightness", type=float, default=20.0)
        command.add_argument(
            "--gains", nargs=3, type=float, default=(1.0, 1.0, 1.0), metavar=("R", "G", "B")
        )
        command.add_argument("--crop", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    return parser


def main(argv: list[str] | None = None) -> int:
    """Return zero on success; report actionable input failures on stderr."""
    args = make_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            pixel = np.array([[[255, 0, 0]]], dtype=np.uint8)
            converted = cv2.cvtColor(pixel, cv2.COLOR_RGB2BGR)
            if converted.tolist() != [[[0, 0, 255]]]:
                raise RuntimeError("Unexpected OpenCV color conversion result.")
            print(json.dumps({"status": "ok", "runtime": environment_info()}, indent=2))
        elif args.command == "inspect":
            print(json.dumps(image_summary(load_rgb(args.image)), indent=2))
        elif args.command == "benchmark":
            if args.output.exists():
                raise ValueError("Benchmark output already exists; choose a new --output file.")
            result = benchmark_brightness(args.repeats)
            save_json(args.output, result)
            print(f"Saved measured benchmark to {args.output}")
        else:
            seed = args.seed if args.command == "demo" else None
            image = make_scene(seed=seed) if args.command == "demo" else load_rgb(args.image)
            label = "synthetic scene" if args.command == "demo" else args.image.name
            config = LabConfig(
                args.brightness, tuple(args.gains), tuple(args.crop) if args.crop else None
            )
            run_lab(image, args.output, config, label, seed)
            print(f"Saved Pixel Lab report to {args.output / 'report.html'}")
        return 0
    except (FileNotFoundError, ValueError, TypeError, OSError, RuntimeError, cv2.error) as error:
        print(f"cvzero: {error}", file=sys.stderr)
        return 2
