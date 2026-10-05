# 48 · Neural Radiance Fields

**Research · CPU baseline · 3 focused notebooks · no required downloads**

A neural radiance field represents a scene with a function that predicts density and appearance at spatial locations and viewing directions. Rendering integrates samples along camera rays. The representation learns through images, but geometric identifiability depends on the available views.

## What You Will Learn

- Rays, density and positional encoding
- Volume rendering and transmittance
- Fit a tiny radiance field

## Why It Matters

Train a tiny synthetic scene and separate camera errors from model errors. A ray starts at a camera origin and advances along a direction. A network can map sampled positions and view directions to density and color. Positional encoding supplies sinusoidal features to represent spatial variation. The local model uses positions only, so it cannot model full view-dependent appearance.

## Prerequisites

[24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [42 · Generative Computer Vision](../42-generative-computer-vision/README.md), [44 · 3D Computer Vision](../44-3d-computer-vision/README.md), [47 · Point Clouds](../47-point-clouds/README.md)

## Core Concepts

Rays, radiance, density, volume rendering, positional encoding, view synthesis, alternatives. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
C=\sum_i T_i(1-e^{-\sigma_i\Delta_i})c_i
$$

σi is density, Δi sample interval, ci color and Ti transmittance before sample i. One sample with opacity 0.5, black color and white background yields final intensity 0.5 after adding the background term. A worked Python calculation is included in every notebook.

## Practical Examples

The field uses sinusoidal position features, an MLP and nonnegative density. The differentiable renderer accumulates opacity and transmittance, then a pixel MSE trains the field.

```bash
python -m cvzero.course --chapter 48 --lesson 0 --seed 42 --output artifacts/ch48-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Rays, density and positional encoding](notebooks/01_foundations.ipynb)
- [2. Volume rendering and transmittance](notebooks/02_mechanisms.ipynb)
- [3. Fit a tiny radiance field](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Tiny NeRF Study](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Low training-image loss does not prove correct 3D geometry. Ignoring background transmittance darkens empty rays.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does rays, density and positional encoding solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Hold out a camera view in an extended multiview experiment and compare its error with training-view error. Inspect whether density is plausible or merely explains one view. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Low training-image loss does not prove correct 3D geometry. Ignoring background transmittance darkens empty rays. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Tiny NeRF Study into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-48) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/2003.08934) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[49 · Model Optimization](../49-model-optimization/README.md)
