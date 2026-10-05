# 15 · Video Processing

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

A video is a time-ordered sequence of images with timing and encoding information. Frame count, nominal FPS, processing throughput and end-to-end latency describe different things. A reliable loop must handle end-of-file, decode failures and unavailable cameras.

## What You Will Learn

- Frames, codecs and video I/O
- Processing loops and timestamps
- Background models and streaming design

## Why It Matters

Process finite files and release camera resources reliably. Video containers hold encoded frames and timing metadata; a codec compresses the frames. VideoWriter needs a compatible codec, frame dimensions, color convention and nominal FPS. The lab writes a small generated motion sequence, reads it back and verifies the decoded frame count. Codec availability can differ across operating systems.

## Prerequisites

[04 · OpenCV Fundamentals](../04-opencv-fundamentals/README.md), [08 · Color Spaces](../08-color-spaces/README.md), [14 · Classical Segmentation](../14-segmentation-classical/README.md)

## Core Concepts

Frames, FPS, timestamps, codecs, streams, capture, background subtraction. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
t_i=i/f
$$

ti is the nominal timestamp of frame index i and f the constant frame rate in frames per second. Frame 45 at 30 FPS is at 1.5 seconds. Variable-frame-rate video requires actual timestamps rather than this formula. A worked Python calculation is included in every notebook.

## Practical Examples

Generated moving frames isolate codec and loop behavior from camera hardware. Differences are computed in a signed type; thresholded differences are only motion candidates.

```bash
python -m cvzero.course --chapter 15 --lesson 0 --seed 42 --output artifacts/ch15-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Frames, codecs and video I/O](notebooks/01_foundations.ipynb)
- [2. Processing loops and timestamps](notebooks/02_mechanisms.ipynb)
- [3. Background models and streaming design](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Motion and Traffic Counter](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

VideoCapture.read returning false can mean end-of-stream or failure. Writing frames of the wrong shape may silently produce a broken video.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does frames, codecs and video i/o solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Process every second frame and compare trajectory displacement per processed frame with displacement per second. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

VideoCapture.read returning false can mean end-of-stream or failure. Writing frames of the wrong shape may silently produce a broken video. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Motion and Traffic Counter into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-15) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[16 · Camera and Calibration](../16-camera-and-calibration/README.md)
