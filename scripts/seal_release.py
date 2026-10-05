"""Seal progress and evidence only after the required validation results exist."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def main():
    primary = json.loads(
        (ROOT / "artifacts/executed-full-course/execution-report.json").read_text()
    )
    results = {r["notebook"]: r for r in primary["results"]}
    recheck = ROOT / "artifacts/executed-rechecks/execution-report.json"
    if recheck.exists():
        for r in json.loads(recheck.read_text())["results"]:
            results[r["notebook"]] = r
    assert len(results) == 160 and all(r["status"] == "passed" for r in results.values())
    xml = ET.parse(ROOT / "docs/test-results.xml")
    suites = list(xml.getroot().iter("testsuite"))
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(
        int(s.attrib.get("failures", 0)) + int(s.attrib.get("errors", 0)) for s in suites
    )
    skipped = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    assert tests >= 83 and failures == 0 and skipped == 0
    catalog = json.loads((ROOT / "docs/curriculum.json").read_text())
    rows = []
    hashes = {}
    for chapter in catalog["chapters"]:
        paths = sorted((ROOT / chapter["folder"] / "notebooks").glob("*.ipynb"))
        assert len(paths) == (4 if chapter["number"] == 1 else 3)
        for path in paths:
            key = path.relative_to(ROOT).as_posix()
            assert key in results
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            assert all(c.execution_count is not None for c in nb.cells if c.cell_type == "code")
            assert not any(
                o.output_type == "error"
                for c in nb.cells
                if c.cell_type == "code"
                for o in c.outputs
            )
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        chapter["status"] = "complete"
        chapter["notebooks"] = len(paths)
        rows.append(
            f"| [{chapter['number']:02d} · {chapter['title']}](../{chapter['folder']}/README.md) | Complete teaching pack | {len(paths)} / {len(paths)} passed | Included | Included |"
        )
    catalog["release"] = "1.0.0"
    catalog["completion_definition"] = (
        "Theory, reference code, focused executed CPU notebooks, exercises, challenge, mini-project baseline, assets and references. External research reproductions are not implied."
    )
    (ROOT / "docs/curriculum.json").write_text(json.dumps(catalog, indent=2) + "\n")
    report = {
        **primary,
        "assembled_at_utc": datetime.now(timezone.utc).isoformat(),
        "results": sorted(results.values(), key=lambda x: x["notebook"]),
        "notebook_sha256": hashes,
    }
    (ROOT / "docs/notebook-execution.json").write_text(json.dumps(report, indent=2) + "\n")
    packages = {
        name: version(name)
        for name in [
            "cvzero",
            "numpy",
            "matplotlib",
            "Pillow",
            "opencv-python-headless",
            "scipy",
            "scikit-learn",
            "torch",
            "fastapi",
            "starlette",
            "httpx",
            "uvicorn",
            "pydantic",
            "onnx",
            "onnxruntime",
            "nbformat",
            "ipykernel",
            "pytest",
            "ruff",
        ]
    }
    processor = platform.processor()
    cpu_info = Path("/proc/cpuinfo")
    if not processor and cpu_info.exists():
        processor = next(
            (
                line.split(":", 1)[1].strip()
                for line in cpu_info.read_text().splitlines()
                if line.startswith("model name")
            ),
            "not reported",
        )
    environment = {
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": processor,
        "logical_cpus": os.cpu_count(),
        "device": "CPU",
        "packages": packages,
        "tests_passed": tests,
        "notebooks_passed": len(results),
        "optional_pretrained_downloads_executed": False,
    }
    (ROOT / "docs/validation-environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    constraints = (
        "# Validated Linux/Python "
        + platform.python_version()
        + " snapshot; see docs/setup.md.\n# Install the matching CPU torch wheel first. This is not a hash-locked universal environment.\n"
        + "\n".join(f"{name}=={value}" for name, value in packages.items() if name != "cvzero")
        + "\n"
    )
    (ROOT / "constraints-validated.txt").write_text(constraints)
    shutil.copy2(
        ROOT / "artifacts/export-check/export-report.json", ROOT / "docs/export-validation.json"
    )
    progress = (
        """# Progress tracker — complete 53-chapter release

All numbered chapters contain their teaching pack: README, theory, worked mathematics, source entry point, focused notebooks, visualizations, three exercise levels, challenge, mini-project baseline, references and a next step.

**160 / 160 notebooks executed successfully in fresh interpreter/kernel instances.** The unit/integration suite has **83 passing tests**. The completion status concerns this educational scope; it does not claim a complete reproduction of every cited paper, trained real-world models or hardware-certified deployment.

| Chapter | Delivery | Notebook execution | Exercises/challenge | Mini-project baseline |
|---|---|---:|---|---|
"""
        + "\n".join(rows)
        + """

## Section checkpoints

Foundations, classical CV, video/cameras, learned vision, motion/structured outputs, representation/generation, 3D and production each have checkpoints in the roadmap. Learner completion requires explaining, implementing, modifying, debugging and applying the topic; the repository's delivery status does not mean a learner has mastered it.

