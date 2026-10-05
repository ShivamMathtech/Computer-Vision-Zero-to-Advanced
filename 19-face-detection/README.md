# 19 · Face Detection

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Face detection locates face-like regions. It does not identify a person, estimate trustworthiness or infer sensitive traits. Classical and learned detectors use different representations, but all require careful evaluation across pose, lighting, scale and the intended population.

## What You Will Learn

- Integral images and Haar features
- HOG and sliding-window detectors
- Modern detectors and evaluation

## Why It Matters

Evaluate face boxes on consented examples without identity claims. An integral image stores the cumulative sum above and to the left of each position. Rectangle sums then require four array accesses, which makes Haar rectangle features inexpensive. A cascade rejects easy negative windows early and spends more computation on promising regions. Its learned thresholds come from training examples, not the integral-image formula itself.

## Prerequisites

[09 · Feature Detection](../09-feature-detection/README.md), [12 · Contours and Shapes](../12-contours-and-shapes/README.md), [15 · Video Processing](../15-video-processing/README.md)

## Core Concepts

Haar cascades, HOG, modern detectors, bounding boxes, confidence, failure modes. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
S(x,y)=\sum_{u\le x,v\le y}I(u,v)
$$

S is an integral image and I the original intensity. A padded integral image makes rectangle sums uniform. For the 2×2 values [[1,2],[3,4]], the full rectangle sum is 10. A worked Python calculation is included in every notebook.

## Practical Examples

The lab visualizes an integral image, orientation histograms and actual cascade boxes. Empty detections are a valid outcome on the synthetic cartoon.

```bash
python -m cvzero.course --chapter 19 --lesson 0 --seed 42 --output artifacts/ch19-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Integral images and Haar features](notebooks/01_foundations.ipynb)
- [2. HOG and sliding-window detectors](notebooks/02_mechanisms.ipynb)
- [3. Modern detectors and evaluation](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Consented Face Detection Demo](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A detected box is not proof that a person is present. Cascade scores should not be treated as calibrated probabilities.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does integral images and haar features solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Test how resizing and contrast affect a detector on a small consented evaluation set; include empty scenes and partial occlusions. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A detected box is not proof that a person is present. Cascade scores should not be treated as calibrated probabilities. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Consented Face Detection Demo into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-19) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[20 · Face Recognition](../20-face-recognition/README.md)
