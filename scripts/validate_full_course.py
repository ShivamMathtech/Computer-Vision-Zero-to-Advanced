"""Execute all lesson notebooks in fresh processes, with bounded parallel workers.

No shared notebook state and no kernel sockets. This wraps the same worker as
validate_notebooks.py; --jobs changes validation throughput, not lesson behavior.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def execute(path, output, timeout):
    start = time.perf_counter()
    destination = output / path.parent.parent.name / path.name
    env = {
        **os.environ,
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "MPLBACKEND": "Agg",
    }
    process = subprocess.run(
        [
            sys.executable,
            "-Xfrozen_modules=off",
            str(ROOT / "scripts/validate_notebooks.py"),
            "--worker",
            str(path),
            str(destination),
        ],
        cwd=path.parent,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if process.returncode:
        return {
            "notebook": path.relative_to(ROOT).as_posix(),
            "status": "failed",
            "error": (process.stdout + process.stderr)[-6000:],
        }
    notebook = nbformat.read(destination, as_version=4)
    nbformat.validate(notebook)
    cells = [c for c in notebook.cells if c.cell_type == "code"]
    if not all(c.execution_count is not None for c in cells):
        raise RuntimeError(f"Unexecuted cell: {path}")
    if any(o.output_type == "error" for c in cells for o in c.outputs):
        raise RuntimeError(f"Error output: {path}")
    images = sum("image/png" in o.get("data", {}) for c in cells for o in c.outputs)
    return {
        "notebook": path.relative_to(ROOT).as_posix(),
        "status": "passed",
        "seconds": time.perf_counter() - start,
        "code_cells": len(cells),
        "png_outputs": images,
        "kind": "lesson",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--chapters", type=int, nargs="*")
    parser.add_argument("--copy-back", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/executed-full-course")
    args = parser.parse_args()
    if not 1 <= args.jobs <= 8:
        parser.error("jobs must be 1–8.")
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    chapters = json.loads((ROOT / "docs/curriculum.json").read_text())["chapters"]
    lessons = [
        p
        for c in chapters
        if not args.chapters or c["number"] in args.chapters
        for p in sorted((ROOT / c["folder"] / "notebooks").glob("*.ipynb"))
    ]
    if not lessons:
        parser.error("No lessons selected.")
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(execute, p, args.output, args.timeout): p for p in lessons}
        for future in as_completed(futures):
            path = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                result = {
                    "notebook": path.relative_to(ROOT).as_posix(),
                    "status": "failed",
                    "error": str(exc),
                }
            results.append(result)
            print(result["status"].upper(), result["notebook"], flush=True)
            if result["status"] == "failed":
                print(result["error"], flush=True)
            elif args.copy_back:
                shutil.copy2(args.output / path.parent.parent.name / path.name, path)
            report = {
                "executed_at_utc": datetime.now(timezone.utc).isoformat(),
                "python": platform.python_version(),
                "engine": "ipykernel.inprocess; one fresh subprocess per notebook",
                "fresh_kernel_per_notebook": True,
                "results": sorted(results, key=lambda r: r["notebook"]),
            }
            (args.output / "execution-report.json").write_text(json.dumps(report, indent=2) + "\n")
    if any(r["status"] != "passed" for r in results):
        raise SystemExit(1)
    print(f"Validated {len(results)} notebooks.", flush=True)


if __name__ == "__main__":
    main()
