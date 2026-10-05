# 11 · Morphological Image Processing

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

Morphology processes shape using a small structuring element. Imagine moving a stencil across a binary mask and asking whether any or all covered pixels are foreground. This provides controllable ways to remove specks, fill gaps and outline regions.

## What You Will Learn

- Erosion and dilation from scratch
- Opening and closing
- Gradients, top-hat and black-hat

## Why It Matters

Clean binary masks without destroying useful structure. Binary erosion keeps a pixel only when every active stencil position fits inside foreground. Dilation keeps it when any stencil position touches foreground. A disk, square and line encode different geometric assumptions. This lab uses a full square stencil and treats pixels outside the image as background.

## Prerequisites

[05 · Image Processing](../05-image-processing/README.md), [08 · Color Spaces](../08-color-spaces/README.md)

## Core Concepts

Structuring element, erosion, dilation, opening, closing, gradient, top-hat, black-hat. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
(A\ominus B)(p)=\bigwedge_{b\in B}A(p+b)
$$

A is a Boolean image, B the active stencil offsets, p the current pixel, and ∧ means all entries must be true. For a 3×3 all-foreground patch, erosion returns true; one missing entry makes it false. A worked Python calculation is included in every notebook.

## Practical Examples

The reference pads with false, scans square windows and evaluates all or any. OpenCV performs optimized morphology; border settings must match to compare edges.

```bash
python -m cvzero.course --chapter 11 --lesson 0 --seed 42 --output artifacts/ch11-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Erosion and dilation from scratch](notebooks/01_foundations.ipynb)
- [2. Opening and closing](notebooks/02_mechanisms.ipynb)
- [3. Gradients, top-hat and black-hat](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Document Cleanup Pipeline](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Opening can delete legitimate thin lines. The structuring element size should reflect object scale, not an arbitrary constant copied from another image.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does erosion and dilation from scratch solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Try a horizontal line stencil on broken text and compare it with a square stencil. Measure whether neighboring letters incorrectly merge. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Opening can delete legitimate thin lines. The structuring element size should reflect object scale, not an arbitrary constant copied from another image. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Document Cleanup Pipeline into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-11) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[12 · Contours and Shapes](../12-contours-and-shapes/README.md)
