# 20 · Face Recognition

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

Recognition compares representations to decide whether two observations may share an identity. Verification is a one-to-one comparison; identification searches a gallery. The educational lab uses synthetic vectors and anonymous labels so the decision mechanics can be learned without collecting biometric data.

## What You Will Learn

- Embeddings, PCA and distance
- Verification thresholds and open sets
- Evaluation, consent and failure cases

## Why It Matters

Study small consented verification experiments with error analysis. An embedding is a vector intended to preserve useful similarity. PCA projects data onto directions of high variance; it does not automatically learn identity. Face-recognition systems usually train a representation with identity-related supervision and carefully align crops. The synthetic lab separates the geometry of embeddings from those data and training requirements.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [19 · Face Detection](../19-face-detection/README.md)

## Core Concepts

Embedding distance, verification vs identification, thresholds, false matches, bias, consent. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
s(a,b)=\frac{a^Tb}{\lVert a\rVert\lVert b\rVert}
$$

a and b are nonzero embedding vectors and s is cosine similarity. For a=[1,0] and b=[1,1], similarity is 1/√2, about 0.707. A threshold is a deployment choice, not a universal constant. A worked Python calculation is included in every notebook.

## Practical Examples

Generated cluster prototypes create anonymous identities. PCA and nearest-prototype comparison demonstrate distance and rejection; they do not constitute a pretrained human-face recognition system.

```bash
python -m cvzero.course --chapter 20 --lesson 0 --seed 42 --output artifacts/ch20-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Embeddings, PCA and distance](notebooks/01_foundations.ipynb)
- [2. Verification thresholds and open sets](notebooks/02_mechanisms.ipynb)
- [3. Evaluation, consent and failure cases](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Local Opt-in Verification Lab](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Selecting the threshold on the test set leaks evaluation information. Good synthetic cluster separation is not evidence of biometric performance.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does embeddings, pca and distance solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Add unknown synthetic identities and sweep the threshold. Plot false acceptance and false rejection rather than only closed-set accuracy. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Selecting the threshold on the test set leaks evaluation information. Good synthetic cluster separation is not evidence of biometric performance. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Local Opt-in Verification Lab into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-20) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[21 · OCR](../21-ocr/README.md)
