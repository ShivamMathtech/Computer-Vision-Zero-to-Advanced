# 21 · OCR

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Optical character recognition converts an image of text into symbols. A useful pipeline distinguishes text detection, geometric cleanup, recognition and layout reconstruction. Blurring, skew, language and font choices can each break a different stage.

## What You Will Learn

- Thresholding, deskewing and text regions
- Template recognition and sequence errors
- Tesseract and learned OCR pipelines

## Why It Matters

Extract text while preserving reading order and error evidence. Preprocessing should improve separation of strokes from background without deleting punctuation or joining letters. Estimate skew from text-line orientation or reliable foreground geometry, rotate with controlled interpolation and preserve a copy of the original. Thresholding is appropriate for some documents but can harm colored or textured text.

## Prerequisites

[07 · Geometric Transformations](../07-geometric-transformations/README.md), [11 · Morphological Image Processing](../11-morphological-image-processing/README.md), [13 · Edge and Corner Detection](../13-edge-and-corner-detection/README.md)

## Core Concepts

Text detection, thresholding, deskew, Tesseract, deep OCR, character and word error rates. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
CER=(S+D+I)/N
$$

S is substitutions, D deletions, I insertions and N the number of reference characters. One substitution in a five-character word gives CER=0.2. General CER needs an edit-distance alignment; equal-length position errors are only a restricted case. A worked Python calculation is included in every notebook.

## Practical Examples

The local lab uses known fixed-spaced glyphs to isolate template recognition. Its positional character error is explicitly narrower than unrestricted edit-distance CER.

```bash
python -m cvzero.course --chapter 21 --lesson 0 --seed 42 --output artifacts/ch21-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Thresholding, deskewing and text regions](notebooks/01_foundations.ipynb)
- [2. Template recognition and sequence errors](notebooks/02_mechanisms.ipynb)
- [3. Tesseract and learned OCR pipelines](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Document OCR Pipeline](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A higher-resolution resize cannot restore unreadable strokes. OCR confidence is not a guarantee that a number was read correctly.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does thresholding, deskewing and text regions solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Change blur, rotation and character spacing independently. Identify whether errors arise before or during recognition. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A higher-resolution resize cannot restore unreadable strokes. OCR confidence is not a guarantee that a number was read correctly. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Document OCR Pipeline into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-21) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[22 · Machine Learning for Vision](../22-machine-learning-for-vision/README.md)
