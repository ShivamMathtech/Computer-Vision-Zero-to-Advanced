# 09 · Feature Detection

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

A feature is a location with a pattern that can be found again. A uniform wall gives no precise location; a corner constrains movement in two directions. Feature detection chooses interesting points, while feature description records a neighborhood for later comparison.

## What You Will Learn

- Structure tensors and Harris corners
- Shi–Tomasi selection and suppression
- FAST, scale and detector tradeoffs

## Why It Matters

Find repeatable image locations and explain detector tradeoffs. The structure tensor summarizes products of horizontal and vertical gradients in a local window. Two small eigenvalues indicate a flat region; one large value indicates an edge; two large values indicate a corner. Harris combines determinant and trace into a score without explicitly computing both eigenvalues.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [05 · Image Processing](../05-image-processing/README.md)

## Core Concepts

Image derivatives primer, Harris, Shi-Tomasi, FAST, SIFT, ORB, scale and rotation. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
R=\det(M)-k\,\operatorname{trace}(M)^2
$$

M is the 2×2 sum of local gradient outer products, R the Harris response and k a sensitivity parameter. For eigenvalues 4 and 3, det=12 and trace=7; with k=0.04, R=10.04. A worked Python calculation is included in every notebook.

## Practical Examples

The reference computes Sobel gradients, smooths their products and forms the response. The library comparison applies detector-specific selection, so point sets need not be identical.

```bash
python -m cvzero.course --chapter 9 --lesson 0 --seed 42 --output artifacts/ch09-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Structure tensors and Harris corners](notebooks/01_foundations.ipynb)
- [2. Shi–Tomasi selection and suppression](notebooks/02_mechanisms.ipynb)
- [3. FAST, scale and detector tradeoffs](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Corner Explorer](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A high feature count is not proof of useful coverage. Border padding and threshold units influence the response.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does structure tensors and harris corners solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Rotate and blur a checkerboard. Count repeatable detections after transforming coordinates back, rather than comparing only raw detection counts. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A high feature count is not proof of useful coverage. Border padding and threshold units influence the response. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Corner Explorer into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-09) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/dc/d0d/tutorial_py_features_harris.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[10 · Feature Description and Matching](../10-feature-description-and-matching/README.md)
