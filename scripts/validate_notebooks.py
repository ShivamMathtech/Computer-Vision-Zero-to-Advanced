"""Execute each lesson in a fresh interpreter with a real IPython kernel.

The default in-process kernel uses Jupyter messages without opening sockets.
A separate Python process per notebook prevents hidden state across lessons.
Use --engine jupyter for standard nbclient/socket transport on a normal host.
"""

from __future__ import annotations

import argparse
import atexit
import json
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from queue import Empty
from time import perf_counter

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def execute_inprocess(source: Path, destination: Path) -> None:
    """Worker: capture stream and rich display outputs through Jupyter messages."""
    from ipykernel.inprocess.manager import InProcessKernelManager

    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    manager = InProcessKernelManager()
    manager.start_kernel()
    manager.kernel.shell.enable_matplotlib("inline")
    client = manager.client()
    client.start_channels()
    try:
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            cell.outputs = []
            client.execute(cell.source, store_history=True, allow_stdin=False)
            reply = client.get_shell_msg(timeout=30)
            # In-process stream messages can have no parent ID. Since execution
            # is synchronous and the queue is drained after every cell, all
            # messages now belong to this cell; no cells run concurrently.
            manager.kernel.stdout.flush()
            manager.kernel.stderr.flush()
            while True:
                try:
                    message = client.get_iopub_msg(block=False)
                except Empty:
                    break
                kind = message["msg_type"]
                if kind in {"stream", "display_data", "execute_result", "error"}:
                    cell.outputs.append(nbformat.v4.output_from_msg(message))
                elif kind == "clear_output":
                    cell.outputs = []
            cell.execution_count = reply["content"].get("execution_count")
            if reply["content"]["status"] != "ok":
                destination.parent.mkdir(parents=True, exist_ok=True)
                nbformat.write(notebook, destination)
                raise RuntimeError(
                    f"Cell failed: {reply['content'].get('ename')}: {reply['content'].get('evalue')}"
                )
        notebook.metadata["cvzero_validation"] = {
            "engine": "ipykernel.inprocess",
            "fresh_interpreter": True,
            "python": platform.python_version(),
            "input_requests_allowed": False,
        }
        nbformat.validate(notebook)
        destination.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, destination)
    finally:
        client.stop_channels()
        manager.shutdown_kernel()


def execute_jupyter(source: Path, destination: Path, directory: Path, timeout: int) -> None:
    """Alternative normal socket-backed nbclient execution, using this interpreter."""
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    from nbclient import NotebookClient

    spec_dir = directory / "cvzero-validate"
    spec_dir.mkdir(exist_ok=True)
    (spec_dir / "kernel.json").write_text(
        json.dumps(
            {
                "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                "display_name": "CV Zero validation",
                "language": "python",
            }
        )
    )
    specs = KernelSpecManager(kernel_dirs=[str(directory)])
    manager = KernelManager(
        kernel_name="cvzero-validate", kernel_spec_manager=specs, ip="127.0.0.1"
    )
    notebook = nbformat.read(source, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=timeout,
        km=manager,
        resources={"metadata": {"path": str(source.parent)}},
        allow_errors=False,
    )
    try:
        client.execute(cleanup_kc=True)
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
        manager.cleanup_resources()
        atexit.unregister(client._cleanup_kernel)
    destination.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "executed-notebooks")
    parser.add_argument("--engine", choices=("inprocess", "jupyter"), default="inprocess")
    parser.add_argument("--include-templates", action="store_true")
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Seconds per notebook in inprocess mode, per cell in jupyter mode",
    )
    parser.add_argument(
        "--worker", nargs=2, metavar=("SOURCE", "DESTINATION"), help=argparse.SUPPRESS
    )
    args = parser.parse_args()
    if args.worker:
        execute_inprocess(Path(args.worker[0]), Path(args.worker[1]))
        return
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    catalog = json.loads((ROOT / "docs/curriculum.json").read_text())
    lessons = []
    for chapter in catalog["chapters"]:
        if chapter["status"] in {"complete", "in_validation"}:
            lessons.extend(sorted((ROOT / chapter["folder"] / "notebooks").glob("*.ipynb")))
    if args.include_templates:
        lessons.append(ROOT / "docs/templates/notebook-template.ipynb")
    if not lessons:
        raise RuntimeError("No delivered notebooks found.")
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="cvzero-kernel-") as directory:
        for path in lessons:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            start = perf_counter()
            destination = args.output / path.parent.parent.name / path.name
            if args.engine == "inprocess":
                process = subprocess.run(
                    [
                        sys.executable,
                        "-Xfrozen_modules=off",
                        str(Path(__file__).resolve()),
                        "--worker",
                        str(path),
                        str(destination),
                    ],
                    cwd=path.parent,
                    capture_output=True,
                    text=True,
                    timeout=args.timeout,
                )
                if process.returncode:
                    raise RuntimeError(f"{path.name} failed:\n{process.stdout}\n{process.stderr}")
            else:
                execute_jupyter(path, destination, Path(directory), args.timeout)
            executed = nbformat.read(destination, as_version=4)
            code_cells = [cell for cell in executed.cells if cell.cell_type == "code"]
            assert all(cell.execution_count is not None for cell in code_cells)
            assert not any(
                output.output_type == "error" for cell in code_cells for output in cell.outputs
            )
            images = sum(
                "image/png" in output.get("data", {})
                for cell in code_cells
                for output in cell.outputs
            )
            results.append(
                {
                    "notebook": path.relative_to(ROOT).as_posix(),
                    "status": "passed",
                    "seconds": perf_counter() - start,
                    "code_cells": len(code_cells),
                    "png_outputs": images,
                    "kind": "template" if "templates" in path.parts else "lesson",
                }
            )
            print(f"PASS {path.name}: {len(code_cells)} code cells, {images} inline figures")
    report = {
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "engine": "ipykernel.inprocess, isolated interpreter"
        if args.engine == "inprocess"
        else "nbclient/socket",
        "fresh_kernel_per_notebook": True,
        "results": results,
    }
    (args.output / "execution-report.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
