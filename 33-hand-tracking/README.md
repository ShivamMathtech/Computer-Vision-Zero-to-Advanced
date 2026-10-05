# 33 · Hand Tracking

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Hand tracking combines landmark detection, temporal consistency and a gesture interpretation layer. Landmarks provide coordinates; a gesture controller still needs normalization, state and debouncing. Image-space motion should not automatically become an operating-system action.

## What You Will Learn

- Hand landmarks and normalized geometry
- Pinch and finger gesture features
- Stable interaction and virtual pointers

## Why It Matters

Convert landmarks into reversible desktop interactions. A common hand model uses 21 landmarks, including wrist and finger joints. Coordinates may be normalized to image dimensions and depth may use a model-specific scale. Finger numbering is an API contract, not something to infer from drawing order. Handedness can be affected by mirrored camera views.

## Prerequisites

[18 · Object Tracking](../18-object-tracking/README.md), [32 · Pose Estimation](../32-pose-estimation/README.md)

## Core Concepts

Hand landmarks, angles, gestures, smoothing, calibration, interaction. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
r=\lVert p_{thumb}-p_{index}\rVert/\lVert p_{wrist}-p_{middle}\rVert
$$

r is a scale-normalized pinch ratio. If fingertip distance is 10 pixels and reference hand length 80 pixels, r=0.125. A zero reference length makes the feature invalid. A worked Python calculation is included in every notebook.

## Practical Examples

Synthetic landmarks make indexing, distance normalization and pointer mapping inspectable. No live hand accuracy or OS-control behavior is claimed by the default lab.

```bash
python -m cvzero.course --chapter 33 --lesson 0 --seed 42 --output artifacts/ch33-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Hand landmarks and normalized geometry](notebooks/01_foundations.ipynb)
- [2. Pinch and finger gesture features](notebooks/02_mechanisms.ipynb)
- [3. Stable interaction and virtual pointers](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Virtual Pointer Simulator](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Raw pixel thresholds change with distance from the camera. Mirroring the display without adjusting coordinates reverses interaction.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does hand landmarks and normalized geometry solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Scale all landmark coordinates by two and verify that a normalized pinch ratio stays constant. Add noise and inspect click stability. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Raw pixel thresholds change with distance from the camera. Mirroring the display without adjusting coordinates reverses interaction. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Virtual Pointer Simulator into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-33) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[34 · Action Recognition](../34-action-recognition/README.md)
