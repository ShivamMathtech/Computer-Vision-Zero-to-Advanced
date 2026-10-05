# 39 · Self-Supervised Learning

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Self-supervised learning constructs a training signal from data itself. The goal is a useful representation, not merely a low pretext-task loss. Augmentations and objectives decide what information is preserved and what is deliberately ignored.

## What You Will Learn

- Contrastive views and SimCLR
- EMA targets and BYOL ideas
- Masked image modeling and evaluation

## Why It Matters

Compare representations with fixed evaluation protocols. Contrastive learning pulls representations of two augmented views of the same image together and distinguishes other examples. Normalization and temperature control similarity scores. The local SimCLR-style experiment forms paired views and computes a normalized temperature-scaled contrastive objective. Augmentations must preserve information needed for downstream tasks.

## Prerequisites

[26 · Transfer Learning](../26-transfer-learning/README.md), [38 · Attention Mechanisms](../38-attention-mechanisms/README.md)

## Core Concepts

Representations, augmentation, contrastive loss, SimCLR, BYOL, masked modeling, collapse. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\theta_{target}\leftarrow m\theta_{target}+(1-m)\theta_{online}
$$

m is the EMA momentum, θtarget the slow-moving parameters and θonline the current trained parameters. With values 1 and 3 and m=0.9, the target becomes 1.2. A worked Python calculation is included in every notebook.

## Practical Examples

Three experiments isolate contrastive pair construction, EMA target consistency and masked reconstruction. They use small synthetic data and report local objectives, not large-scale representation benchmarks.

```bash
python -m cvzero.course --chapter 39 --lesson 0 --seed 42 --output artifacts/ch39-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Contrastive views and SimCLR](notebooks/01_foundations.ipynb)
- [2. EMA targets and BYOL ideas](notebooks/02_mechanisms.ipynb)
- [3. Masked image modeling and evaluation](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Self-Supervised Representation Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Two crops can remove the object and cease to be meaningful positive pairs. EMA consistency without the full method can collapse.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does contrastive views and simclr solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Remove an augmentation and measure downstream probe performance, not only training loss. Check embedding variance for collapse. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Two crops can remove the object and cease to be meaningful positive pairs. EMA consistency without the full method can collapse. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Self-Supervised Representation Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-39) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/2002.05709) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[40 · Vision-Language Models](../40-vision-language-models/README.md)
