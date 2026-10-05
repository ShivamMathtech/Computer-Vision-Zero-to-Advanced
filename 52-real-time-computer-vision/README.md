# 52 · Real-Time Computer Vision

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Real-time vision is about meeting timing needs on current frames. Throughput measures completed work per second; latency measures delay; frame age measures how stale a result is. A fast model can still produce unusable output if queues grow without bounds.

## What You Will Learn

- Latency, throughput and frame age
- Bounded queues and frame dropping
- Async pipelines and profiling

## Why It Matters

Keep displays responsive while processing bounded work queues. A source can produce frames faster than the inference stage consumes them. In a FIFO queue, waiting time then grows even if every frame is eventually processed. Batch processing can increase throughput while increasing latency. Decide which timing metric matches the application before optimizing.

## Prerequisites

[15 · Video Processing](../15-video-processing/README.md), [36 · Multi-Object Tracking](../36-multi-object-tracking/README.md), [49 · Model Optimization](../49-model-optimization/README.md), [50 · Computer Vision Deployment](../50-computer-vision-deployment/README.md)

## Core Concepts

Latency, throughput, FPS, backpressure, frame dropping, timestamps, threading, multiprocessing. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\rho=\lambda s
$$

λ is arrival rate in frames/second, s mean service seconds/frame and ρ utilization. At 30 FPS and 0.045 seconds of service, ρ=1.35, so one worker cannot keep up indefinitely without dropping or reducing input. A worked Python calculation is included in every notebook.

## Practical Examples

The scheduling simulator advances event times, completes active work and drops the oldest waiting frame when capacity is exceeded. Its output is a simulated latency distribution, not a hardware FPS claim.

```bash
python -m cvzero.course --chapter 52 --lesson 0 --seed 42 --output artifacts/ch52-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Latency, throughput and frame age](notebooks/01_foundations.ipynb)
- [2. Bounded queues and frame dropping](notebooks/02_mechanisms.ipynb)
- [3. Async pipelines and profiling](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Real-Time Analytics Dashboard](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Reporting average FPS hides long stalls. Repeated wait calls and unbounded queues can make live results increasingly stale.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does latency, throughput and frame age solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Compare FIFO and bounded queues under a service-time spike. Report dropped frames alongside p50 and p95 frame latency. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Reporting average FPS hides long stalls. Repeated wait calls and unbounded queues can make live results increasingly stale. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Real-Time Analytics Dashboard into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-52) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.python.org/3/library/queue.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[53 · Production Computer Vision](../53-production-computer-vision/README.md)
