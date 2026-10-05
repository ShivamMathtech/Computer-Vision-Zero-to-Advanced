# 05 · Image Processing

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

Filtering replaces a pixel using its neighborhood. Think of a small window sliding across a spreadsheet. The weights in that window form a kernel. Different weights preserve, blur or emphasize different spatial patterns, and boundary handling changes the answer near image edges.

## What You Will Learn

- Correlation and weighted neighborhoods
- Gaussian noise and smoothing
- Impulse noise and nonlinear filters

## Why It Matters

Implement a sliding window and compare denoising methods. Correlation multiplies each neighborhood by a kernel and sums the products. Mathematical convolution flips the kernel first. OpenCV filter2D and deep-learning convolution layers implement correlation. Symmetric kernels hide the distinction. A mean filter assigns equal weight to every location; its weights sum to one so constant regions stay constant.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [04 · OpenCV Fundamentals](../04-opencv-fundamentals/README.md)

## Core Concepts

Convolution vs correlation, mean, Gaussian, median, bilateral, Gaussian noise, salt-and-pepper, speckle. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
Y_{ij}=\sum_{u=-r}^{r}\sum_{v=-r}^{r}K_{uv}X_{i+u,j+v}
$$

X is the input, K the kernel, Y the result, and r the window radius. A 3×3 mean kernel has nine weights of 1/9. A neighborhood containing values 1 through 9 therefore produces 5. A worked Python calculation is included in every notebook.

## Practical Examples

The reference implementation pads explicitly and loops over pixels. OpenCV uses optimized kernels and vectorized hardware. Match dtype, correlation convention and border mode before comparing results.

```bash
python -m cvzero.course --chapter 5 --lesson 0 --seed 42 --output artifacts/ch05-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Correlation and weighted neighborhoods](notebooks/01_foundations.ipynb)
- [2. Gaussian noise and smoothing](notebooks/02_mechanisms.ipynb)
- [3. Impulse noise and nonlinear filters](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Image Restoration Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Smoothing may lower noise while removing a real small object. Numerical equality comparisons are invalid when border modes differ.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does correlation and weighted neighborhoods solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Use equal noise seeds to compare mean, Gaussian and median filtering. Report MSE against the clean synthetic image and also inspect whether thin edges disappear. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Smoothing may lower noise while removing a real small object. Numerical equality comparisons are invalid when border modes differ. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Image Restoration Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-05) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[06 · Image Enhancement](../06-image-enhancement/README.md)
