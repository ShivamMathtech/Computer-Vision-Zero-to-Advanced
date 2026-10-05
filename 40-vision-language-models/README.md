# 40 · Vision-Language Models

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Vision-language models relate images to text. A dual encoder can compare image and text embeddings for retrieval; a generative model can produce captions or answers. These are different capabilities and require different outputs and evaluation.

## What You Will Learn

- Image–text embedding alignment
- Retrieval and zero-shot candidate scoring
- Captioning, VQA and grounding limits

## Why It Matters

Measure retrieval and prompt sensitivity with documented model licenses. An image encoder and text encoder map their inputs into a shared space. Training can increase similarity for paired observations and reduce it for other pairs. The CPU lab learns three synthetic word embeddings and a small image encoder; it demonstrates alignment but has no open-vocabulary language understanding.

## Prerequisites

[38 · Attention Mechanisms](../38-attention-mechanisms/README.md), [39 · Self-Supervised Learning](../39-self-supervised-learning/README.md)

## Core Concepts

CLIP, image-text embeddings, prompting, captions, visual questions, hallucination. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
s_{ij}=\hat v_i^T\hat t_j/\tau
$$

Normalized image embedding v̂i and text embedding t̂j have dot-product similarity, scaled by positive temperature τ. Aligned unit vectors have similarity 1 before scaling. These scores are not calibrated truth probabilities. A worked Python calculation is included in every notebook.

## Practical Examples

The local dual encoder learns a closed vocabulary on generated image-label pairs. Pretrained retrieval, captioning and VQA are implemented separately and are never silently substituted for this small experiment.

```bash
python -m cvzero.course --chapter 40 --lesson 0 --seed 42 --output artifacts/ch40-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Image–text embedding alignment](notebooks/01_foundations.ipynb)
- [2. Retrieval and zero-shot candidate scoring](notebooks/02_mechanisms.ipynb)
- [3. Captioning, VQA and grounding limits](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Image-Text Search](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A plausible caption may hallucinate objects. An embedding similarity cannot establish a person’s identity, intent or protected traits.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does image–text embedding alignment solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Add a visually similar distractor prompt to a candidate set and inspect score changes. Evaluate retrieval rank rather than assuming a fixed probability meaning. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A plausible caption may hallucinate objects. An embedding similarity cannot establish a person’s identity, intent or protected traits. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Image-Text Search into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-40) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/2103.00020) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[41 · Multimodal Computer Vision](../41-multimodal-computer-vision/README.md)
