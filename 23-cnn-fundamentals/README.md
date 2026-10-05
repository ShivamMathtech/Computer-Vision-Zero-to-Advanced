# 23 · CNN Fundamentals

**Intermediate · CPU baseline · 3 focused notebooks · no required downloads**

A neural network composes simple differentiable operations. A CNN shares small learned filters across image locations, exploiting local structure. Begin with an explicit small network and derivatives, then connect those operations to a framework training loop.

## What You Will Learn

- Perceptrons, loss and backpropagation
- Convolution, padding and receptive fields
- A tiny trainable CNN

## Why It Matters

Derive a tiny network update and compare fixed and learned filters. A perceptron forms a weighted sum plus bias; a nonlinear activation lets multiple layers express more than one linear map. Forward propagation produces scores, a loss compares them with labels, and backpropagation applies the chain rule to obtain parameter gradients. The NumPy MLP includes explicit derivatives for tanh and softmax cross entropy.

## Prerequisites

[02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md), [05 · Image Processing](../05-image-processing/README.md), [22 · Machine Learning for Vision](../22-machine-learning-for-vision/README.md)

## Core Concepts

Perceptron, activation, forward pass, backpropagation, losses, gradient descent, stride, padding, pooling, receptive field. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
\frac{\partial L}{\partial z_j}=p_j-y_j
$$

z is a class logit, p=softmax(z), y a one-hot label and L single-example cross entropy. For p=[0.2,0.8] and label class 1, the logit gradient is [0.2,−0.2]. Average this gradient over a mean-reduced batch. A worked Python calculation is included in every notebook.

## Practical Examples

Inspect the NumPy weight and bias gradients, then compare a fixed kernel through NumPy correlation and PyTorch conv2d. The final lesson trains a CNN with independent generated test samples.

```bash
python -m cvzero.course --chapter 23 --lesson 0 --seed 42 --output artifacts/ch23-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

- [1. Perceptrons, loss and backpropagation](notebooks/01_foundations.ipynb)
- [2. Convolution, padding and receptive fields](notebooks/02_mechanisms.ipynb)
- [3. A tiny trainable CNN](notebooks/03_practical_experiments.ipynb)

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[Tiny CNN from First Principles](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

Calling backward accumulates gradients unless they are cleared. A decreasing training loss does not prove generalization.

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does perceptrons, loss and backpropagation solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

Remove the activation from a multilayer network and reason about which functions remain possible. Change stride and compute output size before running. What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

Calling backward accumulates gradients unless they are cleared. A decreasing training loss does not prove generalization. Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn Tiny CNN from First Principles into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-23) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

[24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md)

## Complete NumPy CNN

The practical notebook also trains a full small CNN without autograd. [Manual forward/backward source](../src/cvzero/course/scratch_cnn.py) includes valid correlation, ReLU, global mean pooling and a class head. Independent finite-difference tests check gradients for kernels, biases and head weights.
