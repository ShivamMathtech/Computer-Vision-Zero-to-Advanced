# 26 · Transfer Learning

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Transfer learning starts from useful learned features and adapts them to a new task. This can reduce data and training requirements, but success depends on how source and target data relate. Frozen features and fine-tuning answer different experimental questions.

## What You Will Learn

- Source pretraining and feature reuse
- Frozen backbones and new heads
- Fine-tuning under domain shift

## Why It Matters

Compare frozen features against controlled fine-tuning. Early image features often capture edges and textures, while later features become more task-specific. Pretraining on a source task provides an initialization or fixed representation. The CPU lab trains its own source model on synthetic shapes, so the origin of every weight is visible.

## Prerequisites

[25 · Image Classification](../25-image-classification/README.md)

## Core Concepts

Feature extraction, freezing, fine-tuning, learning rates, dataset size, domain shift. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
h=f_{\theta}(x),\qquad z=W h+b
$$

x is an image, fθ the backbone, h its feature vector and W,b the new head. Frozen transfer changes W and b while holding θ fixed. With h=[2,1], W=[0.5,−1] and b=0.2, the score is 0.2. A worked Python calculation is included in every notebook.

## Practical Examples

The lab snapshots feature parameters, trains the target head or full network and computes the maximum feature change. The reported source model is locally trained, not ImageNet pretrained.

```bash
python -m cvzero.course --chapter 26 --lesson 0 --seed 42 --output artifacts/ch26-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Source pretraining and feature reuse](notebooks/01_foundations.ipynb)
- [2. Frozen backbones and new heads](notebooks/02_mechanisms.ipynb)
- [3. Fine-tuning under domain shift](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Industrial Defect Classifier](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Replacing the head without matching the label map can silently swap class meanings. Pretraining data may overlap an evaluation set.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does source pretraining and feature reuse solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Vary target brightness and compare frozen features with fine-tuning at two learning rates using an unchanged test set. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Replacing the head without matching the label map can silently swap class meanings. Pretraining data may overlap an evaluation set. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Industrial Defect Classifier into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-26) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[27 · Object Detection](../27-object-detection/README.md)
