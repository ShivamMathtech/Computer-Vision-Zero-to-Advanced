# 28 · YOLO

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

YOLO-family detectors predict objects efficiently from shared image features. The exact head, assignment, loss and suppression behavior varies by version. Learn the box and training mechanics first, then use an explicit model configuration for the full library workflow.

## What You Will Learn

- Single-stage localization mechanics
- Dataset preparation and annotation checks
- Training, evaluation, inference and export

## Why It Matters

Run an auditable custom detector workflow. A dense detector learns location and category predictions from spatial features at one or more scales. Early YOLO used a grid-based formulation; newer families change important details. The CPU lab trains a single-object box regressor to expose normalized target encoding and localization loss. It is intentionally not a reproduction of a named YOLO architecture.

## Prerequisites

[27 · Object Detection](../27-object-detection/README.md)

## Core Concepts

Annotations, YAML, split audit, training, validation, confidence, NMS, export. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
c_x=(x_1+x_2)/(2W),\quad w=(x_2-x_1)/W
$$

x1,x2 are horizontal corners and W image width; cx and w are normalized center and width. For corners 20 and 60 in a 100-pixel image, cx=0.4 and w=0.4. A worked Python calculation is included in every notebook.

## Practical Examples

The local regressor predicts normalized cxcywh with a sigmoid and trains against boxes derived from generated masks. Full detector stages are implemented in the optional external workflow and are not executed by default.

```bash
python -m cvzero.course --chapter 28 --lesson 0 --seed 42 --output artifacts/ch28-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Single-stage localization mechanics](notebooks/01_foundations.ipynb)
- [2. Dataset preparation and annotation checks](notebooks/02_mechanisms.ipynb)
- [3. Training, evaluation, inference and export](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Custom YOLO Detector](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Training and test images from adjacent video frames can leak scene content. A synthetic regressor loss must not be advertised as YOLO mAP.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does single-stage localization mechanics solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Inspect every generated label as an overlay, then intentionally introduce an invalid width and confirm that validation rejects it. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Training and test images from adjacent video frames can leak scene content. A synthetic regressor loss must not be advertised as YOLO mAP. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Custom YOLO Detector into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-28) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.ultralytics.com/modes/train/) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[29 · Object Segmentation](../29-object-segmentation/README.md)
