# 45 · Depth Estimation

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Depth is distance along a stated camera axis or ray; the convention must be declared. Stereo geometry can recover metric depth from calibration, while monocular learned depth often has scale ambiguity or domain-dependent calibration.

## What You Will Learn

- Disparity and metric depth
- Depth uncertainty and invalid pixels
- Monocular priors and evaluation

## Why It Matters

Evaluate depth without pretending image estimates are measurements. In a rectified stereo pair, disparity is the horizontal pixel difference between matching points. Larger disparity usually means smaller depth. Focal length in pixels and baseline in physical units determine metric scale. Zero or negative disparity should be marked invalid, not converted into an invented finite distance.

## Prerequisites

[31 · Semantic Segmentation](../31-semantic-segmentation/README.md), [44 · 3D Computer Vision](../44-3d-computer-vision/README.md)

## Core Concepts

Metric vs relative depth, monocular cues, learned priors, uncertainty, depth metrics. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
Z=fB/d
$$

Z is depth, f focal length in pixels, B baseline in meters and d disparity in pixels. With f=200 px, B=0.12 m and d=8 px, Z=3 m. Units cancel only when f and d share pixel units. A worked Python calculation is included in every notebook.

## Practical Examples

The lab generates a known depth surface, converts it to disparity, adds measured pixel noise and recovers depth with invalid-value masking. It also visualizes first-order uncertainty.

```bash
python -m cvzero.course --chapter 45 --lesson 0 --seed 42 --output artifacts/ch45-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Disparity and metric depth](notebooks/01_foundations.ipynb)
- [2. Depth uncertainty and invalid pixels](notebooks/02_mechanisms.ipynb)
- [3. Monocular priors and evaluation](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Depth Inspector](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A visually smooth depth map can be consistently wrong in scale. Depth Z and Euclidean range are different away from the optical axis.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does disparity and metric depth solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Add the same disparity noise at 2 m and 6 m. Compare depth MAE and explain the nonlinear difference. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A visually smooth depth map can be consistently wrong in scale. Depth Z and Euclidean range are different away from the optical axis. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Depth Inspector into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-45) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/dd/d53/tutorial_py_depthmap.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[46 · Stereo Vision](../46-stereo-vision/README.md)
