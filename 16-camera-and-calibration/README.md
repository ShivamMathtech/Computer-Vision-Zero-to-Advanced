# 16 · Camera and Calibration

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Calibration estimates how a camera maps three-dimensional points to image pixels. Intrinsics describe the camera coordinate system and pixel scaling; extrinsics describe camera pose relative to a world frame. Lens distortion adds departures from the ideal pinhole model.

## What You Will Learn

- Pinhole cameras and intrinsics
- Chessboard calibration and reprojection
- Distortion, undistortion and validation

## Why It Matters

Calibrate a camera and validate on held-out board views. The intrinsic matrix contains horizontal and vertical focal lengths in pixels and the principal point. Rotation and translation place a world point in camera coordinates. Perspective division makes distant objects appear smaller. Physical focal length in millimeters cannot be substituted for focal length in pixels without sensor scaling.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [07 · Geometric Transformations](../07-geometric-transformations/README.md)

## Core Concepts

Pinhole model, intrinsics, extrinsics, distortion, chessboard, reprojection error, undistortion. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
u=f_xX/Z+c_x,\qquad v=f_yY/Z+c_y
$$

X,Y,Z are camera-frame coordinates, fx,fy focal lengths in pixels, and cx,cy principal point. With X=0.2 m, Z=2 m, fx=400 px and cx=320 px, u=360 px. A worked Python calculation is included in every notebook.

## Practical Examples

The synthetic lab projects a grid through known intrinsics and poses, adds pixel noise and calls calibrateCamera. The reported parameter error is meaningful because synthetic truth is available.

```bash
python -m cvzero.course --chapter 16 --lesson 0 --seed 42 --output artifacts/ch16-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Pinhole cameras and intrinsics](notebooks/01_foundations.ipynb)
- [2. Chessboard calibration and reprojection](notebooks/02_mechanisms.ipynb)
- [3. Distortion, undistortion and validation](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Camera Calibration Toolkit](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Chessboard dimensions count inner corners, not squares. Mixing units changes estimated translations and baseline scale.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does pinhole cameras and intrinsics solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Use many nearly identical front-facing board views versus varied views. Compare parameter stability, not just training reprojection error. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Chessboard dimensions count inner corners, not squares. Mixing units changes estimated translations and baseline scale. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Camera Calibration Toolkit into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-16) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[17 · Motion Detection](../17-motion-detection/README.md)
