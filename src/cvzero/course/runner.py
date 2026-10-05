"""One discoverable interface; each dispatch target is a topic-specific lab."""

from __future__ import annotations

import argparse
from importlib import import_module

from .result import Result

LABS = {
    2: ("classical", "mathematics"),
    3: ("classical", "fundamentals"),
    4: ("classical", "opencv_basics"),
    5: ("classical", "filtering"),
    6: ("classical", "enhancement"),
    7: ("classical", "transformations"),
    8: ("classical", "colors"),
    9: ("classical", "features"),
    10: ("classical", "matching"),
    11: ("classical", "morphology_lab"),
    12: ("classical", "contours"),
    13: ("classical", "edges"),
    14: ("classical", "segmentation"),
    15: ("classical", "video"),
    16: ("classical", "calibration"),
    17: ("classical", "motion"),
    18: ("classical", "single_tracking"),
    19: ("classical", "faces"),
    20: ("classical", "recognition"),
    21: ("classical", "ocr"),
    22: ("classical", "machine_learning"),
    23: ("deep", "cnn"),
    24: ("deep", "pytorch_lab"),
    25: ("deep", "classification"),
    26: ("deep", "transfer"),
    27: ("deep", "detection"),
    28: ("deep", "yolo_grid"),
    29: ("deep", "segmentation_lab"),
    30: ("deep", "instances"),
    31: ("deep", "segmentation_lab"),
    32: ("deep", "pose"),
    33: ("deep", "hands"),
    34: ("deep", "actions"),
    35: ("spatial", "optical_flow"),
    36: ("spatial", "multi_tracking"),
    37: ("deep", "vit"),
    38: ("deep", "attention_lab"),
    39: ("deep", "self_supervision"),
    40: ("deep", "vision_language"),
    41: ("spatial", "multimodal"),
    42: ("deep", "generative"),
    43: ("deep", "diffusion"),
    44: ("spatial", "reconstruction"),
    45: ("spatial", "depth"),
    46: ("spatial", "stereo"),
    47: ("spatial", "point_clouds"),
    48: ("deep", "nerf"),
    49: ("engineering", "optimization"),
    50: ("engineering", "deployment"),
    51: ("engineering", "edge"),
    52: ("engineering", "realtime"),
    53: ("engineering", "production"),
}


def lab_function(chapter):
    if chapter not in LABS:
        raise ValueError("Choose chapter 2–53; Chapter 1 uses cvzero demo.")
    module, name = LABS[chapter]
    return getattr(import_module(f"cvzero.course.{module}"), name)


def run(chapter: int, lesson: int = 0, seed: int = 42, amount: float = 1.0) -> Result:
    """Run one reproducible CPU experiment; no network or pretrained weights."""
    if lesson not in (0, 1, 2):
        raise ValueError("lesson must be 0, 1 or 2.")
    if not 0.1 <= amount <= 3:
        raise ValueError("amount must be in [0.1, 3].")
    return lab_function(chapter)(lesson, seed, amount)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--lesson", type=int, choices=(0, 1, 2), default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--amount", type=float, default=1.0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = run(args.chapter, args.lesson, args.seed, args.amount)
        output = result.save(args.output, vars(args))
    except (ValueError, ImportError, FileNotFoundError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print(f"Saved measured report and plot to {output}")