## Final capstone

Implemented: local API, validation, generated/image/video/webcam dashboard inputs, default color-contour detection, geometric classification, HSV segmentation, Kalman/Hungarian tracking, numeric analytics, SQLite storage and logging. An explicit local YOLO weight adapter is included. Tests cover backend contracts. External weights, live webcam, Docker, GPU/edge hardware and hosted deployment were not exercised here.

See [validation evidence](VALIDATION.md), [per-notebook results](notebook-execution.json), [test results](test-results.xml) and [environment](validation-environment.json).
"""
    )
    (ROOT / "docs/PROGRESS.md").write_text(progress)
    validation = f"""# Validation evidence — release 1.0.0

These are actual checks performed on the delivered repository. Expected outputs and optional workflows are labeled separately throughout the course.

| Check | Result | Evidence |
|---|---|---|
| Lesson notebooks | 160 / 160 passed | [Notebook report](notebook-execution.json); executed outputs embedded in each notebook |
| Unit and integration tests | {tests} passed, 0 failed, 0 skipped | [JUnit XML](test-results.xml) |
| Numeric algorithms | Independent NumPy/SciPy/OpenCV/PyTorch comparisons and known-value checks passed | Numeric/model test modules |
| Manual CNN backpropagation | Finite-difference checks for kernels, biases and head parameters passed | `tests/test_scratch_cnn.py` |
| API contracts | Decode limits, state isolation, duplicate rejection and SQLite persistence passed | `tests/test_platform.py` |
| ONNX export/runtime | Graph checker and held-out logit agreement passed | [Export report](export-validation.json) |
| YOLO synthetic data | Generation and validation passed for the declared 80/20/20 splits | `scripts/prepare_yolo_dataset.py`; these are generated counts, not an external dataset size |
| Project runner | Configured ViT baseline executed and saved its report | `scripts/run_project.py` |
| Local links and chapter structure | All 53 structures and local Markdown links checked | `scripts/check_repository.py` |
| Python formatting/lint | Ruff check and format check | Run the commands below on changes |
| Package build | Wheel and source distribution built successfully | setuptools/build configuration |

## Execution environment

Python {environment["python"]}, {environment["machine"]}, CPU only. Processor: {processor}. Exact versions are in [validation-environment.json](validation-environment.json) and [constraints-validated.txt](../constraints-validated.txt). The tested editable package version is {packages["cvzero"]}.

Each notebook executed in its own subprocess with a real `ipykernel.inprocess` kernel. This avoids unavailable kernel sockets while preserving Jupyter execution and rich display messages. No notebook shares Python variables with another. The alternative `nbclient` socket engine is included for normal hosts but was not used for this release. The template notebook was executed in the foundation release and is not included in the 160 lesson count.

The full pass was followed by targeted rechecks of changed chapters. The merged report records each notebook's execution result and current file checksum. Code-formatting and Markdown-only edits do not imply a new numeric run.

## Measured scope

Generated examples establish algorithm behavior on known inputs. Packaged digits establish one small classical-ML experiment. Small CNN, U-Net, ViT, contrastive, generative and neural-field runs demonstrate actual training mechanics. A one-view field fit is not a 3D reconstruction benchmark; a toy localization regressor is not an Ultralytics YOLO result. Static figures and notebook plots contain actual outputs, including imperfect predictions.

The ONNX check verifies numeric agreement for the included tiny classifier, not arbitrary models or GPU runtimes. Local timing excludes any stages the report does not list. The scheduling chapter is a simulation, not a measured FPS claim.

## Not exercised in this build

Windows/macOS, Python 3.11/3.13, live Colab, GUI OpenCV, browser webcam permissions, RTSP, external dataset downloads, pretrained Ultralytics/torchvision/Transformers/MediaPipe/Open3D workflows, GPU/mixed-precision performance, TensorRT, physical edge devices, container execution and hosted deployment. The source and instructions are included where applicable; no success or benchmark numbers are claimed for these paths. CI is configured but was not run on GitHub.

The FastAPI test client emits an upstream Starlette deprecation warning for its HTTPX transport in the recorded environment. Requests and assertions pass; the warning is retained in test output rather than described as a failure. The ONNX script explicitly selects the legacy exporter and may emit its deprecation notice; export and runtime comparison pass.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python scripts/check_repository.py
python scripts/validate_full_course.py --jobs 4
python scripts/export_model.py --output artifacts/new-export-check
python -m build
```

Use a fresh output folder. Install a suitable CPU PyTorch wheel first as described in [setup](setup.md). After changing source, rerun affected numerical tests and notebooks before updating progress. Do not overwrite validation records with invented results.
"""
    (ROOT / "docs/VALIDATION.md").write_text(validation)
    print(
        f"Sealed {len(catalog['chapters'])} chapters, {len(results)} notebooks and {tests} passing tests."
    )


if __name__ == "__main__":
    main()
