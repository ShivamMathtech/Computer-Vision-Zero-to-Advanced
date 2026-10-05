# 44 · 3D Computer Vision

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Three-dimensional vision connects world geometry to image measurements. A single image loses depth through projection; multiple views and assumptions can constrain it. Coordinate frames, units and calibration are as important as the reconstruction algorithm.

## What You Will Learn

- World, camera and image coordinates
- Epipolar geometry and triangulation
- Reprojection and reconstruction error

## Why It Matters

Recover geometry while tracking coordinate frames and scale ambiguity. A rigid pose uses a rotation matrix and translation to map coordinates between frames. Rotation preserves lengths and has determinant +1. The camera projects camera-frame XYZ through intrinsics and perspective division. Be explicit whether a transform maps world to camera or camera to world; their translations are not interchangeable.

## Prerequisites

[07 · Geometric Transformations](../07-geometric-transformations/README.md), [16 · Camera and Calibration](../16-camera-and-calibration/README.md), [35 · Optical Flow](../35-optical-flow/README.md)

## Core Concepts

Camera matrices, rotation, translation, projection, epipolar geometry, triangulation, pose. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\tilde p\sim K[R\mid t]\tilde X
$$

X̃ is a homogeneous world point, R,t map world to camera, K contains intrinsics and p̃ is homogeneous image position. The symbol ∼ means equal up to a nonzero scale. Dividing by depth yields pixel coordinates. A worked Python calculation is included in every notebook.

## Practical Examples

The reference builds four linear equations per correspondence and solves a homogeneous least-squares problem by SVD. OpenCV triangulation is compared under identical camera matrices.

```bash
python -m cvzero.course --chapter 44 --lesson 0 --seed 42 --output artifacts/ch44-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. World, camera and image coordinates](notebooks/01_foundations.ipynb)
- [2. Epipolar geometry and triangulation](notebooks/02_mechanisms.ipynb)
- [3. Reprojection and reconstruction error](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Two-View Geometry Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Low reprojection error alone does not fix scale or guarantee accurate depth. Mixing left-handed and right-handed frames can mirror a reconstruction.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does world, camera and image coordinates solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Reduce the baseline while holding pixel noise fixed and measure how 3D error changes. Include points at several depths. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Low reprojection error alone does not fix scale or guarantee accurate depth. Mixing left-handed and right-handed frames can mirror a reconstruction. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Two-View Geometry Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-44) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[45 · Depth Estimation](../45-depth-estimation/README.md)
