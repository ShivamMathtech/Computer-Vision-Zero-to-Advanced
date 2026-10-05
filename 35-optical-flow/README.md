# 35 · Optical Flow

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Optical flow estimates apparent pixel motion between frames. It is a dense or sparse correspondence field, not a semantic object tracker. Brightness constancy and local motion assumptions make the problem tractable but can fail under illumination change, occlusion or large motion.

## What You Will Learn

- Brightness constancy and the aperture problem
- Lucas–Kanade least squares
- Pyramids and dense flow

## Why It Matters

Estimate apparent motion and test its assumptions. Brightness constancy assumes a moving scene point keeps approximately the same image intensity. Linearizing this assumption gives one equation for two motion components, so a single pixel is underdetermined. Along a straight edge, only motion perpendicular to the edge is locally observable: this is the aperture problem.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [13 · Edge and Corner Detection](../13-edge-and-corner-detection/README.md), [15 · Video Processing](../15-video-processing/README.md), [18 · Object Tracking](../18-object-tracking/README.md)

## Core Concepts

Brightness constancy, image derivatives, Lucas-Kanade, pyramids, dense flow, aperture problem. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
I_xu+I_yv+I_t=0
$$

Ix,Iy are spatial intensity derivatives, It the temporal derivative and u,v the small displacement components. If Ix=2, Iy=0 and It=−4, horizontal displacement u=2 satisfies the equation, while v remains unconstrained. A worked Python calculation is included in every notebook.

## Practical Examples

The reference builds gradient equations and solves least squares. Library comparisons use pyramidal Lucas–Kanade and Farneback; their assumptions and support differ.

```bash
python -m cvzero.course --chapter 35 --lesson 0 --seed 42 --output artifacts/ch35-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Brightness constancy and the aperture problem](notebooks/01_foundations.ipynb)
- [2. Lucas–Kanade least squares](notebooks/02_mechanisms.ipynb)
- [3. Pyramids and dense flow](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Flow Visualization Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A colorful flow image can look plausible even when magnitudes are wrong. Use endpoint error against known displacement.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does brightness constancy and the aperture problem solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Increase translation until the small-motion estimate fails, then compare with pyramidal tracking. Add a uniform brightness offset as a separate failure test. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A colorful flow image can look plausible even when magnitudes are wrong. Use endpoint error against known displacement. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Flow Visualization Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-35) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[36 · Multi-Object Tracking](../36-multi-object-tracking/README.md)
