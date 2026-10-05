# 10 · Feature Description and Matching

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

A descriptor turns a neighborhood into a vector or bit string. Matching asks which vectors likely describe the same physical point. A nearest neighbor is only a proposal: geometry is needed to reject accidental visual similarities.

## What You Will Learn

- Descriptors and distance metrics
- Ratio tests and robust correspondence
- RANSAC homography and stitching

## Why It Matters

Reject false matches before estimating a geometric map. SIFT descriptors are floating-point histograms, commonly compared with Euclidean distance. ORB descriptors are binary strings, compared with Hamming distance. BFMatcher checks descriptor pairs directly; FLANN uses approximate search structures suited to the descriptor type. A mismatch between descriptor type and distance changes the meaning of similarity.

## Prerequisites

[07 · Geometric Transformations](../07-geometric-transformations/README.md), [09 · Feature Detection](../09-feature-detection/README.md)

## Core Concepts

Descriptors, BFMatcher, FLANN, distance metrics, ratio test, RANSAC, homography. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
d_1/d_2<\tau
$$

d1 is the nearest descriptor distance, d2 the second nearest and τ the chosen ratio threshold. Distances 12 and 30 produce 0.4 and pass τ=0.75. Zero second-neighbor distance is ambiguous and should not be divided blindly. A worked Python calculation is included in every notebook.

## Practical Examples

The lab detects ORB or SIFT features in a generated texture and its translated view, filters matches, estimates a RANSAC homography and compares translation with known truth.

```bash
python -m cvzero.course --chapter 10 --lesson 0 --seed 42 --output artifacts/ch10-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Descriptors and distance metrics](notebooks/01_foundations.ipynb)
- [2. Ratio tests and robust correspondence](notebooks/02_mechanisms.ipynb)
- [3. RANSAC homography and stitching](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Image Stitching System](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Drawing many lines between two images can conceal false correspondences. A low residual on a tiny cluster of points may extrapolate badly.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does descriptors and distance metrics solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Add repeated tiles and increase viewpoint change. Record keypoints, accepted matches, inliers and reprojection error separately. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Drawing many lines between two images can conceal false correspondences. A low residual on a tiny cluster of points may extrapolate badly. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Image Stitching System into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-10) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[11 · Morphological Image Processing](../11-morphological-image-processing/README.md)
