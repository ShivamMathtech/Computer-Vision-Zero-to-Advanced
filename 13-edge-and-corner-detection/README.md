# 13 · Edge and Corner Detection

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Edges are rapid changes in image intensity. They often correspond to boundaries, but also arise from texture, shadows and noise. A derivative measures change; a good edge pipeline controls noise and decides which changes should form connected boundaries.

## What You Will Learn

- Gradients, Sobel and Scharr
- Laplacian and second derivatives
- Canny step by step

## Why It Matters

Construct a simplified Canny pipeline and evaluate noise effects. A horizontal derivative responds to left-right intensity change, and a vertical derivative responds to up-down change. Sobel combines differencing with smoothing. Scharr uses different coefficients to improve rotational behavior for small kernels. Gradient magnitude combines both responses; orientation is obtained with atan2.

## Prerequisites

[05 · Image Processing](../05-image-processing/README.md), [09 · Feature Detection](../09-feature-detection/README.md)

## Core Concepts

Gradients, Sobel, Scharr, Laplacian, Canny, non-maximum suppression, hysteresis. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
G=\sqrt{G_x^2+G_y^2},\qquad\theta=\operatorname{atan2}(G_y,G_x)
$$

Gx and Gy are horizontal and vertical derivatives, G their magnitude and θ edge-normal orientation. Derivatives (3,4) have magnitude 5 and orientation about 53.13 degrees. A worked Python calculation is included in every notebook.

## Practical Examples

Follow the NumPy implementation in order: Gaussian blur → Sobel → magnitude/orientation → directional suppression → two thresholds → queue-based hysteresis. Compare intermediate arrays, not only the final binary output.

```bash
python -m cvzero.course --chapter 13 --lesson 0 --seed 42 --output artifacts/ch13-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Gradients, Sobel and Scharr](notebooks/01_foundations.ipynb)
- [2. Laplacian and second derivatives](notebooks/02_mechanisms.ipynb)
- [3. Canny step by step](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Document Boundary Detector](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Edges are not closed object masks. Applying contours to a broken Canny map can produce fragmented shapes.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does gradients, sobel and scharr solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Increase noise and independently change blur scale and hysteresis thresholds. Observe missing boundaries versus false texture edges. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Edges are not closed object masks. Applying contours to a broken Canny map can produce fragmented shapes. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Document Boundary Detector into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-13) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[14 · Classical Segmentation](../14-segmentation-classical/README.md)
