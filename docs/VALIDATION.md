# Validation evidence — release 1.0.0

These are actual checks performed on the delivered repository. Expected outputs and optional workflows are labeled separately throughout the course.

| Check | Result | Evidence |
|---|---|---|
| Lesson notebooks | 160 / 160 passed | [Notebook report](notebook-execution.json); executed outputs embedded in each notebook |
| Unit and integration tests | 83 passed, 0 failed, 0 skipped | [JUnit XML](test-results.xml) |
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

Python 3.12.14, x86_64, CPU only. Processor: x86_64. Exact versions are in [validation-environment.json](validation-environment.json) and [constraints-validated.txt](../constraints-validated.txt). The tested editable package version is 1.0.0.

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
