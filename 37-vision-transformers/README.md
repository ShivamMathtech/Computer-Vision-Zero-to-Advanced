# 37 · Vision Transformers

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

A Vision Transformer turns an image into a sequence of patch tokens and lets tokens exchange information through attention. This changes the inductive assumptions used by a CNN. Read the attention primer in Chapter 38 before implementing the transformer block here; the directory numbering follows the requested catalog.

## What You Will Learn

- Patch embeddings and positions
- Transformer encoder mechanics
- Train a simplified ViT

## Why It Matters

Implement small attention first, then a simplified ViT. Divide an image into non-overlapping patches, flatten each patch and project it into an embedding vector. A convolution with kernel and stride equal to the patch size performs the same shared projection. Position embeddings distinguish where tokens came from; otherwise attention alone does not encode the image grid order.

## Prerequisites

[24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md), [25 · Image Classification](../25-image-classification/README.md). First read [38 attention primer](../38-attention-mechanisms/theory/concepts.md); return here to build ViT.

## Core Concepts

Attention primer, query, key, value, patches, position, encoder, ViT, pretrained adaptation. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
N=(H/P)(W/P)
$$

H and W are image height and width, P square patch size and N the number of patch tokens when dimensions divide exactly. A 24×24 image with 6×6 patches produces 16 tokens. A worked Python calculation is included in every notebook.

## Practical Examples

TinyViT uses a patch projection, learned position embeddings, an encoder block, normalization, token averaging and a classifier. The source exposes each step instead of calling a pretrained model in the default notebook.

```bash
python -m cvzero.course --chapter 37 --lesson 0 --seed 42 --output artifacts/ch37-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Patch embeddings and positions](notebooks/01_foundations.ipynb)
- [2. Transformer encoder mechanics](notebooks/02_mechanisms.ipynb)
- [3. Train a simplified ViT](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Tiny Vision Transformer](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Reshape cannot replace a correct patch permutation. Pretrained position embeddings may need resizing when image resolution changes.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does patch embeddings and positions solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Double the number of tokens and estimate attention-matrix growth before measuring memory. Compare the tiny CNN and ViT on the same synthetic split. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Reshape cannot replace a correct patch permutation. Pretrained position embeddings may need resizing when image resolution changes. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Tiny Vision Transformer into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-37) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/2010.11929) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[38 · Attention Mechanisms](../38-attention-mechanisms/README.md)
