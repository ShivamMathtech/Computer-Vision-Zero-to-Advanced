# 41 · Multimodal Computer Vision

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Multimodal vision combines information from different sources, such as RGB, depth, text or audio. The central problems include alignment, missing inputs and conflicting evidence. More sensors can improve a system only when their uncertainties and timing are handled correctly.

## What You Will Learn

- Early, late and cross-modal fusion
- Uncertainty-weighted sensor fusion
- Missing modalities and synchronization

## Why It Matters

Combine visual and nonvisual observations without hiding missing data. Early fusion combines inputs or features before the final predictor; late fusion combines separate predictions. Cross-attention can allow one modality to query another. These choices trade flexibility, missing-input handling and compute. RGB and depth must refer to compatible coordinates before pixel-level fusion makes sense.

## Prerequisites

[16 · Camera and Calibration](../16-camera-and-calibration/README.md), [35 · Optical Flow](../35-optical-flow/README.md), [40 · Vision-Language Models](../40-vision-language-models/README.md)

## Core Concepts

Sensor timestamps, calibration, fusion, missing modalities, uncertainty, alignment. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\hat x=(x_1/\sigma_1^2+x_2/\sigma_2^2)/(1/\sigma_1^2+1/\sigma_2^2)
$$

x1,x2 estimate one quantity and σ1²,σ2² are independent measurement variances. Measurements 2 and 4 with variances 1 and 4 combine to 2.4, closer to the more precise first sensor. A worked Python calculation is included in every notebook.

## Practical Examples

The lab generates visual and depth-like scalar measurements, applies precision weighting and falls back to the available sensor when depth is missing. It isolates fusion rather than a full learned multimodal architecture.

```bash
python -m cvzero.course --chapter 41 --lesson 0 --seed 42 --output artifacts/ch41-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Early, late and cross-modal fusion](notebooks/01_foundations.ipynb)
- [2. Uncertainty-weighted sensor fusion](notebooks/02_mechanisms.ipynb)
- [3. Missing modalities and synchronization](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[RGB and Sensor Fusion Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Concatenating arrays is not sufficient if modalities describe different times or coordinates. A high-confidence sensor can still be systematically biased.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does early, late and cross-modal fusion solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Make sensor errors correlated and compare the theoretical confidence with observed error. Then introduce missing depth. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Concatenating arrays is not sufficient if modalities describe different times or coordinates. A high-confidence sensor can still be systematically biased. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn RGB and Sensor Fusion Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-41) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[42 · Generative Computer Vision](../42-generative-computer-vision/README.md)
