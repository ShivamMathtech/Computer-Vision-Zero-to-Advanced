# 17 · Motion Detection

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Motion detection asks where the scene changes over time. It does not identify object categories or preserve identity. The simplest useful systems compare frames or maintain a slowly changing background and then clean a foreground mask.

## What You Will Learn

- Frame differencing
- Running backgrounds and adaptation
- MOG2, shadows and failure analysis

## Why It Matters

Detect scene change without confusing it with object identity. Frame differencing subtracts consecutive images and thresholds the absolute change. It emphasizes movement boundaries and can miss the interior of a slowly moving object. A stopped object disappears from the difference even though it still occupies the scene.

## Prerequisites

[14 · Classical Segmentation](../14-segmentation-classical/README.md), [15 · Video Processing](../15-video-processing/README.md)

## Core Concepts

Frame differencing, background models, shadows, temporal thresholds. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
B_t=(1-\alpha)B_{t-1}+\alpha I_t
$$

Bt is the updated background, It the current frame and α the update rate. For previous background 100, current intensity 140 and α=0.1, the new estimate is 104. A worked Python calculation is included in every notebook.

## Practical Examples

The generated sequence supplies an initial background and moving foreground. The lab compares absolute differences, a running mean and OpenCV MOG2 masks under a fixed seed.

```bash
python -m cvzero.course --chapter 17 --lesson 0 --seed 42 --output artifacts/ch17-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Frame differencing](notebooks/01_foundations.ipynb)
- [2. Running backgrounds and adaptation](notebooks/02_mechanisms.ipynb)
- [3. MOG2, shadows and failure analysis](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Motion Detector](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Global lighting changes resemble motion. A binary foreground mask does not distinguish one object from two touching objects.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does frame differencing solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Stop the object midway and vary adaptation rate. Measure how long it remains foreground and how long a ghost remains after it leaves. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Global lighting changes resemble motion. A binary foreground mask does not distinguish one object from two touching objects. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Motion Detector into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-17) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[18 · Object Tracking](../18-object-tracking/README.md)
