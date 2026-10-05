# 03 · Image Fundamentals

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

Imagine an image as a spreadsheet. A grayscale cell holds one intensity; an RGB pixel holds three channel values. Sampling chooses where measurements are taken, and quantization chooses which intensity values can be represented. The array is the measurement, not the scene itself.

## What You Will Learn

- Pixels, coordinates and channels
- Bit depth and quantization error
- Resolution, alpha and tensor layout

## Why It Matters

Explain sampling, quantization and image memory. Array indexing uses row then column, so image[y, x] is a pixel at horizontal position x and vertical position y. RGB has three channels; RGBA adds alpha, an opacity value. Grayscale is a weighted summary of color, not simply the first channel. OpenCV commonly stores BGR while plotting libraries expect RGB.

## Prerequisites

[01 · Python for Computer Vision](../01-python-for-computer-vision/README.md), [02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md)

## Core Concepts

Pixels, resolution, RGB, RGBA, grayscale, channels, bit depth, metadata, tensors. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
C=\alpha F+(1-\alpha)B
$$

C is the composited channel, F foreground intensity, B background intensity, and α opacity between zero and one. Half-opacity red over white gives RGB [1, 0.5, 0.5] in normalized units. A worked Python calculation is included in every notebook.

## Practical Examples

The experiments separate channels, quantize levels with rounding, resample the spatial grid and transpose axes. Image dimensions and memory size are measured from the actual array.

```bash
python -m cvzero.course --chapter 3 --lesson 0 --seed 42 --output artifacts/ch03-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Pixels, coordinates and channels](notebooks/01_foundations.ipynb)
- [2. Bit depth and quantization error](notebooks/02_mechanisms.ipynb)
- [3. Resolution, alpha and tensor layout](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Image Inspector](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Pixel coordinates are not Cartesian world coordinates: y normally increases downward. Alpha is not another visible color channel.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does pixels, coordinates and channels solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Reduce the number of intensity levels while leaving resolution fixed. Then reduce resolution with all 256 levels. Describe how the two artifacts differ. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Pixel coordinates are not Cartesian world coordinates: y normally increases downward. Alpha is not another visible color channel. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Image Inspector into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-03) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[04 · OpenCV Fundamentals](../04-opencv-fundamentals/README.md)
