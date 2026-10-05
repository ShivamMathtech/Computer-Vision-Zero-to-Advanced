# 31 · Semantic Segmentation

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Semantic segmentation assigns a category to every pixel. All pixels of the same category share a label even when they belong to separate objects. Dense prediction requires spatially aligned targets, careful loss design and evaluation across classes.

## What You Will Learn

- Dense class targets and FCN
- U-Net, DeepLab and context
- IoU, imbalance and deployment masks

## Why It Matters

Train and inspect a dense labeling model. A fully convolutional network replaces image-level classification with spatial logits. For C mutually exclusive classes, logits have shape N×C×H×W and targets typically have integer IDs N×H×W. Binary one-channel segmentation is a special case and uses a different target contract.

## Prerequisites

[29 · Object Segmentation](../29-object-segmentation/README.md)

## Core Concepts

FCN, U-Net, DeepLab, pixel labels, class imbalance, boundaries. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
IoU_c=TP_c/(TP_c+FP_c+FN_c)
$$

TPc counts pixels correctly assigned class c, FPc pixels incorrectly assigned c and FNc missed class-c pixels. Counts 8,2,4 give IoU=8/14. Mean IoU averages class scores under a declared absent-class policy. A worked Python calculation is included in every notebook.

## Practical Examples

The baseline is binary semantic segmentation with a shallow U-Net. The same dense-prediction principles extend to C classes by changing head channels, targets and loss together.

```bash
python -m cvzero.course --chapter 31 --lesson 0 --seed 42 --output artifacts/ch31-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Dense class targets and FCN](notebooks/01_foundations.ipynb)
- [2. U-Net, DeepLab and context](notebooks/02_mechanisms.ipynb)
- [3. IoU, imbalance and deployment masks](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Industrial Surface Segmentation](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Colorful mask visualizations are not training targets unless colors are mapped consistently to integer class IDs.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does dense class targets and fcn solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Create a rare foreground class and compare unweighted loss with a documented weighting scheme. Report per-class IoU rather than only the mean. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Colorful mask visualizations are not training targets unless colors are mapped consistently to integer class IDs. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Industrial Surface Segmentation into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-31) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/1606.00915) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[32 · Pose Estimation](../32-pose-estimation/README.md)
