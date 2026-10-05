# 02 · Mathematics for Computer Vision

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

Computer vision turns measurements into arrays and optimizes rules over those arrays. A scalar is one number; a vector is an ordered list; a matrix is a rectangular table. The same notation will later describe pixels, camera coordinates, weights and gradients.

## What You Will Learn

- Arrays, linear maps and eigenvectors
- Derivatives, gradients and optimization
- Probability, statistics and frequency

## Why It Matters

Translate small equations into array operations before using models. A dot product multiplies corresponding entries and adds them: it measures alignment. Matrix multiplication combines rows with columns and composes linear maps. An eigenvector keeps its direction under a map; its eigenvalue is the scale factor. Symmetric covariance matrices have orthogonal eigenvectors, which makes PCA a rotation toward directions of variation.

## Prerequisites

[01 · Python for Computer Vision](../01-python-for-computer-vision/README.md)

## Core Concepts

Scalars, vectors, matrices, functions, derivatives, gradients, probability, statistics, optimization, eigenvectors, Fourier basics. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
w_{t+1}=w_t-\eta\,2(w_t-1)
$$

For loss L(w)=(w−1)², w is the current parameter, t the update number and η the positive learning rate. At w=3 and η=0.1, the gradient is 4, so the next value is 2.6. A worked Python calculation is included in every notebook.

## Practical Examples

The lab checks an eigendecomposition numerically, compares finite differences with an analytic derivative, and detects a sinusoid through an FFT. The FFT uses complex coefficients; magnitude discards phase.

```bash
python -m cvzero.course --chapter 2 --lesson 0 --seed 42 --output artifacts/ch02-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Arrays, linear maps and eigenvectors](notebooks/01_foundations.ipynb)
- [2. Derivatives, gradients and optimization](notebooks/02_mechanisms.ipynb)
- [3. Probability, statistics and frequency](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Visual Math Workbook](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Elementwise multiplication A*B is not matrix multiplication A@B. A low loss after one example says nothing about generalization.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does arrays, linear maps and eigenvectors solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Change the gradient-descent step from 0.1 to 0.3, then derive the stability interval for the quadratic before trying a larger step. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Elementwise multiplication A*B is not matrix multiplication A@B. A low loss after one example says nothing about generalization. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Visual Math Workbook into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-02) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://numpy.org/doc/stable/reference/routines.linalg.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[03 · Image Fundamentals](../03-image-fundamentals/README.md)
