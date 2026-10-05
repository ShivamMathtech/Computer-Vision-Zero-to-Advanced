# 51 · Edge AI

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Edge AI runs perception near the sensor on constrained hardware. Memory, power, thermal behavior and supported operators can matter as much as model size. Target-device measurements are necessary because desktop CPU results do not predict every edge accelerator.

## What You Will Learn

- Compute, memory and resolution budgets
- Model and runtime choices
- Target-device evaluation

## Why It Matters

Measure performance under actual device constraints. An RGB uint8 frame uses height×width×3 bytes before additional buffers. Intermediate feature maps can use much more memory than the input. Lowering resolution reduces compute but may remove small defects or distant objects. The lab measures memory and edge fidelity across input sizes.

## Prerequisites

[49 · Model Optimization](../49-model-optimization/README.md), [50 · Computer Vision Deployment](../50-computer-vision-deployment/README.md)

## Core Concepts

Device budgets, thermal constraints, memory, offline operation, camera adapters. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
M=HWCb
$$

M is buffer size in bytes, H,W spatial dimensions, C channels and b bytes per element. A 640×480 RGB uint8 image uses 921600 bytes, excluding object overhead and copies. A worked Python calculation is included in every notebook.

## Practical Examples

The lab resizes one generated image, runs Canny repeatedly, records buffer size and compares resized edge masks to the full-resolution algorithm output.

```bash
python -m cvzero.course --chapter 51 --lesson 0 --seed 42 --output artifacts/ch51-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Compute, memory and resolution budgets](notebooks/01_foundations.ipynb)
- [2. Model and runtime choices](notebooks/02_mechanisms.ipynb)
- [3. Target-device evaluation](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Edge Inference Benchmark](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A smaller model file may still allocate large activations. Cold-start and thermally throttled timings answer different operational questions.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does compute, memory and resolution budgets solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Choose a small-object size and reduce resolution until it disappears. Compare the memory saving with the task-specific quality loss. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A smaller model file may still allocate large activations. Cold-start and thermally throttled timings answer different operational questions. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Edge Inference Benchmark into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-51) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://onnxruntime.ai/docs/performance/) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[52 · Real-Time Computer Vision](../52-real-time-computer-vision/README.md)
