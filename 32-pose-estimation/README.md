# 32 · Pose Estimation

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Pose estimation locates keypoints such as joints. A skeleton connects selected keypoints into a geometric structure. The output can support motion visualization or repetition counting, but visibility, projection and landmark uncertainty limit interpretation.

## What You Will Learn

- Keypoint heatmaps and coordinates
- Joint angles and skeleton geometry
- Temporal states and exercise counting

## Why It Matters

Visualize joints with uncertainty and safe exercise feedback. A heatmap gives a spatial score for one keypoint. Argmax picks its peak; soft-argmax computes an expected coordinate under normalized scores. Temperature controls concentration. Multiple peaks can make the expectation fall between plausible locations, so confidence and multimodality matter.

## Prerequisites

[24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [27 · Object Detection](../27-object-detection/README.md)

## Core Concepts

Keypoints, skeletons, heatmaps, confidence, coordinate conversion, visibility. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\theta=\arccos\left(\frac{u\cdot v}{\lVert u\rVert\lVert v\rVert}\right)
$$

u and v are limb vectors from the joint and θ their angle. Perpendicular vectors [1,0] and [0,1] give 90 degrees. Clamp the cosine to [−1,1] to handle floating-point roundoff. A worked Python calculation is included in every notebook.

## Practical Examples

Heatmap decoding, angle computation and hysteresis are separate functions so each can be inspected and tested independently of a pose detector.

```bash
python -m cvzero.course --chapter 32 --lesson 0 --seed 42 --output artifacts/ch32-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Keypoint heatmaps and coordinates](notebooks/01_foundations.ipynb)
- [2. Joint angles and skeleton geometry](notebooks/02_mechanisms.ipynb)
- [3. Temporal states and exercise counting](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Exercise Counter](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A keypoint detector does not diagnose posture or health. Occluded joints can be guessed incorrectly.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does keypoint heatmaps and coordinates solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Add angular noise around the thresholds and compare a single threshold with hysteresis. Include an incomplete repetition. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A keypoint detector does not diagnose posture or health. Occluded joints can be guessed incorrectly. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Exercise Counter into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-32) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/python) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[33 · Hand Tracking](../33-hand-tracking/README.md)
