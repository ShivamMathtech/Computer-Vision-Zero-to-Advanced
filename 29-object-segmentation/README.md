# 29 · Object Segmentation

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Object segmentation describes which pixels belong to a foreground region. A binary mask gives finer geometry than a box, enabling measurements of coverage and shape. Before separating categories or individual instances, learn mask representation and overlap metrics.

## What You Will Learn

- Binary masks and overlap metrics
- Encoder–decoder segmentation
- Thresholds and boundary errors

## Why It Matters

Match segmentation formulations to an industrial question. A binary target assigns each pixel foreground or background. IoU measures intersection divided by union; Dice doubles the intersection and divides by the sum of mask sizes. Empty masks require a stated convention. Pixel accuracy can be misleading when nearly every pixel is background.

## Prerequisites

[14 · Classical Segmentation](../14-segmentation-classical/README.md), [24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [27 · Object Detection](../27-object-detection/README.md)

## Core Concepts

Binary vs semantic vs instance, masks, losses, Dice, IoU, FCN, U-Net, DeepLab, Mask R-CNN. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
Dice=2|P\cap G|/(|P|+|G|)
$$

P is the predicted foreground and G ground truth. If each contains 10 pixels and 8 overlap, Dice=0.8. The associated IoU is 8/12, not 0.8. A worked Python calculation is included in every notebook.

## Practical Examples

The lab trains on generated images and exact synthetic masks, then measures held-out IoU and Dice. These numbers describe only the stated generated distribution.

```bash
python -m cvzero.course --chapter 29 --lesson 0 --seed 42 --output artifacts/ch29-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Binary masks and overlap metrics](notebooks/01_foundations.ipynb)
- [2. Encoder–decoder segmentation](notebooks/02_mechanisms.ipynb)
- [3. Thresholds and boundary errors](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Segmentation Task Explorer](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Resize categorical masks with nearest-neighbor interpolation. Bilinear interpolation creates invalid intermediate class IDs.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does binary masks and overlap metrics solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Change the foreground threshold and plot precision/recall for foreground pixels. Inspect small objects separately. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Resize categorical masks with nearest-neighbor interpolation. Bilinear interpolation creates invalid intermediate class IDs. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Segmentation Task Explorer into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-29) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/1505.04597) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[30 · Instance Segmentation](../30-instance-segmentation/README.md)
