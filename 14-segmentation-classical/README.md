# 14 · Classical Segmentation

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Segmentation assigns a label to each pixel. Classical methods use explicit assumptions about intensity, color or connectivity. They are useful baselines because their failure conditions are easier to inspect than those of a large trained model.

## What You Will Learn

- Global, adaptive and Otsu thresholds
- K-means color segmentation
- Connected components and region cleanup

## Why It Matters

Separate regions with explicit assumptions and evaluation. A threshold separates pixels above and below a cutoff. Otsu chooses a cutoff by maximizing between-class variance in the histogram. It works best when two intensity groups are meaningfully separable. Adaptive thresholding computes local cutoffs and can handle uneven illumination, but its neighborhood size introduces another scale assumption.

## Prerequisites

[08 · Color Spaces](../08-color-spaces/README.md), [11 · Morphological Image Processing](../11-morphological-image-processing/README.md), [13 · Edge and Corner Detection](../13-edge-and-corner-detection/README.md)

## Core Concepts

Thresholding, Otsu, adaptive threshold, connected components, k-means, watershed. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
J=\sum_i\lVert x_i-\mu_{c_i}\rVert^2
$$

xi is a pixel feature vector, ci its cluster assignment and μ the selected cluster center. For values [1,2] assigned to center 1.5, the summed squared distance is 0.5. K-means decreases this objective but may reach a local solution. A worked Python calculation is included in every notebook.

## Practical Examples

The Otsu reference sweeps histogram partitions, k-means updates assignments and means, and the component reference uses a queue to flood each unvisited foreground region.

```bash
python -m cvzero.course --chapter 14 --lesson 0 --seed 42 --output artifacts/ch14-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Global, adaptive and Otsu thresholds](notebooks/01_foundations.ipynb)
- [2. K-means color segmentation](notebooks/02_mechanisms.ipynb)
- [3. Connected components and region cleanup](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Classical Segmentation Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Cluster zero is not automatically background. Accuracy on a mostly-background image can be high for an empty prediction.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does global, adaptive and otsu thresholds solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Add a lighting gradient before thresholding. Compare Otsu and adaptive masks at fixed object geometry, then inspect component counts. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Cluster zero is not automatically background. Accuracy on a mostly-background image can be high for an empty prediction. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Classical Segmentation Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-14) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[15 · Video Processing](../15-video-processing/README.md)
