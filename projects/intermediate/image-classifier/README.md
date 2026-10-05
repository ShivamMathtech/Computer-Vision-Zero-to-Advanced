# Image Classifier

## Problem Statement

Build a three-class image classifier with an error gallery, calibrated validation threshold and a documented unknown-image policy.

This folder includes a runnable, inspectable baseline. The open-ended extension asks you to generalize and evaluate it; the baseline is not presented as a completed real-world research result.

## Objectives

- Train and evaluate a small CNN before adapting a real ImageFolder dataset.
- Measure a declared quality criterion and inspect failure cases.
- Save configuration, plots and measured results for reproduction.

## Architecture

The entry point calls the shared chapter implementation in `deep.py`. Data generation and numeric/model code are separate from plotting and reporting. [Implementation](../../../src/cvzero/course/deep.py).

## System Flow

Load configuration → generate or validate data → compute prediction/transformation → evaluate → save arrays, metrics and visual report. Consult the source for the active experiment's exact steps.

## Dataset

The baseline generates its own data with seed 42; Chapter 22 uses scikit-learn's packaged digit dataset. No large data or pretrained weights are bundled. [Dataset catalog and preparation](../../../datasets/README.md). Use separate acquisition groups for real train, validation and test splits.

## Installation

From the repository root:

```bash
python -m pip install -e ".[notebooks,deep,api]"
```

CPU is sufficient for the baseline. Larger real-data model training can benefit from a GPU; no CUDA device is required here.

## Folder Structure

`README.md` explains the project; `config.json` defines the run; `run.py` launches it. Generated outputs contain `metrics.json`, `arrays.npz` and `result.png`. Reusable algorithms live in `src/cvzero/course/`.

## Configuration

Read `config.json` before running. It selects chapter 25, lesson 2, seed 42 and amount 1.0. `amount` only affects a parameter when that experiment uses it; exact model, optimizer, batch size and epochs are visible in the shared source and notebook source display. [Experiment protocol](../../../docs/reproducibility.md).

## Training

For learned baselines, the runner performs the short CPU training experiment and reports its actual loss. For deterministic image/geometry methods, there is no training stage: choose parameters on validation examples. Checkpointed real-data classification and opt-in pretrained workflows are documented in [external workflows](../../../docs/external-workflows.md).

## Evaluation

Create a background-only class and inspect whether confidence on unknown objects falls. Compare macro and micro metrics under class imbalance.

Use the metrics' exact names and the report's scope notes. Distinguish training loss, held-out synthetic evaluation and external-dataset evaluation. Never choose a final threshold on the test set.

## Inference

```bash
python scripts/run_project.py --config projects/intermediate/image-classifier/config.json --output artifacts/25-project-run
```

Use a new or empty output folder. For direct inference on user images with optional pretrained models, follow the external workflow instructions.

## Results

The chapter's `assets/lab-metrics.json` records a baseline run and its environment. Your run produces a fresh report. No accuracy or FPS is guaranteed; synthetic and local timing results have the scope stated in the report.

## Screenshots

![Actual baseline output](../../../25-image-classification/assets/lab-preview.png)

## Limitations

Softmax forces scores to sum to one even for an out-of-distribution image. A confident prediction is not proof that the image belongs to a known class. The synthetic baseline is deliberately small and does not establish reliability on unobserved data, hardware or users.

## Future Improvements

Complete the problem statement on a documented real dataset, add the failure cases from the chapter, and compare one justified alternative under identical splits and compute conditions. Advanced projects should progress through tests, held-out evaluation, optimization, deployment and monitoring.

## References

- [Primary documentation or paper](https://docs.pytorch.org/vision/stable/models.html)
- [Reproducibility and reporting](../../../docs/reproducibility.md)

## Example commands

```bash
python scripts/run_project.py --config projects/intermediate/image-classifier/config.json --output artifacts/25-seed43 --seed 43
```

## Expected output

A `Saved measured report` message and three output files: `result.png`, `metrics.json`, `arrays.npz`. The image shows the actual current run. Metric values depend on the seed, versions, algorithm and hardware; they are not fabricated sample scores.

## Project-specific extension

Train and evaluate a small CNN before adapting a real ImageFolder dataset.

The shipped command runs the chapter baseline. Complete the real-data extension with a documented dataset, independent evaluation and the optional adapters where appropriate. The research projects provide executable baselines and experimental protocols, not claims of new scientific results.
