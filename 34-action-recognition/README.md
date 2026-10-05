# 34 · Action Recognition

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Action recognition uses temporal information to classify a sequence. A single frame may show a pose but cannot reliably reveal motion direction or order. The choice of temporal representation determines what evidence a model can use.

## What You Will Learn

- Sequences and temporal sampling
- CNN–RNN and recurrent state
- 3D CNNs and temporal transformers

## Why It Matters

Classify visible actions without inferring private mental states. A clip samples frames over a time interval. Frame rate, stride and clip length control which motions remain visible. Splits should group related clips by source video or actor to avoid leakage. The synthetic lab uses coordinate trajectories so temporal order is the only useful direction cue.

## Prerequisites

[15 · Video Processing](../15-video-processing/README.md), [24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [32 · Pose Estimation](../32-pose-estimation/README.md)

## Core Concepts

Temporal windows, CNN plus RNN, 3D CNN, temporal attention, subject-disjoint splits. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
v_t=(x_t-x_{t-1})/\Delta t
$$

xt is position at time t, Δt the time interval and vt the finite-difference velocity. Moving from 4 to 7 pixels in 0.1 seconds gives 30 pixels per second. Frame differences without Δt mix speed with frame rate. A worked Python calculation is included in every notebook.

## Practical Examples

Generated trajectories become batches of T×2 features; a GRU summarizes them and a head predicts direction. Held-out sequences use an independent random seed.

```bash
python -m cvzero.course --chapter 34 --lesson 0 --seed 42 --output artifacts/ch34-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Sequences and temporal sampling](notebooks/01_foundations.ipynb)
- [2. CNN–RNN and recurrent state](notebooks/02_mechanisms.ipynb)
- [3. 3D CNNs and temporal transformers](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Action Sequence Classifier](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A model may recognize the background or actor instead of the action. Random clip splitting can make evaluation misleadingly easy.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does sequences and temporal sampling solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Reverse each test sequence and check whether the predicted direction changes. Shuffle frame order and measure the damage. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A model may recognize the background or actor instead of the action. Random clip splitting can make evaluation misleadingly easy. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Action Sequence Classifier into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-34) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[35 · Optical Flow](../35-optical-flow/README.md)
