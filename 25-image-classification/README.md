# 25 · Image Classification

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Classification predicts labels for an entire image. Binary, multiclass and multilabel problems have different target and output meanings. Choosing the loss follows from those meanings, not from whichever model is fashionable.

## What You Will Learn

- Multiclass CNN classification
- Binary decisions and calibration
- Multilabel tasks and model families

## Why It Matters

Train a classifier and report per-class failures. Multiclass classification chooses one of several mutually exclusive labels. Cross entropy accepts raw logits and integer class indices in the common PyTorch form. The synthetic CNN learns circle, square and triangle classes. A held-out confusion matrix reveals which classes are confused, while training curves reveal optimization behavior.

## Prerequisites

[22 · Machine Learning for Vision](../22-machine-learning-for-vision/README.md), [24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md)

## Core Concepts

Binary, multiclass, multilabel, simple CNN, ResNet, EfficientNet, MobileNet, calibration. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
p_k=e^{z_k}/\sum_j e^{z_j}
$$

zk is the logit for class k and pk its softmax probability. Subtracting the largest logit before exponentiation avoids overflow without changing the result. Two equal logits produce probabilities [0.5,0.5]. A worked Python calculation is included in every notebook.

## Practical Examples

A tiny convolutional backbone and linear head produce logits; the lab trains on generated shapes, measures held-out predictions and contrasts exclusive and independent target encodings.

```bash
python -m cvzero.course --chapter 25 --lesson 0 --seed 42 --output artifacts/ch25-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Multiclass CNN classification](notebooks/01_foundations.ipynb)
- [2. Binary decisions and calibration](notebooks/02_mechanisms.ipynb)
- [3. Multilabel tasks and model families](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Vehicle or Plant Classifier](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Softmax forces scores to sum to one even for an out-of-distribution image. A confident prediction is not proof that the image belongs to a known class.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does multiclass cnn classification solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Create a background-only class and inspect whether confidence on unknown objects falls. Compare macro and micro metrics under class imbalance. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Softmax forces scores to sum to one even for an out-of-distribution image. A confident prediction is not proof that the image belongs to a known class. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Vehicle or Plant Classifier into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-25) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.pytorch.org/vision/stable/models.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[26 · Transfer Learning](../26-transfer-learning/README.md)
