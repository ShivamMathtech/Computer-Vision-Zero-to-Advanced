# 07 · Geometric Transformations

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

Geometric transformations move coordinates rather than directly changing intensity. A camera sees perspective, while image editing may only need translation or rotation. Separating coordinate mapping from interpolation explains why correct geometry can still produce blurry pixels.

## What You Will Learn

- Translation, rotation and inverse mapping
- Homographies from correspondences
- Interpolation and document rectification

## Why It Matters

Map coordinates correctly and control resampling artifacts. Translation adds an offset; rotation mixes x and y around a chosen center. Homogeneous coordinates append a one, allowing translation and linear transformation in a single matrix. Image warping usually asks which source position produced each destination pixel, avoiding holes that forward scatter can leave.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [04 · OpenCV Fundamentals](../04-opencv-fundamentals/README.md)

## Core Concepts

Resize, crop, flip, rotation, translation, interpolation, homogeneous coordinates, affine, perspective. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\tilde p\prime=H\tilde p,\qquad p\prime=(q_x/q_z,q_y/q_z)
$$

p is an input point, the tilde appends a homogeneous one, H is a 3×3 map and q is the resulting homogeneous vector. Translation by (3,−2) sends (4,5) to (7,3). Divide by the third coordinate after a perspective map. A worked Python calculation is included in every notebook.

## Practical Examples

The reference normalizes point clouds, builds the DLT design matrix, takes the last right singular vector and denormalizes H. OpenCV warpPerspective then performs sampling with that matrix.

```bash
python -m cvzero.course --chapter 7 --lesson 0 --seed 42 --output artifacts/ch07-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Translation, rotation and inverse mapping](notebooks/01_foundations.ipynb)
- [2. Homographies from correspondences](notebooks/02_mechanisms.ipynb)
- [3. Interpolation and document rectification](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Document Rectifier](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A homography cannot generally align a scene with multiple depths under translation. Wrong corner order can fold the page across itself.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does translation, rotation and inverse mapping solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Perturb one corner by two pixels and visualize the interior displacement. Compare nearest and bilinear interpolation on a checkerboard. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A homography cannot generally align a scene with multiple depths under translation. Wrong corner order can fold the page across itself. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Document Rectifier into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-07) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[08 · Color Spaces](../08-color-spaces/README.md)
