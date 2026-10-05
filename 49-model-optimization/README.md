# 49 · Model Optimization

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Optimization changes runtime, memory or storage while controlling output quality. Faster arithmetic is useful only when it improves the actual bottleneck. Measure a representative workload before choosing quantization, pruning, compilation or a different architecture.

## What You Will Learn

- Profiling and reliable benchmarks
- Quantization and numerical error
- ONNX export and runtime parity

## Why It Matters

Benchmark speed, memory and accuracy on the same workload. Separate preprocessing, transfer, model execution and postprocessing time. Warm up the runtime, repeat measurements and report a distribution rather than one sample. GPU operations may be asynchronous and need synchronization for accurate timing. Batch size affects throughput and individual request latency differently.

## Prerequisites

[24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [27 · Object Detection](../27-object-detection/README.md), [31 · Semantic Segmentation](../31-semantic-segmentation/README.md), [37 · Vision Transformers](../37-vision-transformers/README.md)

## Core Concepts

Profiling, quantization, pruning, distillation, ONNX, TensorRT concepts, correctness tolerance. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
q=clip(round(w/s),-127,127),\quad\hat w=sq
$$

w is a weight, s a positive scale, q its signed int8 code and ŵ the reconstruction. With w=0.26 and s=0.1, q=3 and ŵ=0.3, giving error 0.04. A worked Python calculation is included in every notebook.

## Practical Examples

The local lab records storage and output error for a quantized weight matrix. scripts/export_model.py adds actual graph validation and ONNX Runtime output agreement.

```bash
python -m cvzero.course --chapter 49 --lesson 0 --seed 42 --output artifacts/ch49-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Profiling and reliable benchmarks](notebooks/01_foundations.ipynb)
- [2. Quantization and numerical error](notebooks/02_mechanisms.ipynb)
- [3. ONNX export and runtime parity](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Model Optimization Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Benchmarking a first call includes initialization. Numerically close logits can still cross a decision threshold on borderline examples.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does profiling and reliable benchmarks solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Quantize a weight distribution with an outlier and compare per-tensor and per-channel error. Measure the target runtime rather than extrapolating from file size. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Benchmarking a first call includes initialization. Numerically close logits can still cross a decision threshold on borderline examples. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Model Optimization Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-49) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.pytorch.org/docs/stable/onnx.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[50 · Computer Vision Deployment](../50-computer-vision-deployment/README.md)
