# 47 · Point Clouds

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

A point cloud is a set of 3D samples, often with color, normals or confidence. Unlike an image, it has no guaranteed regular grid. Sampling density, outliers and coordinate conventions affect every downstream geometric operation.

## What You Will Learn

- Backprojection and point-cloud structure
- Voxel sampling and nearest neighbors
- Rigid alignment and ICP

## Why It Matters

Construct and inspect point clouds with units and frame labels. A depth map can be backprojected through inverse intrinsics to produce camera-frame points. Filter invalid depth before geometric processing. PLY and other point formats may carry color and normals. Units and frame names must accompany files because coordinates alone do not reveal whether values are meters or millimeters.

## Prerequisites

[44 · 3D Computer Vision](../44-3d-computer-vision/README.md), [46 · Stereo Vision](../46-stereo-vision/README.md)

## Core Concepts

Back-projection, filtering, normals, registration, ICP, Open3D. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\min_{R,t}\sum_i\lVert Rp_i+t-q_i\rVert^2
$$

pi and qi are paired 3D points, R a proper rotation and t translation. If every target equals its source plus [1,0,0], identity rotation and that translation give zero residual. A worked Python calculation is included in every notebook.

## Practical Examples

The lab compares exact paired rigid fitting with iterative unpaired ICP and plots voxel-reduced points. The optional Open3D workflow reads and writes real point-cloud files.

```bash
python -m cvzero.course --chapter 47 --lesson 0 --seed 42 --output artifacts/ch47-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Backprojection and point-cloud structure](notebooks/01_foundations.ipynb)
- [2. Voxel sampling and nearest neighbors](notebooks/02_mechanisms.ipynb)
- [3. Rigid alignment and ICP](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Point Cloud Workshop](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

ICP residual can be small for an incorrect symmetric alignment. Voxel size has physical units and must match the cloud scale.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does backprojection and point-cloud structure solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Increase initial rotation and partial overlap to find ICP failures. Compare point count and geometric detail at several voxel sizes. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

ICP residual can be small for an incorrect symmetric alignment. Voxel size has physical units and must match the cloud scale. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Point Cloud Workshop into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-47) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[48 · Neural Radiance Fields](../48-neural-radiance-fields/README.md)
