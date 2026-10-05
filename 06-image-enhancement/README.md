# 06 · Image Enhancement

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

Enhancement changes appearance so a useful signal is easier to inspect or process. Brightness shifts intensity, contrast changes separation, and a histogram counts how often each intensity occurs. Enhancement should serve a task; a visually dramatic image is not automatically more informative.

## What You Will Learn

- Histograms and equalization
- Local contrast with CLAHE
- Gamma and unsharp masking

## Why It Matters

Choose an enhancement method using image evidence. A histogram ignores spatial arrangement and counts intensity values. Equalization maps intensities through a cumulative distribution so a narrow range spreads more widely. The implementation subtracts the first nonzero cumulative count so a dark lower endpoint maps to zero. A constant image needs special handling because there is no intensity range to expand.

## Prerequisites

[05 · Image Processing](../05-image-processing/README.md)

## Core Concepts

Brightness, contrast, histogram, equalization, CLAHE, gamma, sharpening. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
y=x^\gamma\quad (0\le x\le1)
$$

x is normalized input intensity, y the corrected intensity and γ the chosen exponent. With x=0.25 and γ=0.5, y=0.5. This definition must be stated because some tools expose reciprocal gamma. A worked Python calculation is included in every notebook.

## Practical Examples

The lab computes a NumPy CDF mapping, compares OpenCV equalization, then examines CLAHE and sharpening. The plotted histograms show counts, not probabilities unless normalized.

```bash
python -m cvzero.course --chapter 6 --lesson 0 --seed 42 --output artifacts/ch06-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Histograms and equalization](notebooks/01_foundations.ipynb)
- [2. Local contrast with CLAHE](notebooks/02_mechanisms.ipynb)
- [3. Gamma and unsharp masking](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Image Enhancement Studio](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Equalizing R, G and B independently can change hue. Clipping after sharpening discards values and can hide overshoot.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does histograms and equalization solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Increase CLAHE strength on a noisy flat region and quantify both local contrast and noise variance. Find a setting that improves the downstream threshold mask. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Equalizing R, G and B independently can change hue. Clipping after sharpening discards values and can hide overshoot. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Image Enhancement Studio into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-06) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[07 · Geometric Transformations](../07-geometric-transformations/README.md)
