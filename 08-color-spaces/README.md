# 08 · Color Spaces

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

A color space is a coordinate system for color. RGB is convenient for displays, HSV separates hue from saturation and value, and LAB separates lightness from opponent color axes. Choosing a space can make a simple threshold useful, but it does not remove lighting variation.

## What You Will Learn

- RGB, BGR and channel conventions
- HSV color masks and hue wraparound
- LAB, YCrCb and robust thresholds

## Why It Matters

Isolate a colored object while testing illumination changes. RGB and BGR store the same three color components in different orders. Grayscale deliberately discards chromatic information. A channel is a measurement axis, not an object category. Verify the dtype-specific range whenever converting spaces; OpenCV integer encodings are not identical to textbook floating-point units.

## Prerequisites

[03 · Image Fundamentals](../03-image-fundamentals/README.md), [04 · OpenCV Fundamentals](../04-opencv-fundamentals/README.md)

## Core Concepts

RGB, BGR, HSV, LAB, YCrCb, grayscale, color thresholding, skin-color limitations. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
M=(h<h_1\;\lor\;h>h_2)\land(s>s_0)\land(v>v_0)
$$

M is a Boolean red mask, h hue, s saturation and v value. h1 and h2 bound the two sides of red; s0 and v0 reject gray and darkness. For h=178, s=200, v=150 and bounds 10,170,80,50, the mask is true. A worked Python calculation is included in every notebook.

## Practical Examples

Convert RGB to HSV once, threshold channels, combine hue intervals and clean the binary mask using morphology. A centroid can then drive a simple color tracker.

```bash
python -m cvzero.course --chapter 8 --lesson 0 --seed 42 --output artifacts/ch08-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. RGB, BGR and channel conventions](notebooks/01_foundations.ipynb)
- [2. HSV color masks and hue wraparound](notebooks/02_mechanisms.ipynb)
- [3. LAB, YCrCb and robust thresholds](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Color Object Tracker](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Using hue degrees 0–360 directly on OpenCV uint8 HSV produces incorrect thresholds. Skin color is not a reliable substitute for a trained hand detector.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does rgb, bgr and channel conventions solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Lower saturation while keeping hue fixed and observe the reliability of the red mask. Test two illuminations with the same object. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Using hue degrees 0–360 directly on OpenCV uint8 HSV produces incorrect thresholds. Skin color is not a reliable substitute for a trained hand detector. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Color Object Tracker into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-08) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[09 · Feature Detection](../09-feature-detection/README.md)
