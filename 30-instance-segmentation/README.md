# 30 · Instance Segmentation

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Instance segmentation gives each object its own mask, even when objects share a class. Semantic segmentation alone labels all same-class pixels alike. Separating touching objects therefore requires additional structure, such as markers, proposals or object queries.

## What You Will Learn

- Instance IDs versus class labels
- Distance transforms and watershed
- Mask R-CNN and learned instance masks

## Why It Matters

Keep object identity when masks overlap. An instance map stores a distinct ID for every object and usually reserves zero for background. IDs are local identifiers, not semantic categories. Two touching circles should have two instances even though both are foreground. Evaluation must match predicted and true instances before scoring overlap.

## Prerequisites

[27 · Object Detection](../27-object-detection/README.md), [29 · Object Segmentation](../29-object-segmentation/README.md)

## Core Concepts

Mask R-CNN, per-instance masks, mask AP, overlapping objects. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
D(p)=\min_{q\in background}\lVert p-q\rVert_2
$$

D(p) is a foreground pixel’s distance to background. For point p=[2,2] and background point q=[2,0], the distance is 2 pixels. Large local distances often occur near object interiors. A worked Python calculation is included in every notebook.

## Practical Examples

The lab computes a foreground mask, distance map, marker labels and watershed boundaries. Counted instances are measured from the resulting IDs, not assumed from the input design.

```bash
python -m cvzero.course --chapter 30 --lesson 0 --seed 42 --output artifacts/ch30-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Instance IDs versus class labels](notebooks/01_foundations.ipynb)
- [2. Distance transforms and watershed](notebooks/02_mechanisms.ipynb)
- [3. Mask R-CNN and learned instance masks](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Instance Counting System](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A separate ID for every connected component fails when objects touch. Instance IDs are not stable track IDs across frames.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does instance ids versus class labels solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Move the two circles closer and vary the marker threshold. Identify the point at which seeds merge. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A separate ID for every connected component fails when objects touch. Instance IDs are not stable track IDs across frames. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Instance Counting System into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-30) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/1703.06870) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[31 · Semantic Segmentation](../31-semantic-segmentation/README.md)
