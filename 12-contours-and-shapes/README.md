# 12 · Contours and Shapes

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

A contour traces a region boundary. Once a segmentation mask is available, contours convert pixels into geometric measurements: area, perimeter, enclosing boxes, convex hulls and polygon approximations. The measurement is only as reliable as the mask and scale calibration.

## What You Will Learn

- Contours, components and measurements
- Bounding rectangles and shape approximations
- Convexity and calibrated dimensions

## Why It Matters

Measure image shapes and distinguish pixels from physical units. Connected components label foreground regions; contours trace their boundaries. They answer related but different questions. A contour polygon area differs from counting foreground pixel centers, especially for small objects. Retrieval mode controls whether holes and nested boundaries are returned.

## Prerequisites

[07 · Geometric Transformations](../07-geometric-transformations/README.md), [11 · Morphological Image Processing](../11-morphological-image-processing/README.md)

## Core Concepts

Boundary, area, perimeter, bounding box, rotated box, convex hull, approximation. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
C=4\pi A/P^2
$$

C is circularity, A region area and P perimeter in consistent units. A continuous circle of radius 3 has area 9π and perimeter 6π, yielding C=1. Digitized contours generally differ from the continuous ideal. A worked Python calculation is included in every notebook.

## Practical Examples

OpenCV finds boundaries in the synthetic mask, measures each contour and overlays approximations and rotated boxes. Shape rules use measured values and expose ambiguous cases.

```bash
python -m cvzero.course --chapter 12 --lesson 0 --seed 42 --output artifacts/ch12-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Contours, components and measurements](notebooks/01_foundations.ipynb)
- [2. Bounding rectangles and shape approximations](notebooks/02_mechanisms.ipynb)
- [3. Convexity and calibrated dimensions](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Shape Measurement System](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Perspective changes apparent size. A fixed pixels-per-millimeter ratio cannot measure arbitrary depths.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does contours, components and measurements solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Rotate a rectangle and compare its axis-aligned box area with its minimum-area box. Add holes and inspect contour hierarchy. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Perspective changes apparent size. A fixed pixels-per-millimeter ratio cannot measure arbitrary depths. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Shape Measurement System into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-12) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[13 · Edge and Corner Detection](../13-edge-and-corner-detection/README.md)
