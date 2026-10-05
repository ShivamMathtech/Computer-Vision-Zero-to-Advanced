# 18 · Object Tracking

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Tracking estimates an object state over time. Detection supplies observations; a motion model predicts where the object might be next. Keeping uncertainty explicit allows a tracker to bridge short missing detections without pretending its prediction is a measurement.

## What You Will Learn

- State, observations and prediction
- Kalman correction and uncertainty
- Occlusion, gating and track lifetime

## Why It Matters

Follow a visible object and explain when its identity is uncertain. A simple state stores x, y, horizontal velocity and vertical velocity. A constant-velocity transition advances position by velocity times elapsed time. Process noise represents unmodeled acceleration. A detection observes position with measurement noise and usually does not directly observe velocity.

## Prerequisites

[12 · Contours and Shapes](../12-contours-and-shapes/README.md), [15 · Video Processing](../15-video-processing/README.md), [17 · Motion Detection](../17-motion-detection/README.md)

## Core Concepts

Detection vs tracking, centroid association, template tracking, gating, occlusion. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
x_{t+1}=x_t+v_x\Delta t
$$

x is horizontal position, vx horizontal velocity and Δt elapsed time. At x=10 px, velocity 3 px/s and Δt=0.5 s, predicted x is 11.5 px. This model assumes constant velocity over that interval. A worked Python calculation is included in every notebook.

## Practical Examples

The tracker predicts state/covariance, associates gated observations, corrects matched tracks and expires stale tracks. The lab compares noisy centers and filtered positions against known trajectories.

```bash
python -m cvzero.course --chapter 18 --lesson 0 --seed 42 --output artifacts/ch18-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. State, observations and prediction](notebooks/01_foundations.ipynb)
- [2. Kalman correction and uncertainty](notebooks/02_mechanisms.ipynb)
- [3. Occlusion, gating and track lifetime](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Ball Tracker](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A smooth trajectory can still be wrong. Pixel velocity changes when FPS changes unless elapsed time is included.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does state, observations and prediction solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Increase measurement noise and insert a short occlusion. Plot position error and inspect uncertainty rather than judging smoothness alone. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A smooth trajectory can still be wrong. Pixel velocity changes when FPS changes unless elapsed time is included. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Ball Tracker into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-18) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/dd/d6a/classcv_1_1KalmanFilter.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[19 · Face Detection](../19-face-detection/README.md)
