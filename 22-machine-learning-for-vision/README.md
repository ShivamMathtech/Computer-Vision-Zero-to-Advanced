# 22 · Machine Learning for Vision

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Machine learning fits a rule from examples rather than specifying every visual condition manually. Features are measured inputs, labels are targets, and a held-out evaluation estimates behavior on new examples. Dataset design is part of the model, not administrative work after training.

## What You Will Learn

- Datasets, splits and leakage
- Linear classification and optimization
- Metrics, confusion and thresholds

## Why It Matters

Evaluate a baseline with a genuinely held-out split. Separate training, validation and test data before fitting any preprocessing. Training fits parameters, validation selects settings and the test set estimates final performance. Related images from one person, video or production item should stay in one split. Random image splitting can leak nearly identical observations across splits.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [09 · Feature Detection](../09-feature-detection/README.md), [14 · Classical Segmentation](../14-segmentation-classical/README.md)

## Core Concepts

Features, labels, splits, leakage, classification, regression, confusion matrix, precision, recall, F1, ROC-AUC. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
Precision=TP/(TP+FP),\quad Recall=TP/(TP+FN)
$$

TP, FP and FN count true positives, false positives and missed positives. With TP=8, FP=2 and FN=4, precision=0.8 and recall=2/3. Zero denominators need an explicit reporting policy. A worked Python calculation is included in every notebook.

## Practical Examples

A stratified split preserves approximate class proportions; a training-only scaler and LogisticRegression form the pipeline. The confusion matrix is measured on untouched test examples.

```bash
python -m cvzero.course --chapter 22 --lesson 0 --seed 42 --output artifacts/ch22-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Datasets, splits and leakage](notebooks/01_foundations.ipynb)
- [2. Linear classification and optimization](notebooks/02_mechanisms.ipynb)
- [3. Metrics, confusion and thresholds](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Digit and Defect Classifier](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Fitting a scaler or PCA before splitting leaks test distribution information. Accuracy can hide poor minority-class recall.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does datasets, splits and leakage solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Compare raw-pixel and HOG features while keeping the split fixed. Tune settings on validation data before inspecting final test results. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Fitting a scaler or PCA before splitting leaks test distribution information. Accuracy can hide poor minority-class recall. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Digit and Defect Classifier into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-22) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://scikit-learn.org/stable/common_pitfalls.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[23 · CNN Fundamentals](../23-cnn-fundamentals/README.md)
