# 04 · OpenCV Fundamentals

**Beginner · CPU baseline · 3 focused notebooks · no required downloads**

OpenCV supplies optimized building blocks for images and video. Its functions still have contracts: channel order, data type, coordinate convention and return values. Learning these contracts prevents a successful function call from silently producing the wrong image.

## What You Will Learn

- Read, write, draw and label
- Resizing and image display
- Events, camera loops and controls

## Why It Matters

Build image and webcam tools with useful failure messages. Read an image, check decoding succeeded, and convert BGR to RGB before plotting. Drawing modifies an array in place unless you copy it first. PNG is lossless for the lab arrays; JPEG can change values. The notebook performs an encode/decode round trip so image I/O can be tested without external assets.

## Prerequisites

[01 · Python for Computer Vision](../01-python-for-computer-vision/README.md), [03 · Image Fundamentals](../03-image-fundamentals/README.md)

## Core Concepts

Image I/O, BGR, drawing, text, webcam, keyboard and mouse events, trackbars. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
I_{RGB}(y,x)=[I_{BGR}(y,x,2),I_{BGR}(y,x,1),I_{BGR}(y,x,0)]
$$

I is an image indexed by row y, column x and channel index. Reversing the three BGR channels gives RGB. BGR [10,20,200] becomes RGB [200,20,10]. A worked Python calculation is included in every notebook.

## Practical Examples

OpenCV decoding produces an array, drawing edits its buffer, and encoding compresses that buffer to bytes. VideoCapture abstracts a file or device; read success is independent of the requested frame size.

```bash
python -m cvzero.course --chapter 4 --lesson 0 --seed 42 --output artifacts/ch04-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Read, write, draw and label](notebooks/01_foundations.ipynb)
- [2. Resizing and image display](notebooks/02_mechanisms.ipynb)
- [3. Events, camera loops and controls](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Paint and Webcam Viewer](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

cv2.imread returns None on many failures. A missing camera or display is an environmental condition, not evidence that the vision algorithm is wrong.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does read, write, draw and label solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Save the same RGB image as PNG and JPEG, reload both, and measure the maximum absolute difference after casting to signed integers. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

cv2.imread returns None on many failures. A missing camera or display is an environmental condition, not evidence that the vision algorithm is wrong. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Paint and Webcam Viewer into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-04) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[05 · Image Processing](../05-image-processing/README.md)
