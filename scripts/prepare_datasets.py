"""Recreate the tiny synthetic fixtures. No download, labels or model required."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from cvzero.io import save_json, save_rgb
from cvzero.synthetic import make_scene, tiny_palette


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("datasets/synthetic"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    entries = []
    for name, image in (("scene.png", make_scene(seed=args.seed)), ("palette.png", tiny_palette())):
        destination = save_rgb(args.output / name, image)
        entries.append(
            {
                "file": name,
                "shape": list(image.shape),
                "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            }
        )
    save_json(
        args.output / "manifest.json",
        {
            "source": "cvzero.synthetic; generated original arrays",
            "seed": args.seed,
            "license": "MIT; see repository LICENSE",
            "purpose": "teaching fixtures, not a dataset benchmark",
            "files": entries,
        },
    )
    print(f"Prepared {len(entries)} synthetic PNGs in {args.output}")


if __name__ == "__main__":
    main()
