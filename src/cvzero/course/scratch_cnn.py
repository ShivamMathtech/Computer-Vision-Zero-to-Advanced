"""A complete tiny NumPy CNN with explicit parameter backpropagation.

Architecture: valid 3x3 correlation -> ReLU -> global mean -> linear -> softmax.
There is no autograd, OpenCV or PyTorch in this implementation. Sliding windows
and einsum express the same sums a slower nested-loop implementation would use.
"""

from __future__ import annotations

import numpy as np

from .numerics import softmax


def initialize(seed=42, filters=4, classes=2):
    rng = np.random.default_rng(seed)
    return {
        "kernel": rng.normal(0, 0.2, (filters, 3, 3)),
        "bias": np.zeros(filters),
        "weight": rng.normal(0, 0.2, (filters, classes)),
        "head_bias": np.zeros(classes),
    }


def forward_backward(images, labels, parameters):
    """Return mean cross entropy, probabilities and exact parameter gradients.

    Images have shape N,H,W, labels shape N, and kernels K,3,3. The correlation
    output is N,K,H-2,W-2. Gradients match each parameter's shape.
    """
    images = np.asarray(images, float)
    labels = np.asarray(labels, int)
    if images.ndim != 3 or min(images.shape[1:]) < 3 or len(images) != len(labels):
        raise ValueError("Use N,H,W images at least 3x3 and N integer labels.")
    windows = np.lib.stride_tricks.sliding_window_view(images, (3, 3), axis=(1, 2))
    preactivation = (
        np.einsum("nhwij,kij->nkhw", windows, parameters["kernel"])
        + parameters["bias"][None, :, None, None]
    )
    activated = np.maximum(preactivation, 0)
    features = activated.mean(axis=(2, 3))
    logits = features @ parameters["weight"] + parameters["head_bias"]
    probability = softmax(logits)
    loss = float(-np.log(probability[np.arange(len(labels)), labels] + 1e-12).mean())
    # Softmax + cross entropy derivative; mean reduction supplies 1/N.
    dlogits = probability.copy()
    dlogits[np.arange(len(labels)), labels] -= 1
    dlogits /= len(labels)
    dweight = features.T @ dlogits
    dhead_bias = dlogits.sum(axis=0)
    dfeatures = dlogits @ parameters["weight"].T
    spatial_count = activated.shape[2] * activated.shape[3]
    dpreactivation = dfeatures[:, :, None, None] / spatial_count * (preactivation > 0)
    dkernel = np.einsum("nkhw,nhwij->kij", dpreactivation, windows)
    dbias = dpreactivation.sum(axis=(0, 2, 3))
    gradients = {"kernel": dkernel, "bias": dbias, "weight": dweight, "head_bias": dhead_bias}
    return loss, probability, gradients


def stripe_data(count=32, size=10, seed=42):
    """Horizontal/vertical bars with random positions and small observation noise."""
    rng = np.random.default_rng(seed)
    labels = np.arange(count) % 2
    images = rng.uniform(0, 0.05, (count, size, size))
    for i, label in enumerate(labels):
        position = int(rng.integers(2, size - 3))
        if label == 0:
            images[i, :, position : position + 2] = 1
        else:
            images[i, position : position + 2, :] = 1
    return images, labels


def experiment(seed=42, steps=100, learning_rate=0.5):
    """Train on generated stripes and report accuracy on independent test stripes."""
    images, labels = stripe_data(seed=seed)
    test_images, test_labels = stripe_data(seed=seed + 1000)
    parameters = initialize(seed)
    losses = []
    for _ in range(steps):
        loss, _, gradients = forward_backward(images, labels, parameters)
        losses.append(loss)
        for name in parameters:
            parameters[name] -= learning_rate * gradients[name]
    _, probability, _ = forward_backward(test_images, test_labels, parameters)
    return {
        "losses": np.array(losses),
        "test_accuracy": float((probability.argmax(1) == test_labels).mean()),
        "parameters": parameters,
        "test_images": test_images,
        "seed": seed,
        "steps": steps,
        "learning_rate": learning_rate,
    }
