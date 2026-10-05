# 38 · Attention Mechanisms

**Advanced · CPU baseline · 3 focused notebooks · no required downloads**

Attention is a data-dependent weighted average. Imagine asking a question of every item, scoring how relevant each item is, and combining the information from the most relevant items. Queries, keys and values are learned projections that make this comparison trainable.

## What You Will Learn

- Queries, keys and values
- Scaled dot-product attention
- Masks, heads and efficient attention

## Why It Matters

Investigate the attention mechanism introduced in Chapter 37. A query represents what a token seeks, a key represents how a token can be matched, and a value carries the information to combine. In self-attention all three come from the same sequence; in cross-attention queries and key/value tokens come from different sources. These are mathematical roles, not literal language questions.

## Prerequisites

[02 · Mathematics](../02-mathematics-for-computer-vision/README.md), [23 · CNN fundamentals](../23-cnn-fundamentals/README.md), [24 · PyTorch](../24-pytorch-for-computer-vision/README.md)

## Core Concepts

Scaled dot product, masks, multi-head attention, cross-attention, attention cost. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
Attention(Q,K,V)=softmax(QK^T/\sqrt{d_k})V
$$

Q and K are query/key matrices, V contains values and dk is key width. Softmax acts over keys for each query. Equal scores over two values [2,6] yield their mean 4. A worked Python calculation is included in every notebook.

## Practical Examples

The reference returns both weighted values and the attention matrix, allowing row sums and masked entries to be inspected. Framework comparison uses matching inputs and mask conventions.

```bash
python -m cvzero.course --chapter 38 --lesson 0 --seed 42 --output artifacts/ch38-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Queries, keys and values](notebooks/01_foundations.ipynb)
- [2. Scaled dot-product attention](notebooks/02_mechanisms.ipynb)
- [3. Masks, heads and efficient attention](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Attention Inspector](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

A softmax over the wrong axis can still produce plausible array shapes. Attention weights are not automatically causal explanations of predictions.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does queries, keys and values solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Scale query/key magnitudes and inspect whether attention becomes peaked. Apply a triangular mask and verify forbidden weights are zero. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

A softmax over the wrong axis can still produce plausible array shapes. Attention weights are not automatically causal explanations of predictions. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Attention Inspector into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-38) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://arxiv.org/abs/1706.03762) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[39 · Self-Supervised Learning](../39-self-supervised-learning/README.md)
