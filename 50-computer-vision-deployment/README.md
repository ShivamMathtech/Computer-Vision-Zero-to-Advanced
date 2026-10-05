# 50 · Computer Vision Deployment

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Deployment wraps model behavior in a stable interface. Input validation, preprocessing, versioned outputs and useful failure responses are part of correctness. A local demo becomes a service only when its state, storage and operating assumptions are explicit.

## What You Will Learn

- Inference contracts and FastAPI
- Persistence, sessions and request ordering
- Containers and deployment boundaries

## Why It Matters

Serve a versioned model and validate requests and predictions. An inference contract specifies image formats, maximum size, color order, output coordinates and label meanings. The FastAPI app validates bounded base64 payloads, checks decoded dimensions and returns structured detections plus an overlay. Invalid input should produce a useful client error rather than crash the worker.

## Prerequisites

[49 · Model Optimization](../49-model-optimization/README.md)

## Core Concepts

FastAPI, Streamlit, Gradio, Docker, schemas, validation, batch, CPU and GPU inference. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
L_{end}=L_{decode}+L_{pre}+L_{model}+L_{post}+L_{transport}
$$

Lend is end-to-end latency and the remaining terms are decode, preprocessing, inference, postprocessing and transport times. Components 2,3,10,2,5 milliseconds sum to 22 ms. Server model time alone is only one component. A worked Python calculation is included in every notebook.

## Practical Examples

The capstone factory constructs an API, per-session engine and SQLite event store. Tests send real request payloads without opening a public network listener.

```bash
python -m cvzero.course --chapter 50 --lesson 0 --seed 42 --output artifacts/ch50-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Inference contracts and FastAPI](notebooks/01_foundations.ipynb)
- [2. Persistence, sessions and request ordering](notebooks/02_mechanisms.ipynb)
- [3. Containers and deployment boundaries](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Production Vision API](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

In-memory session state is not shared across server processes. Multiple workers need a deliberate state partitioning or external-state design.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does inference contracts and fastapi solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Send invalid images, duplicate IDs and oversized dimensions. Verify status codes and that failed requests do not create stored events. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

In-memory session state is not shared across server processes. Multiple workers need a deliberate state partitioning or external-state design. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Production Vision API into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-50) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://fastapi.tiangolo.com/tutorial/) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[51 · Edge AI](../51-edge-ai/README.md)
