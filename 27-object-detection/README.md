# 27 · Object Detection

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Object detection predicts both location and class. A detector can produce several overlapping proposals, so evaluation must match predictions to ground-truth objects and count duplicates correctly. Localization and classification errors are different failure modes.

## What You Will Learn

- Boxes, coordinate formats and IoU
- NMS and duplicate predictions
- Precision–recall and detector evolution

## Why It Matters

Implement IoU and NMS before calling a detector API. A box can be expressed by two corners or by center, width and height. This repository uses continuous xyxy coordinates with width=x2−x1. Intersection over Union measures overlap relative to combined area. Empty or non-overlapping boxes need well-defined zero overlap.

## Prerequisites

[12 · Contours and Shapes](../12-contours-and-shapes/README.md), [22 · Machine Learning for Vision](../22-machine-learning-for-vision/README.md), [24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [26 · Transfer Learning](../26-transfer-learning/README.md)

## Core Concepts

Box encodings, IoU, NMS, AP, mAP, R-CNN, Fast R-CNN, Faster R-CNN, SSD, YOLO. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
IoU(A,B)=|A\cap B|/(|A|+|B|-|A\cap B|)
$$

A and B are regions and vertical bars denote area. Two 2×2 boxes overlapping in a 1×1 region have intersection 1, union 7 and IoU=1/7. A worked Python calculation is included in every notebook.

## Practical Examples

The NumPy implementation computes vectorized intersection/union and greedy suppression. Precision/recall are calculated from sorted scores and explicit true/false match flags.

```bash
python -m cvzero.course --chapter 27 --lesson 0 --seed 42 --output artifacts/ch27-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Boxes, coordinate formats and IoU](notebooks/01_foundations.ipynb)
- [2. NMS and duplicate predictions](notebooks/02_mechanisms.ipynb)
- [3. Precision–recall and detector evolution](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Detection Evaluation Toolkit](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

AP50 and COCO-style AP across IoU thresholds are not interchangeable. Coordinate off-by-one conventions matter for small objects.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does boxes, coordinate formats and iou solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Raise the NMS IoU threshold and explain the effect on crowded scenes versus duplicate boxes. Keep confidence and IoU thresholds distinct. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

AP50 and COCO-style AP across IoU thresholds are not interchangeable. Coordinate off-by-one conventions matter for small objects. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Detection Evaluation Toolkit into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-27) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://cocodataset.org/#detection-eval) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[28 · YOLO](../28-yolo/README.md)
