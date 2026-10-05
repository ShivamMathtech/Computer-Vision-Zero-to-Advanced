# 46 · Stereo Vision

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Stereo vision searches for corresponding image points between cameras. Rectification makes ideal matches lie on the same row, reducing a two-dimensional search to a horizontal disparity search. Matching still struggles with occlusion, textureless areas and repeated patterns.

## What You Will Learn

- Rectification and disparity hypotheses
- Block matching from scratch
- SGBM and consistency checks

## Why It Matters

Convert calibrated disparity into depth with valid masks. Rectification remaps calibrated views so epipolar lines align horizontally. The lab starts with already rectified synthetic images to isolate matching. A disparity hypothesis shifts one image relative to the other; only overlapping valid pixels should contribute to its comparison cost.

## Prerequisites

[16 · Camera and Calibration](../16-camera-and-calibration/README.md), [44 · 3D Computer Vision](../44-3d-computer-vision/README.md), [45 · Depth Estimation](../45-depth-estimation/README.md)

## Core Concepts

Rectification, disparity, baseline, matching, occlusion, depth conversion. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
d^*(p)=\arg\min_d\sum_{q\in W(p)}|L(q)-R(q-(d,0))|
$$

L and R are rectified images, W(p) a neighborhood around pixel p and d a candidate disparity. The selected disparity minimizes local absolute intensity difference. Candidate costs [9,2,7] select the second candidate. A worked Python calculation is included in every notebook.

## Practical Examples

The reference constructs a cost volume over integer shifts and chooses its minimum. SGBM provides an optimized comparison; error is evaluated only in an interior region with valid synthetic correspondences.

```bash
python -m cvzero.course --chapter 46 --lesson 0 --seed 42 --output artifacts/ch46-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Rectification and disparity hypotheses](notebooks/01_foundations.ipynb)
- [2. Block matching from scratch](notebooks/02_mechanisms.ipynb)
- [3. SGBM and consistency checks](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Stereo Depth Toolkit](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Using raw SGBM integer output as pixels makes depth wrong by a factor of 16. Rectification does not create missing correspondence in occluded regions.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does rectification and disparity hypotheses solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Replace random texture with a flat patch and inspect ambiguity in the full cost curve. Add an occluder visible to only one camera. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Using raw SGBM integer output as pixels makes depth wrong by a factor of 16. Rectification does not create missing correspondence in occluded regions. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Stereo Depth Toolkit into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-46) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d2/d85/classcv_1_1StereoSGBM.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[47 · Point Clouds](../47-point-clouds/README.md)
