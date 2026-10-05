"""Run a project config with explicit command-line overrides."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runner import run


def main(default_config=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=default_config, required=default_config is None
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    try:
        if not args.config.is_file():
            raise FileNotFoundError(f"Configuration not found: {args.config}")
        config = json.loads(args.config.read_text())
        if args.seed is not None:
            config["seed"] = args.seed
        result = run(**config)
        result.save(args.output, config)
    except (ValueError, TypeError, FileNotFoundError, ImportError) as exc:
        parser.exit(2, f"Project could not run: {exc}\n")
    print(f"Saved measured report to {args.output}")
