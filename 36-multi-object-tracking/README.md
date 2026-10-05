# 36 · Multi-Object Tracking

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Multi-object tracking maintains several identities across detections. It combines prediction, association, creation and deletion policies. Detection quality, occlusion and object similarity all affect identity continuity.

## What You Will Learn

- Track state and detection association
- Hungarian assignment and gating
- SORT, DeepSORT and evaluation

## Why It Matters

Evaluate association separately from detection quality. Each active object has a predicted state and uncertainty. New detections must be assigned to old tracks, left unmatched or used to start new tracks. Independent nearest-neighbor choices can assign two detections to the same track, so association needs a global one-to-one constraint.

## Prerequisites

[18 · Object Tracking](../18-object-tracking/README.md), [27 · Object Detection](../27-object-detection/README.md), [35 · Optical Flow](../35-optical-flow/README.md)

## Core Concepts

Track IDs, Kalman filter, Hungarian assignment, SORT, DeepSORT, identity switches. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\min_A\sum_{ij}A_{ij}C_{ij}
$$

Cij is the cost of assigning track i to detection j, and Aij is 1 when that assignment is selected. Each track and detection may appear at most once. Costs [[1,9],[8,2]] favor the diagonal with total cost 3. A worked Python calculation is included in every notebook.

## Practical Examples

The shared tracker performs prediction, gated Hungarian association and Joseph-form covariance correction. The synthetic lab introduces missed observations and reports a limited nearest-truth identity diagnostic.

```bash
python -m cvzero.course --chapter 36 --lesson 0 --seed 42 --output artifacts/ch36-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Track state and detection association](notebooks/01_foundations.ipynb)
- [2. Hungarian assignment and gating](notebooks/02_mechanisms.ipynb)
- [3. SORT, DeepSORT and evaluation](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Vehicle Tracking System](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Track IDs are temporary anonymous identifiers, not person identities. A detector score is not a track survival probability.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does track state and detection association solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Make two trajectories cross, remove observations briefly and compare the ID sequence before and after occlusion. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Track IDs are temporary anonymous identifiers, not person identities. A detector score is not a track survival probability. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Vehicle Tracking System into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-36) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/1602.00763) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[37 · Vision Transformers](../37-vision-transformers/README.md)
