# Pixel Lab — A Reproducible Image Laboratory

**Status: runnable in v1.0.0.** Prerequisite: Chapter 01. CPU only; no camera, GPU, model weights or external dataset.

## Problem Statement

A beginner can often display an image but cannot explain its values or safely reproduce an edit. Build an image laboratory that makes each transformation visible and records its parameters.

## Objectives

Load or generate an RGB image, crop it, adjust brightness and channels, produce grayscale, inspect channel histograms and save a portable report. Preserve inputs and prior runs. Compare implementations with measured arithmetic timings.

## Architecture

The CLI parses user settings; `LabConfig` validates numerical parameters; the loader establishes RGB `uint8`; pure functions transform arrays; the reporting layer writes images, statistics and a local HTML page. Tests cover numerical properties and input errors.

## System Flow

Input image or seeded synthetic scene → validated RGB array → optional crop → clipped brightness → clipped channel gains → grayscale/statistics/plots → PNG + JSON + HTML.

This order is part of the contract. Multiplying before clipping the brightness stage can produce a different output.

## Dataset

The default is `cvzero.synthetic.make_scene(seed=42)`, 160×240 RGB. Alternatively use a local single-frame 8-bit image you may process. Grayscale converts to RGB; transparency composites on white. Scientific/16-bit images require an explicit separate conversion. [Dataset policy](../../../datasets/README.md).

## Installation

From the repository root, activate a supported Python environment and run:

```bash
python -m pip install -r requirements.txt
python -m cvzero doctor
```

[Full Windows/macOS/Linux setup](../../../docs/setup.md).

## Folder Structure

| Location | Purpose |
| --- | --- |
| `src/cvzero/images.py` | Safe brightness, gains, crop, grayscale and statistics |
| `src/cvzero/io.py` | Load, validate and save files |
| `src/cvzero/lab.py` | Configuration, transformation and report |
| `src/cvzero/cli.py` | Command parsing and error exits |
| `projects/beginner/pixel-lab/run.py` | Convenience demo entry point |
| `tests/` | Numerical and integration validation |
| Your chosen `artifacts/RUN/` | Generated report outputs |

## Configuration

| Flag | Default | Meaning |
| --- | --- | --- |
| `--output` | Required | New or empty report folder |
| `--brightness` | 20 | Finite additive offset from -255 through 255 |
| `--gains R G B` | 1 1 1 | Per-channel multipliers from 0 through 4 |
| `--crop X0 Y0 X1 Y1` | Full image | Integer exclusive-stop crop within image bounds |
| `--seed` | 42 | Synthetic generator seed, for `demo` only |

A `summary.json` records these settings. Reusing a nonempty output folder returns a useful error; choose another run name.

## Training

Not applicable. Pixel Lab uses deterministic array operations and has no learned parameters. Do not invent a training curve or accuracy score for it.

## Evaluation

Run `python -m pytest -q` after installing development requirements. Inspect lossless PNG round trips, boundary clipping, input immutability, crop shape and histogram count conservation. Compare loop and vectorized brightness exactly. Allow a stated one-intensity-level tolerance against OpenCV's grayscale conversion.

## Inference / Example Commands

Here “inference” means applying the configured image transformation; no ML model runs.

```bash
python -m cvzero demo --output artifacts/run-01 --brightness 25 --gains 1.1 1.0 0.8
python -m cvzero edit datasets/synthetic/scene.png --output artifacts/run-02 --crop 20 10 180 120 --brightness -10
python -m cvzero inspect artifacts/run-02/edited.png
python -m cvzero benchmark --repeats 5 --output artifacts/run-01-benchmark.json
```

You can also run `python projects/beginner/pixel-lab/run.py --output artifacts/run-03` from the repository root. The package CLI works from any folder after installation.

## Expected Output

The report directory contains `original.png`, `edited.png`, `grayscale.png`, `contact-sheet.png`, `histograms.png`, `summary.json` and `report.html`. Open `report.html` in a browser. A benchmark command writes raw timing samples and medians to its specified JSON file.

## Results

The bundled [executed sample report](sample-output/report.html) shows output generated during release validation. Its [JSON](sample-output/summary.json) contains the actual configuration and environment. [Validation evidence](../../../docs/VALIDATION.md) reports which checks ran. Timings vary with hardware and load; no image-quality or ML-accuracy claim is made.

## Screenshots

![Executed synthetic Pixel Lab output](sample-output/contact-sheet.png)

## Limitations

Local static images only. It is an educational CLI with an HTML report, not a live GUI editor. It has no camera pipeline, model training, semantic understanding, advanced color management, scientific image scaling or production service. Clipping loses information. Arithmetic speed measurements do not measure end-to-end video performance.

## Future Improvements

Add a learner-designed batch audit, then study mathematical transforms in Chapter 02 and image representation in Chapter 03. Desktop interaction belongs in the later OpenCV chapter. Only add learned models after training and evaluation have been taught.

## References

[NumPy](https://numpy.org/doc/stable/user/quickstart.html), [OpenCV](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html), [Pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html), [repository references](../../../docs/references.md).
